from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import redirect, url_for

def auth(view_func):
    @wraps(view_func)
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        if not user_id:
            return redirect(url_for('main.login'))
        return view_func(*args, **kwargs)
    return decorated

def guest(view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        if user_id:
            return redirect(url_for('main.dashboard'))
        return view_func(*args, **kwargs)
    return decorated
