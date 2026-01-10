from flask import Blueprint
from controllers.analytics_controller import manager_analytics
from middleware.auth_middleware import token_required
from controllers.analytics_controller import missed_followups
from controllers.analytics_controller import salesperson_performance

analytics_bp = Blueprint("analytics", __name__)

analytics_bp.route("/manager", methods=["GET"])(
    token_required("manager")(manager_analytics)
)

analytics_bp.route("/missed-followups", methods=["GET"])(
    token_required("manager")(missed_followups)
)

analytics_bp.route("/salesperson-performance", methods=["GET"])(
    token_required("manager")(salesperson_performance)
)