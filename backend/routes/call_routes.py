from flask import Blueprint, jsonify
from controllers.call_logs_controller import get_call_logs
from controllers.call_controller import (
    make_call, 
    end_call, 
    voice_connect,
    recording_callback,
    status_callback
)
from controllers.call_upload_controller import upload_call
from controllers.call_controller import get_recordings

call_bp = Blueprint("call", __name__)

call_bp.route("/dial", methods=["POST"])(make_call)
call_bp.route("/end", methods=["POST"])(end_call)
call_bp.route("/voice", methods=["GET", "POST"])(voice_connect)
call_bp.route("/recording", methods=["POST"])(recording_callback)  # ✅ NEW
call_bp.route("/status", methods=["POST"])(status_callback)  # ✅ NEW
call_bp.route("/upload", methods=["POST"])(upload_call)
call_bp.route("/recordings", methods=["GET"])(get_recordings)
@call_bp.route("/uploads/results", methods=["GET"])
def call_logs():
    return jsonify(get_call_logs())