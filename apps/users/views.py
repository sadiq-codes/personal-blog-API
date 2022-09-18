from routes import api
from flask import request, make_response, jsonify
from flask_jwt_extended import jwt_required, set_access_cookies
from .. import jwt, db
from .forms import LoginForm, SignUp
from .models import User


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()


@api.route('/login', methods=['POST'])
def user_login():
    form = LoginForm(data=request.form)
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(password=form.password.data):
            response = jsonify({"msg": "login successful"})
            access_token = user.generate_auth_token(user)
            set_access_cookies(response, access_token)
            return jsonify({"email: ": user.email,
                            "is Admin": user.is_admin,
                            "access_token": access_token,
                            }), 200
        return jsonify("Wrong username or password"), 401
    print(form.errors)
    return jsonify({"message": "Enter your details to get access token"}), 200


@api.route('/signup', methods=["GET", "POST"])
@jwt_required()
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
    pass


@api.route('profile', methods=['GET'])
def profile(id):
    user = User.query.get_or_404(id)
    return jsonify({
        "name": user.name,
        "email": user.email,

    })



