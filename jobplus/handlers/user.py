from flask import Blueprint,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
from jobplus.forms import ResumeForm
from jobplus.models import User, Resume, db, CompanyDetail

user = Blueprint('user',__name__,url_prefix='/user')

@user.route('/profile')
@login_required
def profile():
    resume = current_user.resume
    return render_template('user/profile.html',resume=resume)

@user.route('<int:user_id>/edit_resume',methods=['GET','POST'])
@login_required
def edit_resume(user_id):
    resume = Resume.query.join(User).filter(User.id==user_id).first()
    if not resume:
        user = User.query.filter_by(id=user_id).first()
        resume = Resume(
            id=user_id,
            name=user.name
        )
    form = ResumeForm(obj=resume)
    if form .validate_on_submit():
        form.get_resume(resume)
        flash('简历已更新','warning')
        return redirect(url_for('.profile',user_id=current_user.id))
    return render_template('user/edit_resume.html',form=form)
