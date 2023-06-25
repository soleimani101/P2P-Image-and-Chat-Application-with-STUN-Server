from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

cache = redis.Redis(host='localhost', port=6379)

# Protocol for sending text data over TCP

@app.route('/send_peer_profile', methods=['POST'])
def send_peer_profile():
    data = request.get_json()
    username = data.get('username')
    address = data.get('address')
    print(username,address)
    if username and address:
        cache.set(username, address)
        return jsonify({'message': 'User profile saved successfully'}), 200
    else:
        return jsonify({'error': 'Invalid data'}), 400

@app.route('/get_all_peers', methods=['GET'])
def get_all_peers():
    usernames = cache.keys()
    usernames_str = [username.decode() for username in usernames]  # Convert bytes to string
    return jsonify({'peers': usernames_str}), 200

@app.route('/get_peer_info/<username>', methods=['GET'])
def get_peer_info(username):
    print(username)
    address = cache.get(username)
    print(address)
    if address:
        return ({'address': address.decode()}), 200
    else:
        return ({'error': 'Peer not found'}), 404




if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')
