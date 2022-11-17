from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from quizapp.auth import login_required
from quizapp.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    db = get_db()
    students = db.execute(
        'SELECT id, name FROM students'
    ).fetchall()
    quizzes = db.execute(
        'SELECT quiz_id, subject, length, date FROM quizzes'
    ).fetchall()
    return render_template('dashboard/dashboard.html', students=students, quizzes=quizzes)

@bp.route('/student/add', methods = ('GET', 'POST'))
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
                return redirect(url_for('dashboard'))

    return render_template('dashboard/addstudent.html')

@bp.route('/quiz/add', methods = ('GET', 'POST'))
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
            return redirect(url_for('dashboard'))

    return render_template('dashboard/addquiz.html')

def get_results(id):
    results = get_db().execute(
        'SELECT quiz_id, student_name, student_id, score'
        ' FROM quiz_results q JOIN students s ON q.student_id = s.id'
        ' WHERE q.student_id = ?',
        (id,)
    ).fetchall()

    return results


@bp.route('/results/<int:id>', methods=('GET', 'POST'))
@login_required
def view_results(id):
    results = get_results(id)
    error = None

    if not results:
        error = 'No Results Available'
    
    if error is not None:
        flash(error)

    return render_template('dashboard/viewresults.html', results=results)


@bp.route('/result/add', methods=('GET', 'POST'))
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
            return redirect(url_for('dashboard'))

    return render_template('dashboard/add_result.html', student_options=student_options, quiz_options=quiz_options)

    
