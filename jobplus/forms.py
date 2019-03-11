from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField,IntegerField,ValidationError,SelectField
from wtforms.validators import Length,Email,EqualTo,DataRequired,Regexp,URL
from .models import db,User,CompanyDetail,Resume,Job
from flask_wtf.file import FileField,FileRequired,FileAllowed
import os
from flask import url_for

class RegisterForm(FlaskForm):
    name = StringField('用户名',validators=[DataRequired(),Length(3,24)])
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        '''
        user.name = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        '''
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


    def validate_name(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户已经注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')


class LoginForm(FlaskForm):
    name = StringField('用户名 / 邮箱',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_name(self,field):
        u1 = User.query.filter_by(name=field.data).first()
        u2 = User.query.filter_by(email=field.data).first()
        if not u1 and not u2:
            raise ValidationError('用户名或邮箱不存在')

    def validate_password(self,field):
        user = User.query.filter_by(name=self.name.data).first()
        if not user:
            user = User.query.filter_by(email=self.name.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
        self.user = user

class ResumeForm(FlaskForm):
    name = StringField('姓名',validators=[DataRequired(),Length(2,24)])
    age = StringField('年龄',validators=[DataRequired()])
    work_age = StringField('工龄',validators=[DataRequired()])
    home_city = StringField('家乡城市',validators=[DataRequired()])
    job_experience = TextAreaField('工作经历')
    edu_experience = TextAreaField('教育经历')
    project_experience = TextAreaField('项目经历')
    resume = FileField('上传文件',validators=[FileAllowed(['pdf','txt','py','zip'])])
    submit = SubmitField('提交')

    def upload_resume(self):
        f = self.resume.data
        filename = self.name.data + '.pdf'
        f.save(os.path.join(os.getcwd(),'jobplus/static/resumes',filename))
        return url_for('static',filename=os.path.join('resumes',filename))

    def get_resume(self,resume):
        self.populate_obj(resume)
        resume.resume_url = self.upload_resume()
        db.session.add(resume)
        db.session.commit()
        return resume

class UserProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    phone = StringField('手机号',validators=[DataRequired('请输入手机号码'),
            Regexp("1[3578]\d{9}",message="手机格式不正确")])
    work_years = IntegerField('工作年限')
    resume = FileField('上传简历',validators=[FileAllowed(['pdf','txt','py','zip'])])
    submit = SubmitField('提交')

    def update_profile(self,user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        filename = self.upload_resume()
        user.upload_resume_url = url_for('static',filename=os.path.join('resumes',filename))
        db.session.add(user)
        db.session.commit()

    def upload_resume(self):
        f = self.resume.data
        print(f)
        filename = self.name.data + '.pdf'
        f.save(os.path.join(os.getcwd(), 'jobplus/static/resumes', filename))
        return filename

class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    slug = StringField('Slug', validators=[DataRequired(), Length(0, 24)])
    location = StringField('地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')


    def update_profile(self,user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        if user.companydetail:
            companydetail = user.companydetail
        else:
            companydetail = CompanyDetail()
            companydetail.user_id = user.id
        self.populate_obj(companydetail)
        db.session.add(user)
        db.session.add(companydetail)
        db.session.commit()

class UserEditForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    phone = StringField('手机号', validators=[DataRequired('请输入手机号码'),
                                           Regexp("1[3578]\d{9}", message="手机格式不正确")])
    submit = SubmitField('提交')

    def update_user(self,user):
        self.populate_obj(user)
        if self.password.data:
            user.password = self.password.data
        db.session.add(user)
        db.session.commit()

class CompanyEditForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')


    def update_company(self,company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.companydetail:
            companydetail = company.companydetail
        else:
            companydetail = CompanyDetail()
            companydetail.user_id = company.id
        companydetail.site = self.site.data
        companydetail.description = self.description.data
        self.populate_obj(companydetail)
        db.session.add(companydetail)
        db.session.add(company)
        db.session.commit()

class JobForm(FlaskForm):
    name = StringField('职位名称')
    salary = StringField('薪资范围')
    location = StringField('工作地点')
    tags = StringField('职位标签（多个用，隔开）')
    experience_requirement = SelectField('经验要求(年)',choices=[
        ('不限','不限'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('1-3','1-3'),
        ('3-5','3-5'),
        ('5+','5+')
    ])
    degree_requirement = SelectField('学历要求',choices=[
        ('不限','不限'),
        ('专科', '专科'),
        ('本科', '本科'),
        ('硕士', '硕士'),
        ('博士', '博士')
    ])
    description = TextAreaField('职位描述', validators=[Length(0, 100)])
    submit = SubmitField('提交')

    def create_job(self,company):
        job = Job()
        self.populate_obj(job)
        job.company_id=company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self,job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job


