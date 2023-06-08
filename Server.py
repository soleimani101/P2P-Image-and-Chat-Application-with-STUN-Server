from flask import Flask, request, jsonify
import redis
import socket
from PIL import Image
import io
import threading

app = Flask(__name__)

cache = redis.Redis(host='localhost', port=6379)

# Protocol for sending text data over TCP
def send_text_data(text, sock):
    packet_size = 1024  # Adjust the packet size as per your requirements

    # Split the text into packets
    packets = [text[i:i+packet_size] for i in range(0, len(text), packet_size)]

    for packet in packets:
        # Send the packet
        sock.send(packet.encode())

        # Wait for acknowledgment
        ack = sock.recv(1).decode()

        # If acknowledgment is not received, resend the packet
        if ack != 'A':
            sock.send(packet.encode())

# Protocol for sending image data over UDP
def send_image_data(image_path, sock, addr):
    packet_size = 1024  # Adjust the packet size as per your requirements

    # Open and convert the image to matrix
    image = Image.open(image_path)
    image_matrix = image.load()

    # Get the image dimensions
    width, height = image.size

    for row in range(height):
        packet = bytearray()
        for col in range(width):
            # Get the RGB values from the matrix
            r, g, b = image_matrix[col, row]

            # Pack the RGB values into the packet
            packet.extend([r, g, b])

            # If packet size exceeds the limit or it's the last column, send the packet
            if len(packet) >= packet_size or col == width - 1:
                # Send the packet using UDP socket
                sock.sendto(packet, addr)

                # Wait for acknowledgment
                ack, _ = sock.recvfrom(1)

                # If acknowledgment is not received, resend the packet
                if ack != b'A':
                    sock.sendto(packet, addr)

                # Clear the packet
                packet.clear()









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
    app.run(port=8000)
