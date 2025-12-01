import requests


HOST = "http://127.0.0.1:65435"

choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()

# create account 
if choice == "N":
    print("Enter a unique username and memorable password.")
    username = input("Choose a username: ").strip()
    password = input("Enter a password: ").strip()

    requests.post(
        HOST + "/signup",
        json={"username": username, "password": password}
    )

    print("\nAccount created successfully!")
    print("Login Successful!\n")

    print("Type messages to send. Press Ctrl+C to exit.")
    while True:
        msg = input("> ")
        print("your message:", msg)

# login to account

elif choice == "L":
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    requests.post(
        HOST + "/login",
        json={"username": username, "password": password}
    )
    print("Login Successful! \n")

else:
    print("Invalid option. Please choose either N or L.")

# main chat loop
    print("Type messages to send. press Ctrl+C to exit.")
    while True:
        try:
            msg = input("> ").strip()
            if msg == "":
                continue
            # send message to server
            requests.post(
                HOST + "/send",
                json ={"username": username, "content": msg}
            )
            print(msg)

# retrieve All messages
            row = requests.get(HOST + "/messages")
            data = row.json()

            print("\n--- Chatroom Messages ---")
            for m in data["messages"]:
                print(f"{m['data']} {m['time']} - {m['username']}: {m['content']}")
            print("------------------------\n")

        except KeyboardInterrupt:
            print("\nExiting chat...")