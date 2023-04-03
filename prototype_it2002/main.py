from flask import Blueprint, render_template, session, abort, request

from prototype_it2002.user_serializer import get_user, get_matches

main_ = Blueprint('main', __name__)

@main_.route('/')
def index():
    return render_template('index.html')


@main_.route('/profile')
def profile():
    if session.get('current_user', None):
        user_attr = get_user(session['current_user']['email'])
        return render_template('profile.html', current_user=user_attr)
    else:
        abort(403)


@main_.route('/findform', methods=['POST'])
def find_form():
    if session.get('current_user', None):
        return render_template('findform.html')


@main_.route('/match', methods=['POST', 'GET'])
def get_match():
    if request.method == "POST":
        email = session['current_user']['email']
        current_user = get_user(email)
        if session['current_user']['role'] == "TUTOR":
            preferred_zones = request.form.getlist('preferred_zones[]')
            results = get_matches(email=email, preferred_zones=preferred_zones)
        if session['current_user']['role'] == "STUDENT":
            preferred_qualification = request.form.getlist('preferred_qualification[]')
            preferred_gender = request.form.get("preferred_gender")
            results = get_matches(email=email, preferred_qualification=preferred_qualification, preferred_gender=preferred_gender)
        if not results:
            return "Nothing was found"
    
    return render_template('matchlist.html', results=results, current_user=current_user)
