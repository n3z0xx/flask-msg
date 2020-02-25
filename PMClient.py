import time
from datetime import datetime
import requests
import os
import threading
import sys

global name
global password
global ip


def update():
    last_messages = requests.get("http://"+ip+":5000/messages").json()["messages"]
    display_messages(last_messages)
    while True:
        response = requests.get("http://"+ip+":5000/messages")
        messages = response.json()["messages"]
        if len(messages) != len(last_messages):
            os.system("cls")
            display_messages(messages)
            last_messages = messages

        time.sleep(1)


def sender():
    print("*** sender: OK")
    while True:
        text = input()
        if text == "/exit":
            requests.post("http://" + ip + ":5000/send",
                          json={"username": name, "text": "*** Exit the chat.", "password": password, "isSystem": True})
            sys.exit()
        requests.post("http://"+ip+":5000/send",
                      json={"username": name, "text": text, "password": password, "isSystem": False})


def display_messages(messages):
    for message in messages:
        normal_time = datetime.fromtimestamp(message["time"])
        normal_time = normal_time.strftime("%d/%m/%Y %H:%M:%S")
        print(message["username"], normal_time)
        print(message["text"])
        print()


def start():
    global name
    global password
    global ip

    ip = input("*** Server ip: ")
    time.sleep(1)
    print("*** Attempt to connect...")
    try:
        requests.get("http://"+ip+":5000/status")
    except requests.exceptions.ConnectionError:
        print("*** SERVER OFFLINE")
        sys.exit()
    time.sleep(1)
    print("*** Connected successfully")
    time.sleep(1)
    name = input("*** Nickname: ")
    password = input("*** Password: ")
    time.sleep(1)
    response = requests.post(
        "http://"+ip+":5000/auth",
        json={"username": name, "password": password}
    )
    if not response.json()["ok"]:
        print("*** Bad password")
        sys.exit()
    else:
        print("*** Login/registration successful")
    time.sleep(1)
    print("*** Starting threads")
    threading.Thread(target=sender, args="").start()
    time.sleep(1)
    print("*** updater: OK")
    time.sleep(1)
    print("*** Get ready!")
    time.sleep(5)
    os.system("cls")
    # join message
    requests.post("http://" + ip + ":5000/send",
                  json={"username": name, "text": "*** Join the chat. o/", "password": password, "isSystem": True})
    threading.Thread(target=update, args="", daemon=True).start()


start()
