from flask import Blueprint,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileForm

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = CompanyProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('个人信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)
