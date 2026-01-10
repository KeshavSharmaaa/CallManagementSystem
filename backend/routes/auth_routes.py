from flask import Blueprint
from controllers.auth_controller import login, register_manager, register_salesperson

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/register/manager", methods=["POST"])(register_manager)
auth_bp.route("/register/salesperson", methods=["POST"])(register_salesperson)
