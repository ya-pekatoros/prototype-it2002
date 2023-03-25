from flask import Blueprint, render_template
from app import db
from flask_login import login_required, current_user

main_ = Blueprint('main', __name__)

@main_.route('/')
def index():
    return render_template('index.html')

@login_required
@main_.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)
