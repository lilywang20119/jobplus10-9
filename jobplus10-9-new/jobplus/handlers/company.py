from flask import Blueprint,render_template,flash,redirect,url_for,request,current_app
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileForm
from jobplus.models import db,User,Job,CompanyDetail

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
