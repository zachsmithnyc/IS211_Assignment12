import os 
import functools
import sqlite3 as lite
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask

test_config=None
    #create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = 'dev',
    DATABASE=os.path.join(app.instance_path, 'quizapp.sqlite'),
    )

if test_config is None:
    # load the instance config, if it exits, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

#ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
    
def get_db():
    '''Connect to the application's configured database.
    The connection is unique and will by reused if this is called again. 
    '''
    db = lite.connect(
        app.config['DATABASE'],
        detect_types=lite.PARSE_DECLTYPES
        )
    db.row_factory = lite.Row

    return db

def init_db():
    '''Initializes the db.'''
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def register_admin():
    username = 'admin'
    password = 'password'

    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?,?)",
        (username, generate_password_hash(password)),
    )
    db.commit()



@app.route('/register', methods=('GET', 'POST'))
def register():
    ''' 
    Registers a new User.
    Validates that username is not taken.
    hashes password. 
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("login"))
        flash(error)
    
    return render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    '''Log in a registered user by adding their id to the session'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect('/')

        flash(error)
    
    return render_template('auth/login.html')

@app.before_request
def load_logged_in_user():
    '''if a use id is stored in the session
    load the user object from the database into g.user
    '''
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@app.route('/logout')
def logout():
    '''clear the current session, including stored user id'''
    session.clear()
    return redirect('/')

def login_required(view):
    '''view decorator that redirects anonymous users to the login page'''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)
    
    return wrapped_view

@app.route('/')
def index():
    db = get_db()
    students = db.execute(
        'SELECT id, name FROM students'
    ).fetchall()
    quizzes = db.execute(
        'SELECT quiz_id, subject, length, date FROM quizzes'
    ).fetchall()
    return render_template('dashboard/dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods = ('GET', 'POST'))
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Please enter a name.'

        if error is not None:
            flash(error)
        else:
            try:
                db = get_db()
                db.execute(
                    'INSERT INTO students (name)'
                    ' VALUES (?)', 
                    (name,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Student {name} has already been added."
                flash(error)
            else:
                return redirect('/')

    return render_template('dashboard/addstudent.html')

@app.route('/quiz/add', methods = ('GET', 'POST'))
@login_required
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        length = request.form['length']
        date = request.form['date']
        error = None

        if not subject:
            error = 'Please enter a subject.'
        elif not length:
            error = 'Please enter a length'
        elif not date:
            error = 'Please enter a date'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO quizzes (subject, length, date)' 
                ' VALUES (?, ?, ?)', 
                (subject, length, date)
                )
            db.commit()
            return redirect('/')

    return render_template('dashboard/addquiz.html')

def get_results(id):
    results = get_db().execute(
        'SELECT quiz_id, student_name, student_id, score'
        ' FROM quiz_results q JOIN students s ON q.student_id = s.id'
        ' WHERE q.student_id = ?',
        (id,)
    ).fetchall()

    return results


@app.route('/results/<int:id>', methods=('GET', 'POST'))
@login_required
def view_results(id):
    results = get_results(id)
    error = None

    if not results:
        error = 'No Results Available'
    
    if error is not None:
        flash(error)

    return render_template('dashboard/viewresults.html', results=results)


@app.route('/result/add', methods=('GET', 'POST'))
@login_required
def add_result():
    db = get_db()
    student_options = db.execute(
        'SELECT s.name, s.id'
        ' FROM students s'
    ).fetchall()

    quiz_options = db.execute(
        'SELECT quiz_id'
        ' FROM quizzes'
    ).fetchall()

    if request.method == 'POST':
        student_id = request.form['student_id']
        student_name = request.form['name']
        quiz_id = request.form['quiz_id']
        score = request.form['score']
        error = None

        if not student_id:
            error = "Please enter student id"
        elif not student_name:
            error = "Please enter student name"
        elif not quiz_id:
            error = "Please enter quiz_id"
        elif not score:
            error = "Please enter score"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO quiz_results (quiz_id, student_id, student_name, score)'
                ' VALUES (?, ?, ?, ?)',
                (quiz_id, student_id, student_name, score)
            )
            db.commit()
            return redirect('/')

    return render_template('dashboard/add_result.html', student_options=student_options, quiz_options=quiz_options)

if __name__ == '__main__':
    init_db()
    register_admin()
    app.run(debug=True)