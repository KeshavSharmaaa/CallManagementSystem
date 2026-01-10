📞 Sales Management System (SalesMS)
SalesMS is a full-stack Sales and Call Management System designed to streamline sales operations by combining real-time calling, AI-based call analysis, manager dashboards, and secure data handling.
The system focuses on performance monitoring, lead management, and cybersecurity, ensuring that sensitive call data is processed, stored, and displayed in a secure and controlled manner.

🎯 Objectives of the Project
Enable managers to monitor sales calls and agent performance
Provide AI-generated insights from call recordings
Support real-time calling and signaling
Ensure strong cybersecurity and data protection
Build a scalable, modular, industry-style architecture

🚀 Key Features
👨‍💼 Manager Features
📊 Call Insights dashboard with AI metrics
👥 Agent performance tracking
📝 Lead assignment and monitoring
⚠️ Risk assessment per call
📜 Call transcripts and summaries
🎧 Calling System
📞 Real-time call initiation and termination
🔁 WebRTC-based signaling
☎️ Twilio integration for call handling
🎙️ Secure call recording upload

🧠 AI & Analytics
Speech-to-text transcription using Whisper
Engagement, effectiveness, and risk analysis
Structured JSON-based insights

🔐 Security
Token-based authentication
Secure API-only data access
Backend-only file storage
Protected real-time communication

🏗️ Technology Stack
Frontend
HTML5
CSS3 (Dark Mode UI)
Vanilla JavaScript
Font Awesome
Backend
Python (Flask)
Flask Blueprints
Flask-SocketIO
WebRTC
Twilio API
Whisper (Speech-to-Text)
dotenv
JSON-based storage (DB-ready)

📁 Project Structure
SalesManagementSystem/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── call_routes.py
│   │   ├── manager_routes.py
│   │   └── analytics_routes.py
│   ├── controllers/
│   │   ├── call_controller.py
│   │   ├── call_logs_controller.py
│   │   ├── call_upload_controller.py
│   │   ├── webrtc_controller.py
│   │   └── twilio_controller.py
│   ├── utils/
│   │   └── transcription.py
│   └── data/
│       └── call_logs/
│
├── frontend/
│   ├── manager/
│   │   ├── dashboard.html
│   │   ├── insight-calls.html
│   │   ├── dashboard.css
│   │   └── insight-calls.css
│   ├── js/
│   │   └── manager/
│   │       └── insightCalls.js
│   └── index.html
│
├── venv/
├── .env
└── README.md

⚙️ Installation & Setup
Backend Setup (Python 3.10 Recommended)
cd backend
python -m venv venv
venv\Scripts\activate
pip install flask flask-cors flask-socketio python-dotenv eventlet torch openai-whisper twilio
python app.py
Server runs at:
http://127.0.0.1:5000

🌐 Frontend Pages
Manager Dashboard
/manager/dashboard.html

Call Insights
/manager/insight-calls.html

🔗 Key API Endpoint
GET /api/call/manager/call-logs
Returns AI-processed call data including metrics, risk levels, and transcripts.

🔐 Cybersecurity & Data Protection During Calls
SalesMS follows security-by-design principles to ensure confidentiality, integrity, and availability of call data.

🛡️ Secure Architecture
Frontend handles display only
Backend controls data processing and storage
No direct access to server files from browser

🔑 Authentication & Authorization
Token-based authentication for protected pages
Unauthorized users are redirected or blocked
APIs validate access before returning sensitive data
🔒 Secure Calling (Twilio + WebRTC)
Twilio handles call routing securely
WebRTC manages real-time signaling
Socket.IO events are authenticated
Prevents call hijacking and spoofing

🎙️ Secure Recording & Upload
Call recordings uploaded via backend APIs only
Stored in protected backend directories
Not exposed via public URLs

🧠 Secure AI Processing
Audio processed server-side
Transcription and analysis isolated from frontend
Only summarized insights returned to UI

🚫 Attack Mitigation
Threat	Protection
Unauthorized access	Token-based auth
File leakage	Backend-only storage
Call hijacking	Authenticated signaling
Data tampering	API-only writes
XSS	Escaped transcript rendering
👥 Team Workflow & Role Distribution

The project followed a modular, role-based workflow, allowing parallel development and secure integration.

🎨 Frontend Team
👤 Karthik — UI/UX & Dashboard Design

Designed dark-mode dashboard layout
Built sidebar navigation and tables
Ensured UI consistency and responsiveness

Flow:
Design → Layout → Styling → Review

👤 Keshav — Frontend Logic & API Integration
Implemented frontend JavaScript
Integrated backend APIs
Handled authentication guards and data rendering

Flow:
API Contract → Fetch → Render → Debug

⚙️ Backend Team
👤 Chaitanya — Core Backend Architecture
Designed Flask architecture
Implemented Blueprints and REST APIs
Managed routing, CORS, and API structure

Flow:
Architecture → Routing → Controllers → Testing

👤 Dhruv — AI Processing & Call Analytics
Implemented Whisper transcription
Designed call analytics metrics
Processed recordings into structured insights

Flow:
Audio → Transcription → Analysis → JSON Output

🔗 Integration, Calling & Security Lead
👤 Parit — Twilio, WebRTC, Integration & Cybersecurity
Primary Responsibilities:
Implemented Twilio-based calling system
Integrated WebRTC signaling with Socket.IO
Managed end-to-end call lifecycle
Integrated all backend modules
Enforced cybersecurity across the system

Key Contributions:
Twilio call handling and routing
WebRTC signaling logic
Secure call upload pipeline
Backend integration of all modules
Cybersecurity enforcement

Flow:
Calling System → Integration → Security Validation → Deployment Testing

🔄 End-to-End System Flow
UI Design (Karthik)
      ↓
Frontend Logic & API Calls (Keshav)
      ↓
REST APIs & Routing (Chaitanya)
      ↓
Calling System (Twilio + WebRTC) (Parit)
      ↓
AI Transcription & Analysis (Dhruv)
      ↓
Secure Storage & Integration (Parit)
      ↓
Insights Dashboard (Karthik + Keshav)

Features

1️⃣ ML-Based Behavioral Modeling (Natural Evolution)
As historical call data grows, rule-based signals can be complemented with ML models.
Models can learn:
Normal behavior baselines per salesperson
Subtle deviations over time
Early indicators of performance decline or misuse
This improves accuracy without sacrificing explainability.
👉 Key point: ML is introduced only when data justifies it.

2️⃣ Speech & NLP Intelligence on Transcripts
Transcripts can be analyzed for:
Conversation completeness
Keyword relevance
Objection handling patterns
This enables content-aware quality analysis, not just metadata analysis.
👉 Useful for coaching, not surveillance.

3️⃣ Predictive Follow-Up & Conversion Forecasting
Using timestamps and follow-up history, the system can:
Predict which leads need immediate attention
Estimate conversion probability based on behavior patterns
Managers can prioritize high-impact follow-ups.

4️⃣ Organization-Level Risk & Integrity Dashboard
Extend analysis from individuals to teams:
Team-level risk trends
Regional behavior anomalies
Sudden organization-wide pattern shifts
Useful for compliance, audits, and leadership oversight.

5️⃣ Policy-Driven Automated Interventions
Convert insights into automated actions, such as:
Mandatory review for repeated high-risk behavior
Coaching recommendations
Temporary call restrictions for extreme misuse cases
Reduces manual managerial workload.

6️⃣ Integration with CRM & Enterprise Systems
Integrate with existing CRM tools to:
Correlate call behavior with actual revenue outcomes
Improve forecasting accuracy
Makes the system part of the core sales infrastructure.

7️⃣ Broader Cybersecurity Applications
The same framework can be adapted to other domains involving internal activity:
Customer support centers
Financial advisory calls
Healthcare teleconsultations
Any environment where internal misuse and accountability matter.

📌 Conclusion
SalesMS demonstrates a secure, scalable, and real-world sales intelligence system by combining:
Real-time calling
AI-driven analytics
Modular backend architecture
Strong cybersecurity practices
Clear team collaboration
The project reflects industry-standard design principles suitable for enterprise-grade applications.

📜 License
This project is intended for academic and educational use.
It may be extended or adapted for future enhancements.
