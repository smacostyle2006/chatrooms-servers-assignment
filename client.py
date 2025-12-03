import requests
from datetime import datetime
import asyncio

from messages_function import run_messages
import config as cfg


choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()

#--------------- create account ----------------
if choice == "N":
    print("Enter a unique username and memorable password.")
    username = input("Choose a username: ").strip()
    password = input("Enter a password: ").strip()
    
    response = requests.post( 
        cfg.HOST + "/signup", 
        data={"username": username, "password": password})

    if response.status_code == 400:
        print("You have to type a username and password")
    elif response.status_code == 409:
        print("Username already taken")
    else:
        print("\nAccount created successfully!")

        def pull_and_show_messages():
            message_number = 0
            r = requests.get(cfg.HOST + "/messages")

            messages = r.json()

            print("\n===== Previous Messages =====")
            for msg in messages["messages"]:
                full_stamp = f"{msg['date']} {msg['time']}"
                print(f"[{full_stamp}] {msg['username']}: {msg['content']}")
                message_number += 1
            print("=============================\n")
            return message_number

        
        message_number = pull_and_show_messages()
        print("Type messages to send. Press Ctrl+C to exit.")
        print(message_number)
        asyncio.run(run_messages(username, message_number))

# --------------login to account ------------------

elif choice == "L":
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    row = requests.post(
        HOST + "/login",
        data={"username": username, "password": password}
    )
    print("Login Successful! \n")

    print("Type messages to send. Press Ctrl+C to exit.")

    while True:
        msg = input("> ").strip()
        if msg == "":
            continue

        # send message
        requests.post(
            HOST + "/send",
            data={"username": username, "content": msg}
        )

        # get all messages
        row = requests.get(HOST + "/messages")
        data = row.json()

        print("\n--- Chatroom Messages ---")
        for m in data["messages"]:
            print(f"{m['date']} {m['time']} - {m['username']}: {m['content']}")
        print("------------------------\n")


# ------------------ INVALID CHOICE ------------------
else:
    print("Invalid option. Please choose either N or L.")
