import jwt
import os
from datetime import datetime, timedelta, timezone


SECRET_KEY = os.getenv("JWT_SECRET")


# Generate access token
def create_access_token(user_identity):
    payload = {
        "user_identity": user_identity,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "type": "access"
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return encoded_jwt


def create_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "type": "refresh"
    }

    refresh_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return refresh_jwt


def decode_token(token, token_type):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        if decoded_payload.get("type") != token_type:
            raise jwt.InvalidTokenError("Invalid Token Type")
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return {"message": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"message": "Invalid Token"}



