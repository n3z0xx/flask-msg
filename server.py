import time
from flask import Flask, request
import datetime

app = Flask(__name__)
messages = [{"username": "", "text": "print '/exit' to stop", "time": time.time(), "isSystem": True}]
users = {}


@app.route("/")
def hello_view():
    return "Welcome to python messenger server!"


@app.route("/status")
def status_view():
    return {"status": True,
            "time": datetime.datetime.now(),
            "messagesCount": len(messages),
            "usersCount": len(users)}


@app.route("/messages")
def messages_view():
    """
    Получение всех сообщений
    input:
    output: {
        "messages": [
            {"username": str, "text": str, "time": float}
        ]
    }
    """
    return {"messages": messages}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Отправка сообщений
    input: {
        "username": str,
        "password": str,
        "text": str,
        "isSystem": bool
    }
    output: {"isOk": bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username] != password:
        return {"ok": False}

    text = data["text"]
    if not(data["isSystem"]):
        messages.append({"username": username, "text": text, "time": time.time(), "isSystem": False})
    else:
        messages.append({"username": username, "text": text, "time": time.time(), "isSystem": True})
    return {"isOk": True}


@app.route("/auth", methods=['POST'])
def auth():
    """
    Авторизовать или сообщить о неверном пароле
    input: {
        "username": str,
        "password": str
    }
    output: {"ok": True}
    """
    data = request.json
    username = data["username"]
    password = data["password"]
    if username not in users:
        users[username] = password
        return {"ok": True}
    elif users[username] == password:
        return {"ok": True}
    else:
        return {"ok": False}


app.run(host=input("* Host: "))
