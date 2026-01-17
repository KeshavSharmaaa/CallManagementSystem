from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from flask_socketio import SocketIO
import os

# ---------------- ROUTES ----------------
from routes.auth_routes import auth_bp
from routes.manager_routes import manager_bp
from routes.call_routes import call_bp
from routes.followup_routes import followup_bp
from routes.lead_routes import lead_bp
from routes.analytics_routes import analytics_bp
from routes.call_insights_routes import call_insights_bp

# ---------------- WEBRTC ----------------
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

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

# ---------------- APP INIT ----------------
app = Flask(__name__)

# ✅ CORS (frontend hosted separately)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ✅ Socket.IO (Render-safe)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# =====================================================
# ✅ API ROUTES (REGISTER FIRST)
# =====================================================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(manager_bp, url_prefix="/api/manager")
app.register_blueprint(call_insights_bp, url_prefix="/api/manager")
app.register_blueprint(call_bp, url_prefix="/api/call")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(followup_bp, url_prefix="/api/followup")
app.register_blueprint(lead_bp, url_prefix="/api/lead")

# =====================================================
# 🔌 SOCKET EVENTS
# =====================================================
socketio.on_event("connect", handle_connect)
socketio.on_event("disconnect", handle_disconnect)
socketio.on_event("register", register_user)
socketio.on_event("initiate_call", initiate_call)
socketio.on_event("webrtc_offer", webrtc_offer)
socketio.on_event("webrtc_answer", webrtc_answer)
socketio.on_event("webrtc_ice_candidate", webrtc_ice_candidate)
socketio.on_event("end_call", end_call)

# =====================================================
# 🌐 FRONTEND FILE SERVING (NO templates/static)
# =====================================================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/manager/<path:page>")
def serve_manager_pages(page):
    path = os.path.join(FRONTEND_DIR, "manager", page)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(os.path.join(FRONTEND_DIR, "manager"), page)

@app.route("/salesperson/<path:page>")
def serve_salesperson_pages(page):
    path = os.path.join(FRONTEND_DIR, "salesperson", page)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(os.path.join(FRONTEND_DIR, "salesperson"), page)

@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    path = os.path.join(UPLOADS_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(UPLOADS_DIR, filename)

@app.route("/<path:filename>")
def serve_static_files(filename):
    path = os.path.join(FRONTEND_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(FRONTEND_DIR, filename)

# =====================================================
# 🚀 RUN
# =====================================================
if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",   # ✅ REQUIRED for deployment
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
