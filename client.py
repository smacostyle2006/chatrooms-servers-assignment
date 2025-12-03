import requests
from datetime import datetime


HOST = "http://127.0.0.1:65435"

choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()

#--------------- create account ----------------
if choice == "N":
    print("Enter a unique username and memorable password.")
    username = input("Choose a username: ").strip()
    password = input("Enter a password: ").strip()
    
    response = requests.post( 
        HOST + "/signup", 
        data={"username": username, "password": password})

    if response.status_code == 400:
        print("You have to type a username and password")
    elif response.status_code == 409:
        print("Username already taken")
    else:
        print("\nAccount created successfully!")


        def pull_and_show_messages():
            r = requests.get(HOST + "/messages")

            messages = r.json()

            print("\n===== Previous Messages =====")
            for msg in messages["messages"]:
                full_stamp = f"{msg['date']} {msg['time']}"
                print(f"[{full_stamp}] {msg['username']}: {msg['content']}")
            print("=============================\n")

        
        pull_and_show_messages()
        print("Type messages to send. Press Ctrl+C to exit.")

        def send_message():
            while True:
                msg = input("> ").strip()

                if msg == "":
                    continue

                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                requests.post(
                    HOST + "/send",
                    data={
                        "username": username,
                        "content": msg,
                        "date": date_str,
                        "time": time_str
                    }
                )
        send_message()

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
