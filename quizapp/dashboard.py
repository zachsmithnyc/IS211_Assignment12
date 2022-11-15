from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from quizapp.auth import login_required
from quizapp.db import get_db

bp = Blueprint('dashboard', __name__)