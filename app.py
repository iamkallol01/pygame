from flask import Flask, render_template, jsonify, request
import threading
import time
import os

app = Flask(__name__)

# Placeholder for the game thread
game_thread = None

# Function to run the Pygame logic
def run_game():
    os.system("python 02update.py")  # Runs your existing Pygame script

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_game", methods=["POST"])
def start_game():
    global game_thread
    if game_thread is None or not game_thread.is_alive():
        game_thread = threading.Thread(target=run_game)
        game_thread.start()
        return jsonify({"status": "Game started"})
    return jsonify({"status": "Game is already running"})

@app.route("/stop_game", methods=["POST"])
def stop_game():
    global game_thread
    if game_thread and game_thread.is_alive():
        # This example assumes that the game can safely exit itself.
        # Add termination logic here if needed.
        return jsonify({"status": "Game stopped"})
    return jsonify({"status": "Game is not running"})

if __name__ == "__main__":
    app.run(debug=True)
