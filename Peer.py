import requests
import socket
import threading
import random
import os
from PIL import Image
import math

import socket
import math
from tqdm import tqdm




globalPort = 9096
INCHAT = False
def connect_user():
    choice = input("(1) Do you want to get online and wait for Image files?\n(2) Send Images?\n(3) get online and wait for text? \n(4) send text message?\n")
    #recieving files
    if choice == "1":
        Listen_for_files()
    elif choice == "2":
        SendImage()
    elif choice == "3":
        ReceiveText()
    elif choice == "4":
        SendText()
    else:
        print("Invalid choice.")






def ReceiveText():
    name = input("who are you ???")
    send_peer_profile_inapp(name)
    Ip , port = request_special_peer_in_app(name)
    globalPort = port
    print("Waiting for connection...")

    sender_ip =Ip  # IP address of the receiver
    sender_port = globalPort  # Port number to listen on

    # Create a socket object
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the IP address and port
    sender_socket.bind((sender_ip, sender_port))

    # Listen for incoming connections
    sender_socket.listen(1)
    print("listening...")

    # Accept a connection from the receiver
    receiver_socket, receiver_address = sender_socket.accept()
    print("Connected to:", receiver_address)

    # Function to send messages
    def send_messages():
        while True:
            # Send data to the receiver
            message = input("you: ")
            receiver_socket.send(message.encode())

            # Check for the disconnect command
            if message == 'disconnect':
                break

    # Function to receive messages
    def receive_messages():
        while True:
            # Receive data from the receiver
            data = receiver_socket.recv(1024)
            message = data.decode()
            print("that:", message)

            # Check for the disconnect command
            if message == 'disconnect':
                break

    # Create and start the send and receive message threads
    send_thread = threading.Thread(target=send_messages)
    receive_thread = threading.Thread(target=receive_messages)

    send_thread.start()
    receive_thread.start()

    # Wait for the threads to finish
    send_thread.join()
    receive_thread.join()

    # Close the connection
    receiver_socket.close()
    sender_socket.close()



def SendText(): 
    
    name = input("Enter the name of the user: ")

    ip, port = request_special_peer_in_app(name)
    globalPort = port
    receiver_ip = ip  # IP address of the receiver
    receiver_port = globalPort  # Port number of the receiver

    # Create a socket object
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the sender
    receiver_socket.connect((receiver_ip, receiver_port))
    print("Connected to sender.")

    # Function to send messages
    def send_messages():
        while True:
            # Send data to the sender
            message = input("Receiver: ")
            receiver_socket.send(message.encode())

            # Check for the disconnect command
            if message == 'disconnect':
                break

    # Function to receive messages
    def receive_messages():
        while True:
            # Receive data from the sender
            data = receiver_socket.recv(1024)
            message = data.decode()
            print("Sender:", message)

            # Check for the disconnect command
            if message == 'disconnect':
                break

    # Create and start the send and receive message threads
    send_thread = threading.Thread(target=send_messages)
    receive_thread = threading.Thread(target=receive_messages)

    send_thread.start()
    receive_thread.start()

    # Wait for the threads to finish
    send_thread.join()
    receive_thread.join()

    # Close the connection
    receiver_socket.close()






def SendImage():
    name = input("Enter the name of the user: ")
    file_name = input("Enter the name of the file: ")

    ip, port = request_special_peer_in_app(name)
    IP_PORT =(ip, port)
    globalPort = port
    receiver_ip = "127.0.0.1"  # IP address of the receiver
    receiver_port = globalPort  # Port number of the receiver
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    image_path = file_name


    # Define the IP address and port to bind the sender


    # Create a socket object
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Read the image file as binary data
    with open(image_path, 'rb') as file:
        image_data = file.read()

    # Get the image size and calculate the number of packets needed
    image_size = len(image_data)
    packet_size = 1024
    num_packets = math.ceil(image_size / packet_size)

    # Send the number of packets to the receiver
    receiver_address = ('127.0.0.1', receiver_port)  # Replace with receiver's IP address and port
    sender_socket.sendto(str(num_packets).encode(), receiver_address)

    # Wait for the acceptance response from the receiver
    response, _ = sender_socket.recvfrom(1024)
    response = response.decode()

    if response == 'accept':
        print("File accepted. Sending...")

        # Split the image data into packets and send them to the receiver
        progress_bar = tqdm(total=num_packets, unit='packets')
        for i in range(num_packets):
            start = i * packet_size
            end = start + packet_size
            packet_data = image_data[start:end]
            sender_socket.sendto(packet_data, receiver_address)
            progress_bar.update(1)

        progress_bar.close()
        print("File sent successfully.")
    else:
        print("File rejected.")

    # Close the socket
    sender_socket.close()





def Listen_for_files():
            
        ##############################
        name = input("who are you ???")
        send_peer_profile_inapp(name)
        Ip , port = request_special_peer_in_app(name)
        IP_PORT =(Ip, port)
        globalPort = port
        print("Waiting for connection...")

        your_ip = "127.0.0.1"  # IP address of the receiver
        your_port = globalPort  # Port number to listen on
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver_socket.bind((your_ip, your_port))

        image_path = "rec.jpg"  # Replace with the desired path to save the received image

        # Receive the number of packets from the sender
        num_packets_data, sender_address = receiver_socket.recvfrom(1024)
        num_packets = int(num_packets_data.decode())

        # Prompt the receiver to accept or reject the file
        response = input("Do you want to accept the received file? (y/n): ")

        # Send the acceptance response to the sender
        if response.lower() == 'y':
            receiver_socket.sendto('accept'.encode(), sender_address)
        else:
            receiver_socket.sendto('reject'.encode(), sender_address)

        # If accepted, receive and save the image data packets
        if response.lower() == 'y':
            image_data = b''
            for i in range(num_packets):
                packet_data, sender_address = receiver_socket.recvfrom(1024)
                image_data += packet_data

            # Write the received image data to a file
            with open('received_image.jpg', 'wb') as file:
                file.write(image_data)

        # Close the socket
        receiver_socket.close()

    



def send_peer_profile():
    username = input("Enter your username: ")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    Port = random.randint(8001, 8100)
    print(ip_address,Port)
    url = 'http://localhost:8000/send_peer_profile'
    data = {
        'username': username,
        'address':  f'({ip_address},{Port})',
    }   
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception if an HTTP error occurred
        data = response.json()
        if 'message' in data:
            print(data['message'])
        else:
            print('Error: Unexpected response')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        
        
        
def send_peer_profile_inapp(username):
    Port = random.randint(8001, 8100)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    url = 'http://localhost:8000/send_peer_profile'
    data = {
        'username': username,
        'address':  f'({ip_address},{Port})',
    }   
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception if an HTTP error occurred
        data = response.json()
        if 'message' in data:
            print(data['message'])
        else:
            print('Error: Unexpected response')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        



def request_get_all_peers():
    url = 'http://localhost:8000/get_all_peers'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        peers = data.get('peers')
        if peers:
            print("List of Peers:")
            for peer in peers:
                print(peer)
        else:
            print("No peers found")
    else:
        print(f"Error: {response.status_code}")

def request_special_peer():
    username = input("Enter the username: ")
    url = f'http://localhost:8000/get_peer_info/{username}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data.get('address')
        print(address)

        if address:
            address = address.strip('()')  # Remove parentheses
            ip, port = address.split(',')  # Split IP and port
            ip = ip.strip()  # Remove whitespace
            port = int(port.strip())  # Convert port to integer
            print(f"Peer {username}: IP={ip}, Port={port}")
            return ip, port
        
        else:
            print(f"Peer {username} not found")
    else:
        print(f"Peer {username} not found")



def request_special_peer_in_app(username):
    url = f'http://localhost:8000/get_peer_info/{username}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data.get('address')
        print(address)

        if address:
            address = address.strip('()')  # Remove parentheses
            ip, port = address.split(',')  # Split IP and port
            ip = ip.strip()  # Remove whitespace
            port = int(port.strip())  # Convert port to integer
            print(f"Peer {username}: IP={ip}, Port={port}")
        else:
            print(f"Peer {username} not found")
    else:
        print(f"Error: {response.status_code}")

    return ip, port


def main():
    while True:
        print("--------------------------------")
        print("1. Signup")
        print("2. Display all users")
        print("3. Get address of a user")
        print("4. Connect to a user")
        print("0. Cancel")
        print("--------------------------------\n\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            send_peer_profile()
        elif choice == "2":
            request_get_all_peers()
        elif choice == "3":
            request_special_peer()
        elif choice == "4":
            connect_user()
        elif choice == "0":
            print("Canceled.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
