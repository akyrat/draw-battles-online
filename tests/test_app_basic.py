"""
Basic Flask application tests
Testing routes and basic functionality
"""
import pytest


class TestBasicRoutes:
    """Test basic Flask routes"""

    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Drawing Battle' in response.data or b'Create Room' in response.data

    def test_room_page_loads(self, client):
        """Test that room pages load with room code"""
        response = client.get('/room/TEST01')
        assert response.status_code == 200
        assert b'TEST01' in response.data
        assert b'drawing-canvas' in response.data

    def test_room_page_contains_required_elements(self, client):
        """Test that room page contains all required elements"""
        response = client.get('/room/ABCDEF')
        content = response.data.decode()
        
        # Check for essential HTML elements
        assert 'drawing-canvas' in content
        assert 'brush-size' in content
        assert 'color-picker' in content
        assert 'clear-canvas-btn' in content
        assert 'players-list' in content
        assert 'ABCDEF' in content  # Room code should be displayed


class TestHelperFunctions:
    """Test utility functions"""

    def test_generate_room_code_format(self):
        """Test that room codes are generated in correct format"""
        from app import generate_room_code
        
        code = generate_room_code()
        
        # Should be 6 characters, uppercase, URL-safe characters (alphanumeric + underscore/dash)
        assert len(code) == 6
        assert code.isupper()
        # URL-safe characters include A-Z, 0-9, underscore, and dash
        assert all(c.isalnum() or c in ['_', '-'] for c in code)

    def test_generate_room_code_uniqueness(self, clean_rooms):
        """Test that multiple room codes are unique"""
        from app import generate_room_code
        
        codes = [generate_room_code() for _ in range(10)]
        
        # All codes should be unique
        assert len(set(codes)) == 10 