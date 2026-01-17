import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from flask import request, jsonify
from config.db import managers, salespersons

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")  # fallback for dev

def register_manager():
    data = request.json

    password = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    )

    managers.insert_one({
        "name": data.get("name", ""),        # ✅ FIX
        "email": data["email"],
        "password": password,
        "role": "manager"
    })

    return jsonify({"message": "Manager registered"}), 201


def register_salesperson():
    data = request.json

    password = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    )

    salespersons.insert_one({
        "name": data.get("name", ""),        # ✅ FIX
        "email": data["email"],
        "password": password,
        "role": "salesperson",
        "managerId": data.get("managerId")   # ✅ optional
    })

    return jsonify({"message": "Salesperson registered"}), 201


def login():
    data = request.json

    user = managers.find_one({"email": data["email"]}) or \
           salespersons.find_one({"email": data["email"]})

    if not user or not bcrypt.checkpw(
        data["password"].encode(),
        user["password"]
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode({
        "id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=8)
    }, JWT_SECRET, algorithm="HS256")

    return jsonify({
        "token": token,
        "role": user["role"],
        "id": str(user["_id"])
    })
