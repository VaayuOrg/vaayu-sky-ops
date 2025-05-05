from flask import Flask
from flask_socketio import SocketIO
from api.ws_routes import DroneControlRoute
from core.config.config import config

# Create Flask instance
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_interval=5, ping_timeout=10)

# Initialize WebSocket routes BEFORE running the app
drone_socket = DroneControlRoute(socketio)

if __name__ == "__main__":
    socketio.run(app, host=config["host"], port=config["server_port"], debug=True)
