#!/usr/bin/env python3
"""
Real-Time Drawing Battle Game
Main Flask application with Socket.IO support
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import secrets
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Store active rooms and players
active_rooms = {}
connected_players = {}


@app.route('/')
def index():
    """Welcome screen for creating or joining rooms"""
    return render_template('index.html')


@app.route('/room/<room_code>')
def room(room_code):
    """Drawing room interface"""
    return render_template('room.html', room_code=room_code)


@socketio.event
def connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('status', {'msg': 'Connected to drawing server!'})


@socketio.event
def disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")
    # TODO: Remove player from room and notify others


@socketio.event
def create_room():
    """Create a new drawing room"""
    room_code = generate_room_code()
    active_rooms[room_code] = {
        'players': [],
        'created_by': request.sid,
        'canvas_state': []
    }
    logger.info(f"Room created: {room_code}")
    emit('room_created', {'room_code': room_code})


@socketio.event
def join_room_request(data):
    """Handle room join requests"""
    room_code = data.get('room_code', '').upper()
    
    if room_code not in active_rooms:
        emit('error', {'message': 'Room not found'})
        return
    
    # Add player to room
    join_room(room_code)
    player_info = {
        'id': request.sid,
        'joined_at': time.time()
    }
    active_rooms[room_code]['players'].append(player_info)
    connected_players[request.sid] = room_code
    
    logger.info(f"Player {request.sid} joined room {room_code}")
    
    # Send existing canvas state to the new player
    canvas_state = active_rooms[room_code]['canvas_state']
    if canvas_state:
        emit('canvas_state', {'strokes': canvas_state})
        logger.info(f"Sent {len(canvas_state)} existing strokes to new player in room {room_code}")
    
    # Notify player and room
    emit('room_joined', {'room_code': room_code})
    socketio.emit('player_joined', player_info, room=room_code)


@socketio.event
def drawing_data(data):
    """Handle real-time drawing data and broadcast to room"""
    room_code = data.get('room_code')
    if not room_code or room_code not in active_rooms:
        emit('error', {'message': 'Invalid room'})
        return
    
    # Store drawing stroke in room's canvas state for new joiners
    if data.get('type') in ['stroke_start', 'stroke_continue']:
        active_rooms[room_code]['canvas_state'].append(data)
    
    # Broadcast drawing data to all other players in the room (exclude sender)
    emit('drawing_data', data, room=room_code, include_self=False)
    logger.debug(f"Broadcasting drawing data to room {room_code}: {data.get('type')}")


@socketio.event
def clear_canvas(data):
    """Handle canvas clear and broadcast to room"""
    room_code = data.get('room_code')
    if not room_code or room_code not in active_rooms:
        emit('error', {'message': 'Invalid room'})
        return
    
    # Clear the stored canvas state
    active_rooms[room_code]['canvas_state'] = []
    
    # Broadcast canvas clear to all players in the room
    emit('canvas_cleared', {}, room=room_code)
    logger.info(f"Canvas cleared in room {room_code}")


@socketio.event
def test_message(data):
    """Test WebSocket messaging"""
    logger.info(f"Received test message: {data}")
    emit('test_response', {'message': f"Server received: {data.get('message', 'No message')}"})


def generate_room_code():
    """Generate a unique 6-character room code"""
    while True:
        code = secrets.token_urlsafe(4)[:6].upper()
        if code not in active_rooms:
            return code


if __name__ == '__main__':
    logger.info("Starting Real-Time Drawing Battle Game server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 