/**
 * Real-Time Drawing Application
 * Handles canvas drawing and WebSocket communication
 */

class DrawingApp {
    constructor(roomCode) {
        this.roomCode = roomCode;
        this.socket = io();
        this.isDrawing = false;
        this.lastX = 0;
        this.lastY = 0;
        
        this.initCanvas();
        this.initControls();
        this.initSocketEvents();
        this.joinRoom();
        
        console.log('DrawingApp initialized for room:', roomCode);
    }

    initCanvas() {
        this.canvas = document.getElementById('drawing-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Set initial drawing properties
        this.ctx.strokeStyle = '#000000';
        this.ctx.lineWidth = 3;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        
        // Bind canvas events
        this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
        this.canvas.addEventListener('mousemove', this.draw.bind(this));
        this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
        this.canvas.addEventListener('mouseout', this.stopDrawing.bind(this));
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchmove', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchend', this.stopDrawing.bind(this));
        
        console.log('Canvas initialized');
    }

    initControls() {
        // Brush size control
        this.brushSizeSlider = document.getElementById('brush-size');
        this.brushSizeValue = document.getElementById('brush-size-value');
        
        if (this.brushSizeSlider && this.brushSizeValue) {
            this.brushSizeSlider.addEventListener('input', (e) => {
                const size = e.target.value;
                this.ctx.lineWidth = size;
                this.brushSizeValue.textContent = size;
                console.log('Brush size changed to:', size);
            });
        } else {
            console.error('Brush size elements not found');
        }

        // Color picker
        this.colorPicker = document.getElementById('color-picker');
        if (this.colorPicker) {
            this.colorPicker.addEventListener('change', (e) => {
                this.ctx.strokeStyle = e.target.value;
            });
        }

        // Quick color buttons
        const colorButtons = document.querySelectorAll('.color-btn');
        colorButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const color = e.target.dataset.color;
                this.ctx.strokeStyle = color;
                if (this.colorPicker) {
                    this.colorPicker.value = color;
                }
            });
        });

        // Clear canvas button
        const clearBtn = document.getElementById('clear-canvas-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearCanvas();
            });
        }

        console.log('Controls initialized');
    }

    initSocketEvents() {
        this.socket.on('connect', () => {
            this.updateConnectionStatus('Connected', 'connected');
            console.log('Connected to server');
        });

        this.socket.on('disconnect', () => {
            this.updateConnectionStatus('Disconnected', 'disconnected');
            console.log('Disconnected from server');
        });

        this.socket.on('drawing_data', (data) => {
            this.receiveDrawingData(data);
        });

        this.socket.on('canvas_cleared', () => {
            this.clearCanvasLocal();
        });

        this.socket.on('player_joined', (player) => {
            this.addPlayerToList(player);
            this.showMessage(`Player joined the room`);
        });

        this.socket.on('player_left', (player) => {
            this.removePlayerFromList(player);
            this.showMessage(`Player left the room`);
        });

        this.socket.on('room_not_found', () => {
            alert('Room not found! Returning to home page.');
            window.location.href = '/';
        });

        this.socket.on('canvas_state', (data) => {
            this.replayCanvasState(data.strokes);
        });

        console.log('Socket events initialized');
    }

    joinRoom() {
        this.socket.emit('join_room_request', { room_code: this.roomCode });
        console.log('Joining room:', this.roomCode);
    }

    getCanvasCoordinates(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;
        
        return {
            x: (e.clientX - rect.left) * scaleX,
            y: (e.clientY - rect.top) * scaleY
        };
    }

    startDrawing(e) {
        this.isDrawing = true;
        const coords = this.getCanvasCoordinates(e);
        this.lastX = coords.x;
        this.lastY = coords.y;
        
        // Send stroke start event
        this.sendDrawingData({
            type: 'stroke_start',
            x: coords.x,
            y: coords.y,
            color: this.ctx.strokeStyle,
            size: this.ctx.lineWidth
        });
    }

    draw(e) {
        if (!this.isDrawing) return;
        
        e.preventDefault();
        const coords = this.getCanvasCoordinates(e);
        
        // Draw locally
        this.drawLine(this.lastX, this.lastY, coords.x, coords.y);
        
        // Send drawing data to server
        this.sendDrawingData({
            type: 'stroke_continue',
            x: coords.x,
            y: coords.y,
            lastX: this.lastX,
            lastY: this.lastY,
            color: this.ctx.strokeStyle,
            size: this.ctx.lineWidth
        });
        
        this.lastX = coords.x;
        this.lastY = coords.y;
    }

    stopDrawing() {
        if (!this.isDrawing) return;
        
        this.isDrawing = false;
        
        // Send stroke end event
        this.sendDrawingData({
            type: 'stroke_end'
        });
    }

    handleTouch(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 'mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        
        this.canvas.dispatchEvent(mouseEvent);
    }

    drawLine(x1, y1, x2, y2, color = null, size = null) {
        const originalColor = this.ctx.strokeStyle;
        const originalSize = this.ctx.lineWidth;
        
        if (color) this.ctx.strokeStyle = color;
        if (size) this.ctx.lineWidth = size;
        
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
        
        // Restore original settings
        this.ctx.strokeStyle = originalColor;
        this.ctx.lineWidth = originalSize;
    }

    sendDrawingData(data) {
        data.room_code = this.roomCode;
        this.socket.emit('drawing_data', data);
    }

    receiveDrawingData(data) {
        switch(data.type) {
            case 'stroke_start':
                // Start of a new stroke from another user
                break;
                
            case 'stroke_continue':
                // Continue drawing line
                this.drawLine(data.lastX, data.lastY, data.x, data.y, data.color, data.size);
                break;
                
            case 'stroke_end':
                // End of stroke
                break;
        }
    }

    clearCanvas() {
        // Clear locally and notify server
        this.clearCanvasLocal();
        this.socket.emit('clear_canvas', { room_code: this.roomCode });
    }

    clearCanvasLocal() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    updateConnectionStatus(message, status) {
        const statusElement = document.getElementById('connection-status');
        statusElement.textContent = message;
        statusElement.className = `connection-status ${status}`;
    }

    addPlayerToList(player) {
        const playersList = document.getElementById('players-list');
        const playerElement = document.createElement('li');
        playerElement.className = 'player-item';
        playerElement.id = `player-${player.id}`;
        playerElement.textContent = `Player ${player.id.substring(0, 6)}`;
        playersList.appendChild(playerElement);
    }

    removePlayerFromList(player) {
        const playerElement = document.getElementById(`player-${player.id}`);
        if (playerElement) {
            playerElement.remove();
        }
    }

    replayCanvasState(strokes) {
        console.log('Replaying canvas state:', strokes.length, 'strokes');
        
        // Clear canvas first
        this.clearCanvasLocal();
        
        // Replay all stored strokes
        strokes.forEach(stroke => {
            if (stroke.type === 'stroke_continue') {
                this.drawLine(stroke.lastX, stroke.lastY, stroke.x, stroke.y, stroke.color, stroke.size);
            }
        });
        
        this.showMessage(`Loaded existing drawing (${strokes.length} strokes)`);
    }

    showMessage(message) {
        const messageArea = document.getElementById('message-area');
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.textContent = message;
        messageArea.appendChild(messageElement);
        
        // Remove message after 3 seconds
        setTimeout(() => {
            messageElement.remove();
        }, 3000);
    }
}

// Test WebSocket connection function
function testConnection() {
    const socket = io();
    
    socket.on('connect', () => {
        console.log('Test: Connected to server');
        socket.emit('test_message', { message: 'Hello from client!' });
    });
    
    socket.on('test_response', (data) => {
        console.log('Test: Server response:', data);
    });
    
    socket.on('disconnect', () => {
        console.log('Test: Disconnected from server');
    });
} 