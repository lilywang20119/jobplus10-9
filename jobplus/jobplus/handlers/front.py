from flask import Blueprint,url_for,render_template,flash,redirect
from flask import current_app,request
from jobplus.models import User,Company
from jobplus.forms import User_RegisterForm,Company_RegisterForm,LoginForm
from flask_login import login_user,logout_user,login_required

front=Blueprint('front',__name__)

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/userregister',methods=['GET','POST'])
def userregister():
    form=User_RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录','success')
        redirect(url_for('front.login'))
    return render_template('user_register.html',form=form)

@front.route('/companyregister',methods=['GET','POST'])
def companyregister():
    form=Company_RegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录','success')
        redirect(url_for('front.login'))
    return render_template('company_register.html',form=form)

@front.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        company=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        login_user(company,form.remember_me.data)
        redirect(url_for('front.index'))
    return render_template('login.html',form=form)

