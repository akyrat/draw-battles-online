"""
Integration tests
Testing complete workflows and multi-user scenarios
"""
import pytest
import time
from app import active_rooms


class TestCompleteGameFlow:
    """Test complete game workflows from start to finish"""

    def test_room_creation_to_drawing_workflow(self, clean_rooms):
        """Test complete workflow: create room -> join -> draw -> new player joins -> sees drawing"""
        from app import socketio, app
        
        # Step 1: Create room
        creator = socketio.test_client(app)
        creator.emit('create_room')
        
        received = creator.get_received()
        room_created_event = None
        for event in received:
            if event['name'] == 'room_created':
                room_created_event = event
                break
        
        assert room_created_event is not None
        room_code = room_created_event['args'][0]['room_code']
        
        # Step 2: Creator joins their own room
        creator.emit('join_room_request', {'room_code': room_code})
        creator.get_received()  # Clear events
        
        # Step 3: Creator draws something
        drawing_strokes = [
            {
                'room_code': room_code,
                'type': 'stroke_start',
                'x': 10,
                'y': 10,
                'color': '#000000',
                'size': 3
            },
            {
                'room_code': room_code,
                'type': 'stroke_continue',
                'x': 20,
                'y': 20,
                'lastX': 10,
                'lastY': 10,
                'color': '#000000',
                'size': 3
            },
            {
                'room_code': room_code,
                'type': 'stroke_continue',
                'x': 30,
                'y': 30,
                'lastX': 20,
                'lastY': 20,
                'color': '#000000',
                'size': 3
            }
        ]
        
        for stroke in drawing_strokes:
            creator.emit('drawing_data', stroke)
        
        # Step 4: New player joins
        joiner = socketio.test_client(app)
        joiner.emit('join_room_request', {'room_code': room_code})
        
        # Step 5: Verify new player receives canvas state
        received = joiner.get_received()
        canvas_state_event = None
        for event in received:
            if event['name'] == 'canvas_state':
                canvas_state_event = event
                break
        
        assert canvas_state_event is not None
        strokes = canvas_state_event['args'][0]['strokes']
        assert len(strokes) == 3
        
        # Verify stroke data
        assert strokes[0]['type'] == 'stroke_start'
        assert strokes[1]['type'] == 'stroke_continue'
        assert strokes[2]['type'] == 'stroke_continue'
        
        # Step 6: New player draws, creator should see it
        creator.get_received()  # Clear creator's events
        
        new_stroke = {
            'room_code': room_code,
            'type': 'stroke_continue',
            'x': 100,
            'y': 100,
            'lastX': 90,
            'lastY': 90,
            'color': '#FF0000',
            'size': 5
        }
        joiner.emit('drawing_data', new_stroke)
        
        # Creator should receive the new stroke
        creator_received = creator.get_received()
        drawing_events = [e for e in creator_received if e['name'] == 'drawing_data']
        assert len(drawing_events) == 1
        assert drawing_events[0]['args'][0]['color'] == '#FF0000'
        
        creator.disconnect()
        joiner.disconnect()

    def test_multi_player_real_time_drawing(self, sample_room, clean_rooms):
        """Test real-time drawing with multiple players"""
        from app import socketio, app
        
        room_code = sample_room
        
        # Create 3 players
        players = []
        for i in range(3):
            client = socketio.test_client(app)
            client.emit('join_room_request', {'room_code': room_code})
            players.append(client)
        
        # Clear all join events
        for player in players:
            player.get_received()
        
        # Player 1 draws
        drawing_data = {
            'room_code': room_code,
            'type': 'stroke_continue',
            'x': 50,
            'y': 50,
            'color': '#00FF00',
            'size': 4
        }
        players[0].emit('drawing_data', drawing_data)
        
        # Players 2 and 3 should receive the drawing data
        for i in [1, 2]:
            received = players[i].get_received()
            drawing_events = [e for e in received if e['name'] == 'drawing_data']
            assert len(drawing_events) == 1
            assert drawing_events[0]['args'][0]['color'] == '#00FF00'
        
        # Player 1 should NOT receive its own drawing data
        player1_received = players[0].get_received()
        player1_drawing_events = [e for e in player1_received if e['name'] == 'drawing_data']
        assert len(player1_drawing_events) == 0
        
        # Clean up
        for player in players:
            player.disconnect()

    def test_canvas_clear_multi_player(self, sample_room, clean_rooms):
        """Test canvas clearing with multiple players"""
        from app import socketio, app
        
        room_code = sample_room
        
        # Create 2 players
        player1 = socketio.test_client(app)
        player2 = socketio.test_client(app)
        
        player1.emit('join_room_request', {'room_code': room_code})
        player2.emit('join_room_request', {'room_code': room_code})
        
        # Both players draw
        for i, player in enumerate([player1, player2]):
            drawing_data = {
                'room_code': room_code,
                'type': 'stroke_continue',
                'x': 50 + i * 10,
                'y': 50 + i * 10,
                'color': ['#FF0000', '#0000FF'][i],
                'size': 3
            }
            player.emit('drawing_data', drawing_data)
        
        # Verify canvas has data
        assert len(active_rooms[room_code]['canvas_state']) == 2
        
        # Clear events
        player1.get_received()
        player2.get_received()
        
        # Player 1 clears canvas
        player1.emit('clear_canvas', {'room_code': room_code})
        
        # Verify canvas state is cleared
        assert len(active_rooms[room_code]['canvas_state']) == 0
        
        # Both players should receive clear event
        p1_received = player1.get_received()
        p2_received = player2.get_received()
        
        p1_clear_events = [e for e in p1_received if e['name'] == 'canvas_cleared']
        p2_clear_events = [e for e in p2_received if e['name'] == 'canvas_cleared']
        
        assert len(p1_clear_events) == 1
        assert len(p2_clear_events) == 1
        
        player1.disconnect()
        player2.disconnect()


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_drawing_without_joining_room(self, socket_client, clean_rooms):
        """Test sending drawing data without joining a room"""
        # Try to send drawing data without being in a room
        drawing_data = {
            'room_code': 'NOTJOINED',
            'type': 'stroke_continue',
            'x': 50,
            'y': 50
        }
        socket_client.emit('drawing_data', drawing_data)
        
        # Should receive error
        received = socket_client.get_received()
        error_events = [e for e in received if e['name'] == 'error']
        assert len(error_events) == 1

    def test_clear_canvas_without_permission(self, clean_rooms):
        """Test clearing canvas from a client not in the room"""
        from app import socketio, app
        
        # Create a room with one player
        room_code = "TEST01"
        active_rooms[room_code] = {
            'players': [{'id': 'other_player', 'joined_at': time.time()}],
            'created_by': 'other_player',
            'canvas_state': [{'type': 'stroke_continue', 'x': 10, 'y': 10}]
        }
        
        # Different client tries to clear
        client = socketio.test_client(app)
        client.emit('clear_canvas', {'room_code': room_code})
        
        # Should receive error (client not in room)
        received = client.get_received()
        error_events = [e for e in received if e['name'] == 'error']
        assert len(error_events) == 1
        
        # Canvas state should remain unchanged
        assert len(active_rooms[room_code]['canvas_state']) == 1
        
        client.disconnect()

    def test_malformed_drawing_data(self, socket_client, sample_room, clean_rooms):
        """Test handling malformed drawing data"""
        room_code = sample_room
        socket_client.emit('join_room_request', {'room_code': room_code})
        socket_client.get_received()  # Clear events
        
        # Send malformed data (missing required fields)
        malformed_data = {
            'room_code': room_code,
            # Missing type, coordinates, etc.
        }
        socket_client.emit('drawing_data', malformed_data)
        
        # Should not crash the server
        # Canvas state should not be corrupted
        canvas_state = active_rooms[room_code]['canvas_state']
        assert isinstance(canvas_state, list)


class TestPerformanceAndLoad:
    """Test performance aspects and load handling"""

    def test_rapid_drawing_strokes(self, sample_room, clean_rooms):
        """Test handling rapid succession of drawing strokes"""
        from app import socketio, app
        
        room_code = sample_room
        client = socketio.test_client(app)
        client.emit('join_room_request', {'room_code': room_code})
        client.get_received()  # Clear events
        
        # Send many rapid strokes
        num_strokes = 50
        for i in range(num_strokes):
            drawing_data = {
                'room_code': room_code,
                'type': 'stroke_continue',
                'x': i,
                'y': i,
                'lastX': i-1 if i > 0 else 0,
                'lastY': i-1 if i > 0 else 0,
                'color': '#000000',
                'size': 3
            }
            client.emit('drawing_data', drawing_data)
        
        # All strokes should be stored
        canvas_state = active_rooms[room_code]['canvas_state']
        assert len(canvas_state) == num_strokes
        
        # Verify data integrity
        for i, stroke in enumerate(canvas_state):
            assert stroke['x'] == i
            assert stroke['y'] == i
        
        client.disconnect()

    def test_canvas_state_size_limit(self, sample_room, clean_rooms):
        """Test canvas state doesn't grow indefinitely (future consideration)"""
        # This test documents expected behavior for future optimization
        room_code = sample_room
        canvas_state = active_rooms[room_code]['canvas_state']
        
        # For now, we just verify the list exists and can grow
        # In the future, we might want to implement size limits
        initial_length = len(canvas_state)
        assert isinstance(canvas_state, list)
        assert initial_length == 0 