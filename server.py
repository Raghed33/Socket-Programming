#1211326-Raghed
#1210596-Arein
#1211968-Lina

import socket
import threading
import time
import random
import logging
import signal
import sys

# Constants
SERVER_IP = "172.19.1.22"
SERVER_PORT = 5689
BUFFER_SIZE = 1024
MIN_PLAYERS = 2
ROUND_DELAY = 30  # Seconds before starting a new round
QUESTION_DELAY = 30  # Time between questions
ANSWER_TIME = 30  # Time to wait for answers
TOTAL_ROUNDS = 2  # Total number of rounds

# Questions database
QUESTIONS = [
    {"question": "Which planet is known as the 'Blue Planet'?", "answer": "earth"},
    {"question": "How many bones are in the human body?", "answer": "206"},
    {"question": "What is 5 * (4 + 2)?", "answer": "30"},
    {"question": "In which year did World War II end?", "answer": "1945"},
    {"question": "What is the capital of Palestine?", "answer": "Jerusalem"},
    {"question": "What is 15 / 3 - 2?", "answer": "3"},
    {"question": "What is the closest star to Earth?", "answer": "sun"},
    {"question": "What is the square root of 25?", "answer": "5"},
    {"question": "What is the capital of Japan?", "answer": "tokyo"},
]

clients = {}
scores = {}
round_wins = {}  # To track the number of rounds won by each player


# Helper function to broadcast a message to all clients
def broadcast(message):
    for client in clients:
        try:
            server_socket.sendto(message.encode(), client)
        except Exception as e:
            print(f"Error sending to {client}: {e}")

def handle_answers(question, answers):
    correct_answers = {}
    for addr, ans in answers.items():
        if ans.lower() == question["answer"].lower():
            correct_answers[addr] = ans
    return correct_answers

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

def process_round(questions, round_number):
    global scores
    scores = {addr: 0 for addr in clients}
    broadcast(f"Starting Round {round_number}!")

    for idx, question in enumerate(questions, start=1):
        broadcast(f"Question {idx}: {question['question']}")
        logging.info(f"Round {round_number}, Question {idx}: {question['question']}")

        first_answers = {}
        start_time = time.time()
        server_socket.settimeout(ANSWER_TIME)

        try:
            while True:
                try:
                    data, addr = server_socket.recvfrom(BUFFER_SIZE)
                    answer = data.decode().strip().lower()
                    logging.debug(f"Received answer from {addr}: {answer}")
                    if addr not in first_answers:
                        first_answers[addr] = answer
                        logging.debug(f"First answer recorded for {addr}: {answer}")
                except socket.timeout:
                    logging.info("Timeout waiting for answers.")
                    break
                except Exception as e:
                    logging.error(f"Error receiving answer: {e}")
                    break
        except Exception as e:
            logging.exception(f"Error during answer reception: {e}")

        correct_answers = {addr: ans for addr, ans in first_answers.items() if ans == question["answer"].lower()}
        incorrect_answers = {addr: ans for addr, ans in first_answers.items() if ans != question["answer"].lower()}
        no_answers = set(clients.keys()) - set(first_answers.keys())

        broadcast(f"Time's up! The correct answer was: {question['answer']}")

        if correct_answers:
            sorted_correct_answers = sorted(correct_answers.items(), key=lambda x: list(first_answers.keys()).index(x[0]))
            for i, (addr, ans) in enumerate(sorted_correct_answers):
                points = 1 if len(sorted_correct_answers) == 1 else (len(sorted_correct_answers) - i) / len(sorted_correct_answers)
                scores[addr] = scores.get(addr, 0) + points
                broadcast(f"{clients[addr]} got it right (+{points:.3f} points)!")
                logging.info(f"{clients[addr]} got it right (+{points:.3f} points)!")

        for addr, ans in incorrect_answers.items():
            broadcast(f"{clients[addr]} answered: {ans} (Incorrect)")
            logging.info(f"{clients[addr]} answered: {ans} (Incorrect)")

        for addr in no_answers:
            broadcast(f"{clients[addr]} did not answer.")
            logging.info(f"{clients[addr]} did not answer.")

        broadcast("Current Scores:")
        for addr, score in scores.items():
            broadcast(f"{clients[addr]}: {score:.2f} points")
            logging.info(f"{clients[addr]}: {score:.2f} points")

        time.sleep(QUESTION_DELAY)

    if scores:
        winner = max(scores, key=scores.get)
        broadcast(f"Round {round_number} Winner: {clients[winner]} with {scores[winner]:.2f} points!")
        logging.info(f"Round {round_number} Winner: {clients[winner]} with {scores[winner]:.2f} points!")
        round_wins[winner] = round_wins.get(winner, 0) + 1
    else:
        broadcast(f"Round {round_number} had no winner.")


def trivia_game():
    while True:
        if len(clients) >= MIN_PLAYERS:
            broadcast("Starting the Trivia Game in 30 seconds! Get ready!")
            time.sleep(ROUND_DELAY)

            for round_number in range(1, TOTAL_ROUNDS + 1):
                questions = random.sample(QUESTIONS, 3)
                process_round(questions, round_number)
                broadcast(f"Next round starts in 30 seconds. Be ready!")
                time.sleep(ROUND_DELAY)

            if round_wins:
                game_winner = max(round_wins, key=round_wins.get)
                broadcast(f"Game Winner: {clients[game_winner]} with {round_wins[game_winner]} round wins!")
            else:
                broadcast("No overall winner. Better luck next time!")
            break
        else:
            logging.info("Waiting for at least 2 clients to join the game...")
            time.sleep(5)

# Shutdown function
def shutdown_server(signum, frame):
    print("\nServer is shutting down. Goodbye!")
    broadcast("Server is shutting down. Thanks for playing!")
    if server_socket:
        server_socket.close()  # Close the socket if it's open
    sys.exit(0)

# Set up signal handler
signal.signal(signal.SIGINT, shutdown_server)

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.settimeout(ANSWER_TIME)
print(f"Server started on {SERVER_IP}:{SERVER_PORT}")

# Thread for game logic
game_thread = threading.Thread(target=trivia_game, daemon=True)
game_thread.start()

# Main server loop to handle client registration
while True:
    try:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        username = data.decode().strip()
        if addr not in clients:
            clients[addr] = username
            scores[addr] = 0
            print(f"{username} joined the game from {addr}")
            broadcast(f"{username} has joined the game!")
    except socket.timeout:
        print("Timeout waiting for new clients to join.")
    except Exception as e:
        print(f"Unexpected error: {e}")