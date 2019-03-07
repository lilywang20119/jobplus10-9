from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.models import User,db,Job
from jobplus.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from flask import request, current_app

front = Blueprint('front', __name__)

@front.route('/')
def index():
    jobs = [Job.query.all()[i] for i in [27,3,6,8,13,17]]
    companies = [User.query.all()[i] for i in [1,2,3,4,5,9]]
    return render_template('index.html',jobs=jobs,companies=companies)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        '''
        user = User.query.filter_by(name=form.name.data).first()
        if not user:
            user = User.query.filter_by(email=form.name.data).first()

        '''
        user = form.user
        if user.is_disable:
            flash('用户已经被禁用','info')
            return redirect(url_for('.login'))
        if user:
            login_user(user, form.remember_me.data)
            next = 'user.profile'
            if user.is_admin:
                next = 'admin.index'
            elif user.is_company:
                next = 'company.profile'
        flash('您已登录成功', 'success')
        return redirect(url_for(next))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'success')
    return redirect(url_for('.index'))

@front.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户注册成功，请登录', 'success')
        return redirect(url_for('.login'))
    return render_template('user_register.html', form=form)

@front.route('/company_register', methods=['GET', 'POST'])
def company_register():
    form = RegisterForm()
    form.name.label = u'企业名称'
    if form.validate_on_submit():
        user = form.create_user()
        user.role = User.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)
