from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Length,Email,EqualTo,DataRequired,Regexp
from jobplus.models import db,User,Company
from wtforms import ValidationError
from wtforms import TextAreaField,IntegerField
from wtforms.validators import URL,NumberRange

class User_RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(3,24)])
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户已经注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

class Company_RegisterForm(FlaskForm):
    name = StringField('企业名称',validators=[DataRequired(),Length(3,24)])
    email = StringField('企业邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def create_company(self):
        company = Company(name = self.name.data,
                       email = self.email.data,
                       password = self.password.data)
        db.session.add(company)
        db.session.commit()
        return company


    def validate_company_name(self,field):
        if Company.query.filter_by(company_name=field.data).first():
            raise ValidationError('企业用户已经注册')

    def validate_email(self,field):
        if Company.query.filter_by(email=field.data).first():
            raise ValidationError('企业邮箱已经注册')


class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self,field):
        if field.data and not (User.query.filter_by(email=field.data).first() or Company.query.filter_by(email=field.data).first()):
            raise ValidationError('邮箱未注册')
        #if field.data and not Company.query.filter_by(email=field.data).first():
         #   raise ValidationError('企业邮箱未注册')

    def validate_password(self,field):
        user = User.query.filter_by(email=self.email.data).first()
        company = Company.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
        if company and not company.check_password(field.data):
            raise ValidationError('密码错误')



class UserProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）', validators=[DataRequired(), Length(6, 24)])
    phone = StringField('手机号',validators=[DataRequired('请输入手机号码'),Regexp("1[3578]\d{9}",message="手机格式不正确")])
    work_years = IntegerField('工作年限')
    resume_url = StringField('上传简历')
    submit = SubmitField('提交')

    def update_profile(self,user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码(不填写保持不变)')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 24)])
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
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()