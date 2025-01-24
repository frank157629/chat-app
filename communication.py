# Chat Communication Module with One-to-One Communication and Future AI & Encryption Integration
# This code handles one-to-one communication for an instant messaging website.
# Features include secure message sending, receiving, and real-time updates, with future extensibility for AI and encryption.

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # Import CORS for cross-origin resource sharing
from datetime import datetime
import hashlib

# Initialize Flask app
# Flask is a lightweight WSGI web application framework in Python
app = Flask(__name__)
# Enable CORS support for cross-origin requests
CORS(app)
# Configure the secret key for secure sessions
app.config['SECRET_KEY'] = 'your_secret_key_here'
# Initialize SocketIO for real-time communication
socketio = SocketIO(app)

# In-memory storage for simplicity (use a database in production)
users = {}  # Stores user connection info
messages = []  # Stores chat messages

# Helper function to hash messages for basic integrity check
# This can later be replaced with encryption for added security
def hash_message(message):
    """
    Hashes a message using SHA-256 for basic integrity checks.
    :param message: The message string to hash.
    :return: A hexadecimal string of the hashed message.
    """
    return hashlib.sha256(message.encode()).hexdigest()

# Root endpoint for the base URL
@app.route('/')
def home():
    """
    Home endpoint to provide a welcome message and API instructions.
    :return: HTML content with instructions.
    """
    return "<h1>Welcome to the Chat API</h1><p>Use endpoints like /connect, /send_message, /get_messages.</p>"

# Endpoint for user to connect to the chat
@app.route('/connect', methods=['POST'])
def connect_user():
    """
    Connects a user to the chat system.
    :return: JSON response indicating connection status.
    """
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Add user to the in-memory user storage
    users[user_id] = {"connected": True, "last_seen": datetime.now()}
    print(f"User {user_id} connected")  # Debug log
    return jsonify({"message": f"User {user_id} connected successfully"})

# Endpoint to send a message
@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Sends a message from one user to another.
    :return: JSON response with message status and data.
    """
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')

    # Validate input
    if not sender_id or not receiver_id or not message:
        return jsonify({"error": "Sender ID, Receiver ID, and message are required"}), 400

    if receiver_id not in users:
        return jsonify({"error": "Receiver is not connected"}), 404

    # Generate timestamp and hash for the message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hashed_message = hash_message(message)
    msg_data = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
        "hash": hashed_message,
        "timestamp": timestamp
    }
    messages.append(msg_data)

    # Emit message to the receiver in real-time
    print(f"Message sent from {sender_id} to {receiver_id}: {message}")  # Debug log
    socketio.emit('new_message', msg_data, to=receiver_id)
    return jsonify({"message": "Message sent successfully", "data": msg_data})

# Endpoint to retrieve messages for a user
@app.route('/get_messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    """
    Retrieves all messages for a specific user.
    :param user_id: ID of the user to retrieve messages for.
    :return: JSON list of messages.
    """
    user_messages = [msg for msg in messages if msg['receiver_id'] == user_id or msg['sender_id'] == user_id]
    print(f"Messages retrieved for user {user_id}: {user_messages}")  # Debug log
    return jsonify(user_messages)

# Endpoint to disconnect a user
@app.route('/disconnect', methods=['POST'])
def disconnect_user():
    """
    Disconnects a user from the chat system.
    :return: JSON response indicating disconnection status.
    """
    data = request.json
    user_id = data.get('user_id')
    if user_id in users:
        users[user_id]["connected"] = False
        users[user_id]["last_seen"] = datetime.now()
        print(f"User {user_id} disconnected")  # Debug log
        return jsonify({"message": f"User {user_id} disconnected"})
    return jsonify({"error": "User not found"}), 404

# Real-time updates when a message is sent
@socketio.on('send_message')
def handle_message(data):
    """
    Handles real-time message sending.
    :param data: Dictionary containing sender_id, receiver_id, and message.
    """
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']

    if receiver_id in users:
        print(f"Real-time message from {sender_id} to {receiver_id}: {message}")  # Debug log
        emit('new_message', {"sender_id": sender_id, "message": message}, to=receiver_id)

# Main entry point to run the Flask application
if __name__ == '__main__':
    print("Starting Flask application...")  # Debug log
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
