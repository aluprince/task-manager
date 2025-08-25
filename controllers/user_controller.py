from models.user import User
from flask import  jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime as dt
from Jwt_helpers.helper_tokens import create_access_token, create_refresh_token, decode_token


bcrypt = Bcrypt()


def register_user(data):
    # Later work on when the user does not input anything inside the field
    # Work on sending OTP to know if the email is still active
    try:
        hashed_password = bcrypt.generate_password_hash(password=data["password"]).decode("utf-8")
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password
        )
        new_user.save()
        return {"message": "user successfully saved"}, 201
    except Exception as e:
        print(f"This is the cause b: {e}")


def login_user(data):
    user = User.objects(email=data["email"]).first()
    print(user)
    password_is_correct = bcrypt.check_password_hash(user["password"], data["password"])
    print(password_is_correct)
    try:
        if not user or not password_is_correct:
            return jsonify({"error": 'Invalid Credentials'}), 401

        user_identity = {
            "name": user.name,
            "email": user.email,
            "id": str(user.id)
        }

        access_token = create_access_token(user_identity)
        print(access_token)
        refresh_token = create_refresh_token(user_identity)
        print(f"This is the refresh token: {refresh_token}")
        resp = make_response(jsonify({"message": "Login Successful!"}))
        
        resp.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            samesite="Strict",
            secure=False
        )

        resp.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            samesite="Strict",
            secure=False
        )

        return resp, 201

    except Exception as e:
        print(f"This is the cause: {e}")



