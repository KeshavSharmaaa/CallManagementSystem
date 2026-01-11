import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from flask import request, jsonify
from config.db import managers, salespersons

# ==============================
# CONFIG
# ==============================

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret")
JWT_ALGO = "HS256"
TOKEN_EXP_HOURS = 8


# ==============================
# REGISTER MANAGER
# ==============================

def register_manager():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    if managers.find_one({"email": data["email"]}):
        return jsonify({"message": "Manager already exists"}), 409

    hashed_password = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    managers.insert_one({
        "name": data.get("name", ""),
        "email": data["email"],
        "password": hashed_password,
        "role": "manager",
        "createdAt": datetime.utcnow()
    })

    return jsonify({"message": "Manager registered successfully"}), 201


# ==============================
# REGISTER SALESPERSON
# ==============================

def register_salesperson():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    if salespersons.find_one({"email": data["email"]}):
        return jsonify({"message": "Salesperson already exists"}), 409

    hashed_password = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    salespersons.insert_one({
        "name": data.get("name", ""),
        "email": data["email"],
        "password": hashed_password,
        "role": "salesperson",
        "managerId": data.get("managerId"),
        "createdAt": datetime.utcnow()
    })

    return jsonify({"message": "Salesperson registered successfully"}), 201


# ==============================
# LOGIN
# ==============================

def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    user = managers.find_one({"email": data["email"]}) \
        or salespersons.find_one({"email": data["email"]})

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user["password"]
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "id": str(user["_id"]),
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXP_HOURS)
        },
        JWT_SECRET,
        algorithm=JWT_ALGO
    )

    return jsonify({
        "token": token,
        "role": user["role"],
        "id": str(user["_id"])
    }), 200
