from flask import Blueprint
from controllers.followup_controller import add_followup, complete_followup
from middleware.auth_middleware import token_required

followup_bp = Blueprint("followup", __name__)

followup_bp.route("/add", methods=["POST"])(
    token_required("salesperson")(add_followup)
)

followup_bp.route("/complete", methods=["POST"])(
    token_required("salesperson")(complete_followup)
)