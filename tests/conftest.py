"""
Pytest configuration and shared fixtures for testing
"""
import pytest
from app import app, socketio, active_rooms, connected_players


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def socket_client():
    """Create a test client for SocketIO"""
    socket_client = socketio.test_client(app)
    yield socket_client
    socket_client.disconnect()


@pytest.fixture
def clean_rooms():
    """Clean up rooms before and after each test"""
    active_rooms.clear()
    connected_players.clear()
    yield
    active_rooms.clear()
    connected_players.clear()


@pytest.fixture
def sample_room():
    """Create a sample room for testing"""
    room_code = "TEST01"
    active_rooms[room_code] = {
        'players': [],
        'created_by': 'test_sid',
        'canvas_state': []
    }
    return room_code 