from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

socketio = SocketIO(app)

mongo_uri = os.environ["MONGO_URI"]
client = MongoClient(mongo_uri)
db = client["SNS"]
messages_collection = db["messages"]


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("load messages")
def load_messages():
    messages = messages_collection.find().sort("_id", -1).limit(10)
    messages = list(messages)[::-1]
    messages_return = [message["message"] for message in messages]
    emit("load all messages", messages_return)


@socketio.on("send message")
def send_message(message):
    messages_collection.insert_one({"message": message})
    emit("load one message", message, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
