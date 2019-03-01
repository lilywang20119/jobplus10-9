from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import url_for

from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin

# 注意这里不再传入 app 了
db = SQLAlchemy()
#中间表


class Base(db.Model):
    #不需要创建表
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

user_job = db.Table(
    'user_job',Base.metadata,
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE')),
    db.Column('job_id',db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
)
class User(Base,UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)
    # 一对一的关系
    resume = db.relationship('Resume',uselist=False)
    collect_jobs = db.relationship('Job',secondary=user_job)
    upload_resume_url = db.Column(db.String(64))

    #企业用户详情
    detail = db.relationship('Company',uselist=False)


    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_staff(self):
        return self.role == self.ROLE_USER



class Company(Base,UserMixin):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    concat = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True, index=True)
    location = db.Column(db.String(24))
    site = db.Column(db.String(64))
    logo = db.Column(db.String(128))

    description = db.Column(db.Text())
    details = db.Column(db.String(256))
    tags = db.Column(db.String(64))
    #公司技术栈
    stack = db.Column(db.String(128))
    #团队介绍
    team_introduction = db.Column(db.String(256))
    #公司福利
    welfares = db.Column(db.String(256))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    #uselist=False限制表为一对一关系，backref给User的每条数据对象增加company属性
    user = db.relationship('User', uselist=False,backref=db.backref('company',uselist=False))

    def __repr__(self):
        return '<Company:{}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(32), nullable=False)
    tags = db.Column(db.String(64))
    experience_requirement = db.Column(db.String(64))
    degree_requirement = db.Column(db.String(64))
    is_fulltime = db.Column(db.Boolean,default=True)
    #是否在招聘
    is_open = db.Column(db.Boolean,default=True)
    company_id = db.Column(db.Integer,db.ForeignKey('company.id',ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)
    views_count = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)


class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #复合主键
    user = db.relationship('User',uselist=False) #一对一关系
    job_experience = db.relationship('JobExperience')
    edu_experience = db.relationship('EduExperience')
    project_experience = db.relationship('ProjectExperience')

    def profile(self):
        pass

class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer,primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    #在职期间，做了什么，解决了什么问题，做出了什么贡献
    #在校期间，做了什么，获得荣誉
    #项目期间，做了什么，解决了什么问题
    description = db.Column(db.String(1024))




class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32),nullable=False)
    city = db.Column(db.String(32),nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(64),nullable=False)
    #专业
    major = db.Column(db.String(32),nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


class ProjectExperience(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32),nullable=False)
    role = db.Column(db.String(32))
    technology = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

class Delivery(Base):
    __tablename__ = 'delivery'

    #等待企业审核
    STATUS_WAITING = 1
    #被拒绝
    STATUS_REJECT = 2
    #被接受等待面试通知
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id',ondelete='SET NULL'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='SET NULL'))
    status = db.Column(db.SmallInteger,default=STATUS_WAITING)
    #企业回应
    response = db.Column(db.String(256))
