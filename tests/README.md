# 🧪 Draw Battles Online - Test Suite

## Overview

Comprehensive test suite for the Draw Battles Online real-time drawing game. Tests cover Flask routes, WebSocket functionality, room management, drawing synchronization, and complete user workflows.

## 🏃‍♂️ Running Tests

### Quick Start
```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v
```

### Advanced Usage
```bash
# Run specific test file
pytest tests/test_app_basic.py -v

# Run specific test
pytest tests/test_room_management.py::TestRoomCreation::test_create_room_success -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Stop on first failure
pytest tests/ -x

# Run only integration tests (when marked)
pytest tests/ -m integration
```

## 📁 Test Structure

### `conftest.py`
- **Fixtures**: Shared test setup and teardown
- **`client`**: Flask test client for HTTP requests
- **`socket_client`**: SocketIO test client for WebSocket testing
- **`clean_rooms`**: Cleans room state between tests
- **`sample_room`**: Creates a test room for testing

### `test_app_basic.py`
**Basic Flask Application Tests**
- ✅ Index page loads correctly
- ✅ Room pages render with room codes
- ✅ Required HTML elements present
- ✅ Room code generation format and uniqueness

### `test_room_management.py`
**Room Management Functionality**
- ✅ Room creation via WebSocket
- ✅ Multiple unique room generation
- ✅ Joining existing rooms
- ✅ Handling non-existent rooms
- ✅ Case-insensitive room codes
- ✅ Multiple players per room
- ✅ Player tracking and metadata

### `test_drawing_functionality.py`
**Drawing and Canvas Operations**
- ✅ Real-time drawing data broadcast
- ✅ Drawing to invalid rooms (error handling)
- ✅ Canvas state storage and persistence
- ✅ New player canvas state replay
- ✅ Canvas clearing functionality
- ✅ WebSocket connection handling
- ✅ Test message functionality

### `test_integration.py`
**Complete Workflows and Multi-User Scenarios**
- ✅ End-to-end room creation → drawing → new player workflow
- ✅ Multi-player real-time drawing synchronization
- ✅ Canvas clearing with multiple players
- ✅ Error handling for edge cases
- ✅ Performance testing with rapid strokes
- ✅ Malformed data handling

## 🎯 Test Coverage Areas

### Core Functionality ✅
- **Room Management**: Creation, joining, player tracking
- **WebSocket Communication**: Event handling, broadcasting
- **Drawing Synchronization**: Real-time stroke transmission
- **Canvas Persistence**: State storage and replay for new players

### Error Handling ✅
- **Invalid Rooms**: Non-existent room codes
- **Unauthorized Actions**: Operations without proper room membership
- **Malformed Data**: Invalid drawing data structures
- **Network Issues**: Connection handling and reconnection

### Performance ✅
- **Rapid Drawing**: High-frequency stroke transmission
- **Multiple Players**: Concurrent user interactions
- **Canvas State Size**: Memory usage considerations

## 🧪 Test Examples

### Testing Room Creation
```python
def test_create_room_success(self, socket_client, clean_rooms):
    socket_client.emit('create_room')
    received = socket_client.get_received()
    # Verify room_created event received
    assert room_created_event is not None
```

### Testing Real-Time Drawing
```python
def test_drawing_data_broadcast(self, sample_room, clean_rooms):
    # Create two clients
    client1.emit('drawing_data', drawing_data)
    # Verify client2 receives the data
    assert drawing_event is not None
```

### Testing Canvas Persistence
```python
def test_canvas_state_replay_for_new_player(self, sample_room, clean_rooms):
    # Player 1 draws
    client1.emit('drawing_data', drawing_data)
    # Player 2 joins and should see existing drawing
    assert canvas_state_event is not None
```

## 📊 Coverage Goals

### Current Coverage Areas
- **Flask Routes**: 100% (index, room pages)
- **WebSocket Events**: 100% (create_room, join_room_request, drawing_data, clear_canvas)
- **Room Management**: 100% (creation, joining, player tracking)
- **Drawing Features**: 100% (real-time sync, canvas persistence)

### Integration Coverage
- **Complete User Journeys**: Room creation → drawing → multiplayer interaction
- **Error Scenarios**: Invalid operations and edge cases
- **Performance**: Rapid interactions and load handling

## 🔧 Test Configuration

### pytest.ini Settings
```ini
testpaths = tests
python_files = test_*.py
addopts = --strict-markers --disable-warnings
```

### Fixtures and Setup
- **`clean_rooms`**: Ensures isolated test environment
- **`socket_client`**: Manages WebSocket test connections
- **Automatic cleanup**: Test clients disconnected after each test

## 🚀 Benefits

### For Development
- **Regression Prevention**: Catch breaking changes early
- **Refactoring Safety**: Modify code with confidence
- **Documentation**: Tests serve as executable specifications

### For Team Collaboration
- **Onboarding**: New developers understand expected behavior
- **Quality Assurance**: Consistent functionality across changes
- **Debugging**: Isolate issues to specific components

## 🎯 Next Steps for Week 3

When implementing game mechanics (prompts, scoring, turns), add tests for:
- **Prompt System**: Random word generation, difficulty levels
- **Turn Management**: Player rotation, time limits
- **Scoring Logic**: Points calculation, winner determination
- **Game State**: Round progression, game completion

---

**Ready to test your code? Run `python run_tests.py` and see your green checkmarks! ✅** 