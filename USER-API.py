from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample user database (in-memory for simplicity)
users = {}
user_id_counter = 1

# Middleware for logging requests
@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url} - Data: {request.get_json()}")

# Create User (POST)
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = {'id': user_id_counter, 'name': data['name'], 'email': data['email']}
    users[user_id_counter] = user
    user_id_counter += 1
    return jsonify(user), 201

# Get All Users (GET)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200

# Get Single User (GET)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

# Update User (PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    users[user_id]['name'] = data['name']
    users[user_id]['email'] = data['email']
    return jsonify(users[user_id]), 200

# Delete User (DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
