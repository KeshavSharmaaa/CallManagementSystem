from flask import Blueprint
from controllers.manager_controller import assign_lead
from middleware.auth_middleware import token_required

manager_bp = Blueprint("manager", __name__)

manager_bp.route("/assign-lead", methods=["POST"])(
    token_required("manager")(assign_lead)
)
