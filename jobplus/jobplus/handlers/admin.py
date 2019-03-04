from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import User,Job
from jobplus.forms import User_RegisterForm, JobForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = User_RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/create_user.html', form=form)


@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = User_RegisterForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('用户更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination)


@admin.route('/jobs/create', methods=['GET', 'POST'])
@admin_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        form.create_job()
        flash('创建成功', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/create_job.html', form=form)


@admin.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash('更新成功', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('admin/edit_job.html', form=form, job=job)

