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
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        length = request.form['length']
        date = request.form['date']
        db = get_db()
        error = None

        if not subject:
            error = 'Please enter a subject.'
        if not length:
            error = 'Please enter a length'
        if not date:
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
        'SELECT '
    )


@bp.route('/student/<int:id>', methods = ('POST'))
def view_results(id):
    return render_template('dashboard/viewresults')
    
