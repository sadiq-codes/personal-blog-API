from routes import api
from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, set_access_cookies,  unset_jwt_cookies
from .. import jwt, db
from .forms import LoginForm, SignUp
from .models import User
from ..errors import bad_request


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()


@api.route('/login', methods=['POST'])
def user_login():
    form = LoginForm(data=request.json)
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(password=form.password.data):
            response = jsonify({"message": "login successful"})
            access_token = user.generate_auth_token(user)
            set_access_cookies(response, access_token)
            return jsonify({"email": user.email,
                            "is_admin": user.is_admin(),
                            "access_token": access_token,
                            }), 200
        return jsonify("Wrong username or password"), 401
    if form.errors:
        return bad_request(message=form.errors)


@api.route('/signup', methods=["GET", "POST"])
def user_signup():
    form = SignUp(data=request.form)
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(username=form.username.data,
                        name=form.name.data,
                        email=form.email.data.lower(),
                        hash_password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return make_response("user created successfully")
        return make_response("User already exist")
    return make_response("Enter your details to register")


@api.route('/logout', methods=['GET'])
@jwt_required()
def user_logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@api.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "name": user.name,
        "email": user.email,
    })



