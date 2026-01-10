import jwt
import os
from flask import request, jsonify
from functools import wraps

JWT_SECRET = os.getenv("JWT_SECRET")

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"message": "Token missing"}), 401

            try:
                user = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                if role and user["role"] != role:
                    return jsonify({"message": "Unauthorized"}), 403
            except:
                return jsonify({"message": "Invalid token"}), 401

            return f(user, *args, **kwargs)
        return wrapper
    return decorator
