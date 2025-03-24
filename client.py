#1211326-Raghed
#1210596-Arein
#1211968-Lina

import socket
import threading

# Constants
BUFFER_SIZE = 1024

# Prompt user for server details and establish connection
while True:
    try:
        SERVER_IP = input("Enter the server IP address: ").strip()
        SERVER_PORT = int(input("Enter the server port number: "))

        # Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(15)

        # Get username
        username = input("Enter your name: ").strip()
        try:
            client_socket.sendto(username.encode(), (SERVER_IP, SERVER_PORT))
            print(f"Successfully connected to server at {SERVER_IP}:{SERVER_PORT}")  # Confirmation message
            break  # Exit loop if connection is successful
        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running at {SERVER_IP}:{SERVER_PORT}?")
        except Exception as e:
            print(f"Could not connect to server: {e}")
            client_socket.close() # Close the socket if connection fails

    except ValueError:
        print("Invalid port number. Please enter a valid integer.")


def listen_to_server():
    """Listen for messages from the server and display them."""
    while True:
        try:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            print(data.decode())
        except socket.timeout:
            # Continue listening silently if no message is received
            continue
        except ConnectionResetError:
            print("Connection to the server was lost. Exiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

# Start thread to listen for server messages
listener_thread = threading.Thread(target=listen_to_server, daemon=True)
listener_thread.start()

# Main loop to send answers
while True:
    try:
        answer = input("Your answer (or type 'exit' to quit): \n").strip()
        if answer.lower() == "exit":
            print("Exiting the game. Goodbye!")
            break
        client_socket.sendto(answer.encode(), (SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Error sending data: {e}")
        break

client_socket.close() #Close the socket after the loop finishes