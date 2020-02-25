import time
from datetime import datetime
import requests
import os
import threading
import sys

name = "noname"
password = "pass"
ip = "0.0.0.0"
stop = False

def update():
    global stop
    
    last_messages = requests.get("http://"+ip+":5000/messages").json()["messages"]
    display_messages(last_messages)
    while True:
        if stop:
            sys.exit()
        response = requests.get("http://"+ip+":5000/messages")
        messages = response.json()["messages"]
        if len(messages) != len(last_messages):
            os.system("cls")
            display_messages(messages)
            last_messages = messages

        time.sleep(1)


def sender():
    global stop
    while True:
        try:
            text = input()
        except EOFError:
            stop = True
            sys.exit()
        if text == "/exit":
            # exit message 
            requests.post("http://" + ip + ":5000/send", json={"username": name, "text": "left the chat.", "password": password, "isSystem": True})
            stop = True
            sys.exit()
        if text != "":
            requests.post("http://"+ip+":5000/send", json={"username": name, "text": text, "password": password, "isSystem": False})


def display_messages(messages):
    for message in messages:
        normal_time = datetime.fromtimestamp(message["time"])
        normal_time = normal_time.strftime("%d/%m/%Y %H:%M:%S")
        if message["isSystem"]:
            print("***", message["username"], message["text"], normal_time)
        else:
            print(message["username"], normal_time)
            print(message["text"])
        print()


def start():
    global name
    global password
    global ip

    ip = input("*** Server ip: ")
    print("*** Attempt to connect...")
    try:
        requests.get("http://"+ip+":5000/status")
    except (requests.exceptions.ConnectionError, TimeoutError):
        print("*** Server unreachable")
        sys.exit()
    print("*** Connected successfully")
    name = input("*** Nickname: ")
    password = input("*** Password: ")
    response = requests.post(
        "http://"+ip+":5000/auth",
        json={"username": name, "password": password}
    )
    if not response.json()["ok"]:
        print("*** Bad password")
        sys.exit()
        
    # join message
    requests.post("http://" + ip + ":5000/send", json={"username": name, "text": "join the chat.", "password": password, "isSystem": True})
    sender_thread = threading.Thread(target=sender, args="")
    update_thread = threading.Thread(target=update, args="")
    sender_thread.start()
    os.system("cls")
    update_thread.start()

start()
