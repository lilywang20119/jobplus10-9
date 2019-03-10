from flask import Blueprint,render_template,flash,redirect,url_for,request,current_app,abort
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileForm,JobForm
from jobplus.models import db,User,Job,CompanyDetail,Delivery


company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=20).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html',pagination=pagination,active='job')


@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = CompanyProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)


@company.route('/<int:company_id>/detail')
def detail(company_id):
    company = User.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company)

@company.route('/<int:company_id>/admin')
@login_required
def admin_index(company_id):
    if not current_user.is_admin and not current_user.id == company_id:
        abort(404)
    page = request.args.get('page',default=1,type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )

    return render_template('company/admin_index.html',company_id=company_id,pagination=pagination)

@company.route('/<int:company_id>/admin/add_job',methods=['POST','GET'])
@login_required
def admin_add_job(company_id):
    if current_user.id != company_id:
        abort(404)
    form = JobForm()
    form.name.label=u'职位名称'
    if form.validate_on_submit():
        form.create_job(current_user)
        flash('职位增加成功','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/add_job.html',form=form,company_id=company_id)


@company.route('/<int:company_id>/admin/edit_job/<int:job_id>',methods=['POST','GET'])
@login_required
def admin_edit_job(company_id,job_id):
    if current_user.id != company_id:
        abort(404)
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.id:
        abort(404)
    form = JobForm(obj=job)
    form.name.label=u'职位名称'
    if form.validate_on_submit():
        form.update_job(job)
        flash('职位更新成功','success')
        return redirect(url_for('company.admin_index',company_id=current_user.id))
    return render_template('company/edit_job.html',form=form,company_id=company_id,job=job)

@company.route('/<int:company_id>/admin/jobs/<int:job_id>/delete')
@login_required
def admin_delete_job(company_id,job_id):
    if current_user.id != company_id:
        abort(404)
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.id:
        abort(404)
    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功', 'success')
    return redirect(url_for('company.admin_index', company_id=current_user.id))

@company.route('/<int:company_id>/admin/apply')
@login_required
def admin_apply(company_id):
    if not current_user.is_admin and not current_user.id == company_id:
        abort(404)
    status = request.args.get('status','all')
    page = request.args.get('page',default=1,type=int)
    q = Delivery.query.filter_by(company_id=company_id)
    if status=='waiting':
        q = q.filter(Delivery.status==Delivery.STATUS_WAITING)
    elif status=='accept':
        q = q.filter(Delivery.status==Delivery.STATUS_ACCEPT)
    elif status=='reject':
        q = q.filter(Delivery.status==Delivery.STATUS_REJECT)

    pagination = q.order_by(Delivery.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )

    return render_template('company/admin_apply.html',company_id=company_id,pagination=pagination)


@company.route('/<int:company_id>/admin/apply/<int:delivery_id>/reject')
@login_required
def admin_apply_reject(company_id,delivery_id):
    d = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    d.status = Delivery.STATUS_REJECT
    flash('已经拒绝该投递','sucess')
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('company.admin_apply',company_id=company_id))

@company.route('<int:company_id>/admin/apply/<int:delivery_id>/accept')
@login_required
def admin_apply_accept(company_id,delivery_id):
    d = Delivery.query.get_or_404(delivery_id)
    if current_user.id != company_id:
        abort(404)
    d.status = Delivery.STATUS_ACCEPT
    flash('已经接受该投递，可以安排面试了','sucess')
    db.session.add(d)
    db.session.commit()
    return redirect(url_for('company.admin_apply', company_id=company_id))