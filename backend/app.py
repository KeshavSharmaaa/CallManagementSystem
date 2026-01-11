from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import os

from routes.auth_routes import auth_bp
from routes.manager_routes import manager_bp
from routes.call_routes import call_bp
from routes.followup_routes import followup_bp
from routes.lead_routes import lead_bp
from routes.analytics_routes import analytics_bp
from routes.call_upload_routes import call_upload_bp

# Import WebRTC handlers
from controllers.webrtc_controller import (
    handle_connect,
    handle_disconnect,
    register_user,
    initiate_call,
    webrtc_offer,
    webrtc_answer,
    webrtc_ice_candidate,
    end_call
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# API routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(manager_bp, url_prefix="/api/manager")
app.register_blueprint(call_bp, url_prefix="/api/call")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(followup_bp, url_prefix="/api/followup")
app.register_blueprint(lead_bp, url_prefix="/api/lead")
app.register_blueprint(call_upload_bp, url_prefix="/api/call")

# WebSocket event handlers
socketio.on_event('connect', handle_connect)
socketio.on_event('disconnect', handle_disconnect)
socketio.on_event('register', register_user)
socketio.on_event('initiate_call', initiate_call)
socketio.on_event('webrtc_offer', webrtc_offer)
socketio.on_event('webrtc_answer', webrtc_answer)
socketio.on_event('webrtc_ice_candidate', webrtc_ice_candidate)
socketio.on_event('end_call', end_call)

# ✅ Serve frontend files
@app.route("/")
def home():
    """Serve index.html from frontend folder"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route("/<path:filename>")
def serve_static(filename):
    """Serve any other file from frontend folder (CSS, JS, HTML, etc.)"""
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    return send_from_directory(frontend_path, filename)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)