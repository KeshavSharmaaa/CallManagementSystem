from flask import Blueprint
from controllers.call_upload_controller import upload_call

call_upload_bp = Blueprint("call_upload", __name__)

call_upload_bp.route("/upload", methods=["POST"])(upload_call)