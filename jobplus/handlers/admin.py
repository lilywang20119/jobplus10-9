from flask import (Blueprint, render_template, request, current_app,
     redirect, url_for, flash)
from jobplus.models import User, db, Job

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def index():
    return render_template('admin/index.html')