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
    
