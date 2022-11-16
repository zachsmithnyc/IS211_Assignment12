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

@bp.route('/student/add')
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()
        error = None

        if not name:
            error = 'Please enter a name.'
        
        if error is None:
            try:
                db.execute(
                    'INSET INTO students (name) VALUES (?,)',
                    (name,)
                    )
                db.commit()
            except db.IntegrityError:
                error = f"Student {name} has already been added."
            else:
                return redirect(url_for('dashboard'))
        
        flash(error)

    return render_template('dashboard/addstudent.html')
    
