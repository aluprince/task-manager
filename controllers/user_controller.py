from models.user import User
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime as dt
from Jwt_helpers.helper_tokens import create_access_token, create_refresh_token, decode_token


bcrypt = Bcrypt()


def register_user(data):
    # Later work on when the user does not input anything inside the field
    try:
        hashed_password = bcrypt.generate_password_hash(password=data["password"])
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password
        )
        new_user.save()
        return {"message": "user successfully saved"}, 201
    except Exception as e:
        print(f"This is the cause: {e}")


def login_user(data):
    user = User.objects(name=data["name"]).first()
    print(user.id)
    password_is_correct = bcrypt.check_password_hash(user["password"], data["password"])
    try:
        if not user or not password_is_correct:
            return jsonify({"error": 'Invalid Credentials'}), 401

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 201
    except Exception as e:
        print(f"This is the cause: {e}")



