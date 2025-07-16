"""
Room management tests
Testing room creation, joining, and player management
"""
import pytest
from app import active_rooms, connected_players


class TestRoomCreation:
    """Test room creation functionality"""

    def test_create_room_success(self, socket_client, clean_rooms):
        """Test successful room creation"""
        # Request room creation
        socket_client.emit('create_room')
        
        # Should receive room_created event
        received = socket_client.get_received()
        assert len(received) > 0
        
        # Find the room_created event
        room_created_event = None
        for event in received:
            if event['name'] == 'room_created':
                room_created_event = event
                break
        
        assert room_created_event is not None
        room_code = room_created_event['args'][0]['room_code']
        
        # Room should exist in active_rooms
        assert room_code in active_rooms
        assert active_rooms[room_code]['players'] == []
        assert active_rooms[room_code]['canvas_state'] == []

    def test_create_multiple_rooms(self, clean_rooms):
        """Test creating multiple rooms generates unique codes"""
        from app import socketio, app
        
        # Create multiple clients and rooms
        room_codes = []
        for i in range(5):
            socket_client = socketio.test_client(app)
            socket_client.emit('create_room')
            received = socket_client.get_received()
            
            for event in received:
                if event['name'] == 'room_created':
                    room_codes.append(event['args'][0]['room_code'])
            
            socket_client.disconnect()
        
        # All room codes should be unique
        assert len(set(room_codes)) == 5


class TestRoomJoining:
    """Test room joining functionality"""

    def test_join_existing_room(self, socket_client, sample_room, clean_rooms):
        """Test successfully joining an existing room"""
        room_code = sample_room
        
        # Join the room
        socket_client.emit('join_room_request', {'room_code': room_code})
        
        # Should receive room_joined event
        received = socket_client.get_received()
        room_joined_event = None
        for event in received:
            if event['name'] == 'room_joined':
                room_joined_event = event
                break
        
        assert room_joined_event is not None
        assert room_joined_event['args'][0]['room_code'] == room_code
        
        # Player should be added to room
        assert len(active_rooms[room_code]['players']) == 1
        
        # Player should be in connected_players
        assert socket_client.sid in connected_players
        assert connected_players[socket_client.sid] == room_code

    def test_join_nonexistent_room(self, socket_client, clean_rooms):
        """Test joining a room that doesn't exist"""
        # Try to join non-existent room
        socket_client.emit('join_room_request', {'room_code': 'NOTEXIST'})
        
        # Should receive error event
        received = socket_client.get_received()
        error_event = None
        for event in received:
            if event['name'] == 'error':
                error_event = event
                break
        
        assert error_event is not None
        assert 'not found' in error_event['args'][0]['message'].lower()

    def test_join_room_case_insensitive(self, socket_client, sample_room, clean_rooms):
        """Test that room codes are case insensitive"""
        room_code = sample_room.upper()
        
        # Join with lowercase code
        socket_client.emit('join_room_request', {'room_code': room_code.lower()})
        
        received = socket_client.get_received()
        room_joined_event = None
        for event in received:
            if event['name'] == 'room_joined':
                room_joined_event = event
                break
        
        assert room_joined_event is not None

    def test_multiple_players_join_room(self, sample_room, clean_rooms):
        """Test multiple players joining the same room"""
        from app import socketio, app
        
        room_code = sample_room
        clients = []
        
        # Create 3 clients and join the same room
        for i in range(3):
            client = socketio.test_client(app)
            client.emit('join_room_request', {'room_code': room_code})
            clients.append(client)
        
        # All players should be in the room
        assert len(active_rooms[room_code]['players']) == 3
        
        # Clean up
        for client in clients:
            client.disconnect()


class TestPlayerTracking:
    """Test player tracking and room state management"""

    def test_player_info_stored_correctly(self, socket_client, sample_room, clean_rooms):
        """Test that player information is stored correctly"""
        room_code = sample_room
        
        socket_client.emit('join_room_request', {'room_code': room_code})
        
        # Check player info in room
        players = active_rooms[room_code]['players']
        assert len(players) == 1
        
        player = players[0]
        assert 'id' in player
        assert 'joined_at' in player
        assert player['id'] == socket_client.sid
        assert isinstance(player['joined_at'], (int, float)) 