from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from prototype_it2002.user_serializer import get_user_password, get_user, create_user

auth_ = Blueprint('auth', __name__)

@auth_.route('/login')
def login():
    return render_template('/login.html')


@auth_.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user_password = get_user_password(email)
    
    if not user_password or password != user_password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    user_attr = get_user(email)
    session['current_user'] = {}
    session['current_user']['email'] = email
    session['current_user']['role'] = user_attr['role']

    return redirect(url_for('main.index'))

@auth_.route('/signup')
def signup():
    return render_template('/signup.html')

@auth_.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user_attr = get_user(email)

    if user_attr: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    create_user(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    session['current_user']['email'] = email

    return redirect(url_for('auth.login'))

@auth_.route('/logout')
def logout():
    session.pop('current_user', None)
    return redirect(url_for('main.index'))
