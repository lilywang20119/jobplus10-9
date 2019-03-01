from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.models import User,Company
from jobplus.forms import LoginForm, User_RegisterForm,Company_RegisterForm
from flask_login import login_user, logout_user, login_required
from flask import request, current_app

front = Blueprint('front', __name__)

@front.route('/')
def index():

    return render_template('index.html')

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        company = Company.query.filter_by(email=form.email.data).first()

        if user:
            login_user(user, form.remember_me.data)
            next = 'user.profile'
            if user.is_admin:
                next = 'admin.index'

        elif company:
            login_user(company, form.remember_me.data)
            next = 'company.profile'

       # next = 'user.profile'
       # if user.is_admin:
        #    next = 'admin.index'
        #elif user.is_company:
         #   next = 'company.profile'
        return redirect(url_for(next))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success', 'success')
    return redirect(url_for('.index'))

@front.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = User_RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('.login'))
    return render_template('user_register.html', form=form)

@front.route('/company_register', methods=['GET', 'POST'])
def company_register():
    form = Company_RegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('.login'))
    return render_template('company_register.html', form=form)