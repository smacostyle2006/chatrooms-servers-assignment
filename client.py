import requests
from datetime import datetime
import asyncio

from messages_function import run_messages
import config as cfg


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

try:
    choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()
#--------------- create account ----------------
    if choice == "N":
        print("Enter a unique username and memorable password.")
        username = input("Choose a username: ").strip()
        password = input("Enter a password: ").strip()

        if username == "" or password == "":
            print("You have to type a username and password")

        response = requests.post( 
            cfg.HOST + "/signup", 
            data={"username": username, "password": password})
        
        if response.status_code == 409:
            print("Username already taken")
        else:
            print("\nAccount created successfully!")
            
            message_number = pull_and_show_messages()
            print("Type messages to send. Press Ctrl+C to exit.")
            asyncio.run(run_messages(username, message_number))

# --------------login to account ------------------            
    elif choice == "L":
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if username == "" or password == "":
            print("You have to type a username and password")

        row = requests.post(
            cfg.HOST + "/login",
            data={"username": username, "password": password}
        )

        if row.status_code == 401:
            print("Invalid username or password")
        else:
            print("Login Successful! \n")

            print("Type messages to send. Press Ctrl+C to exit.")

            print("\nAccount created successfully!")
            
            message_number = pull_and_show_messages()
            print("Type messages to send. Press Ctrl+C to exit.")
            asyncio.run(run_messages(username, message_number))

# ------------------ INVALID CHOICE ------------------
    else:
        print("Invalid option. Please choose either N or L.")

except KeyboardInterrupt:
    print("You seem want to leave early.. Have a good day!")
except:
    print("There is something wrong with connection between users and servers, try to re-initiate server before proceed!")





