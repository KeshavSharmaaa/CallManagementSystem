from flask import request
from flask_socketio import emit, join_room, leave_room
from config.db import calls
from datetime import datetime
import uuid

# Store active calls and user mappings
active_calls = {}
phone_to_socket = {}  # ✅ Map phone numbers to socket IDs

def handle_connect():
    """Handle new WebSocket connection"""
    print(f"✅ Client connected: {request.sid}")
    emit('connected', {'socketId': request.sid})


def handle_disconnect():
    """Handle WebSocket disconnection"""
    print(f"❌ Client disconnected: {request.sid}")
    
    # Remove from phone mapping
    for phone, sid in list(phone_to_socket.items()):
        if sid == request.sid:
            del phone_to_socket[phone]
    
    # Clean up any active calls
    for call_id, call_data in list(active_calls.items()):
        if call_data.get('caller') == request.sid or call_data.get('receiver') == request.sid:
            del active_calls[call_id]


def register_user(data):
    """Register user with their phone number"""
    phone = data.get('phone')
    user_type = data.get('userType')
    
    # ✅ Store phone to socket mapping
    phone_to_socket[phone] = request.sid
    
    print(f"📝 Registered: {phone} as {user_type} (Socket: {request.sid})")
    
    emit('registered', {
        'phone': phone,
        'socketId': request.sid,
        'userType': user_type
    })


def initiate_call(data):
    """Initiate a call to another user"""
    caller_phone = data.get('callerPhone')
    receiver_phone = data.get('receiverPhone')
    salesperson_id = data.get('salespersonId')
    
    # Create unique call ID
    call_id = f"CALL_{uuid.uuid4().hex[:16]}"
    
    # ✅ Get receiver's socket ID
    receiver_socket = phone_to_socket.get(receiver_phone)
    
    if not receiver_socket:
        print(f"❌ Receiver {receiver_phone} not found online")
        emit('call_failed', {
            'reason': 'Receiver not online',
            'receiverPhone': receiver_phone
        })
        return
    
    # Store call info
    active_calls[call_id] = {
        'callId': call_id,
        'caller': request.sid,
        'receiver': receiver_socket,  # ✅ Store receiver socket
        'callerPhone': caller_phone,
        'receiverPhone': receiver_phone,
        'salespersonId': salesperson_id,
        'startTime': datetime.utcnow(),
        'status': 'initiating'
    }
    
    print(f"📞 Call initiated: {caller_phone} → {receiver_phone}")
    print(f"   Caller socket: {request.sid}")
    print(f"   Receiver socket: {receiver_socket}")
    
    # Both join the call room
    join_room(call_id)
    join_room(call_id, sid=receiver_socket)  # ✅ Add receiver to room
    
    # Notify caller
    emit('call_initiated', {
        'callId': call_id,
        'receiverPhone': receiver_phone
    })
    
    # ✅ Notify receiver directly using their socket ID
    emit('incoming_call', {
        'callId': call_id,
        'callerPhone': caller_phone,
        'caller': request.sid
    }, to=receiver_socket)  # Send to specific socket
    
    print(f"✅ Sent incoming_call to receiver: {receiver_socket}")


def webrtc_offer(data):
    """Forward WebRTC offer to receiver"""
    call_id = data.get('callId')
    offer = data.get('offer')
    
    if call_id not in active_calls:
        print(f"❌ Call {call_id} not found")
        return
    
    receiver_socket = active_calls[call_id]['receiver']
    
    print(f"📤 Forwarding offer for call: {call_id}")
    print(f"   To receiver socket: {receiver_socket}")
    
    # ✅ Send directly to receiver
    emit('webrtc_offer', {
        'callId': call_id,
        'offer': offer,
        'from': request.sid
    }, to=receiver_socket)


def webrtc_answer(data):
    """Forward WebRTC answer to caller"""
    call_id = data.get('callId')
    answer = data.get('answer')
    
    if call_id not in active_calls:
        print(f"❌ Call {call_id} not found")
        return
    
    caller_socket = active_calls[call_id]['caller']
    
    print(f"📤 Forwarding answer for call: {call_id}")
    print(f"   To caller socket: {caller_socket}")
    
    # ✅ Send directly to caller
    emit('webrtc_answer', {
        'callId': call_id,
        'answer': answer,
        'from': request.sid
    }, to=caller_socket)


def webrtc_ice_candidate(data):
    """Forward ICE candidate"""
    call_id = data.get('callId')
    candidate = data.get('candidate')
    
    if call_id not in active_calls:
        return
    
    call_info = active_calls[call_id]
    
    # ✅ Forward to the other peer
    if request.sid == call_info['caller']:
        target = call_info['receiver']
    else:
        target = call_info['caller']
    
    emit('webrtc_ice_candidate', {
        'callId': call_id,
        'candidate': candidate,
        'from': request.sid
    }, to=target)


def end_call(data):
    """End the call and save to database"""
    call_id = data.get('callId')
    
    if call_id not in active_calls:
        print(f"❌ Call {call_id} not found for ending")
        return
    
    call_info = active_calls[call_id]
    
    # Calculate duration
    duration = int((datetime.utcnow() - call_info['startTime']).total_seconds())
    
    # Save to database
    calls.insert_one({
        'callSid': call_id,
        'salespersonId': call_info.get('salespersonId', 'unknown'),
        'agent': call_info['callerPhone'],
        'customer': call_info['receiverPhone'],
        'duration': duration,
        'outcome': 'connected',
        'status': 'completed',
        'createdAt': call_info['startTime'],
        'callType': 'webrtc'
    })
    
    print(f"✅ Call ended: {call_id}, Duration: {duration}s")
    
    # Notify both parties
    emit('call_ended', {
        'callId': call_id,
        'duration': duration
    }, room=call_id)
    
    # Clean up
    leave_room(call_id)
    if call_id in active_calls:
        del active_calls[call_id]