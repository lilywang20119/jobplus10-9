from flask import url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class User(Base,UserMixin):
    __tablename__='user'
    ROLE_USER=10
    ROLE_COMMPANY=20
    ROLE_ADMIN=30
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,index=True,nullable=False)
    email=db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password=db.Column('password',db.String(64),nullable=False)
    role=db.Column(db.SmallInteger,default=ROLE_USER)
    user_jobs=db.relationship('Job')
    
    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return_password
    
    @password.setter
    def password(self,orig_password):
        self._password=genetate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY
    

class Company(Base):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(256),unique=True,index=True,nullable=False)
    email=db.Column(db.String(64),nullable=False)
    number=db.Column(db.String(64),nullable=False)
    slug=db.Column(db.String(64),unique=True,index=True,nullable=False)
    address=db.Column(db.String(128),nullable=False)
    site=db.Column(db.String(64),nullable=False)
    logo=db.Column(db.String(128),nullable=False)
    description=db.Column(db.Text())
    details=db.Column(db.String(256))
    tags=db.Column(db.String(64))
    location=db.Column(db.String(32))
    users=db.relationship('User',uselist=False)

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    
class Job(Base):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),nullable=False)
    wage_low=db.Column(db.Integer,nullable=False)
    wage_high=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String(32),nullable=False)
    tags=db.Column(db.String(64))
    experience=db.Column(db.String(64))
    degree=db.Column(db.String(64))
    companies=db.relationship('Company',uselist=False)
    
    def __repr__(self):
        return '<Job:{}>'.format(self.name)

class Delivery(Base):
    STATUS_WAITING=1
    STATUS_REJECT=2
    STATUS_ACCEPT=3

    id=db.Column(db.Integer,primary_key=True)
    job_id=db.Column(db.Integer,db.ForeignKey('job.id',ondelete='CASCADE'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    status=db.Column(db.SmallInteger,default=STATUS_WAITING)

