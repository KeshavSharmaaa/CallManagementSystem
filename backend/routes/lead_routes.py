from flask import Blueprint
from controllers.lead_controller import update_lead_status
from middleware.auth_middleware import token_required

lead_bp = Blueprint("lead", __name__)

lead_bp.route("/update-status", methods=["POST"])(
    token_required("salesperson")(update_lead_status)
)
