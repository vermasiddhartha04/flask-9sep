from flask import Blueprint, request, render_template, redirect, session, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, Role, RoleMapping, db
from .middleware import auth, guest

main = Blueprint('main', __name__)

@main.route('/')
@guest
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
@guest
def register():
    if request.method == 'POST':
        pass    
    return render_template('register.html')

@main.route('/dashboard')
@auth
@jwt_required()
def dashboard():
    curr_user_id = get_jwt_identity()
    user = User.query.filter_by(id=curr_user_id['id']).first()
    return render_template('dashboard.html', user=user)
