from flask import render_template
from flask_login import current_user
from functools import wraps
from jobplus.models import User

def role_required(role):

    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if not current_user.is_authenticated or current_user.role < role:
                return render_template('404.html')
            return func(*args,**kwargs)
        return wrapper
    return decorator

user_required = role_required(User.ROLE_USER)
admin_required = role_required(User.ROLE_ADMIN)
