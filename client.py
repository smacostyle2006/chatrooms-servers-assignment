from flask import request



HOST = "http://127.0.0.1:65435"

choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()

#--------------- create account ----------------
if choice == "N":
    print("Enter a unique username and memorable password.")
    username = input("Choose a username: ").strip()
    password = input("Enter a password: ").strip()

    row = request.post(
        HOST + "/signup",
        data={"username": username, "password": password}
    )

    print("\nAccount created successfully!")
    print("Login Successful!\n")

    print("Type messages to send. Press Ctrl+C to exit.")

    while True:
        msg = input("> ").strip()
        if msg == "":
            continue

        # send message
        request.post(
            HOST + "/send",
            data={"username": username, "content": msg}
        )

        # get all messages
        row = request.get(HOST + "/messages")
        data = row.json()

        print("\n--- Chatroom Messages ---")
        for m in data["messages"]:
            print(f"{m['date']} {m['time']} - {m['username']}: {m['content']}")
        print("------------------------\n")

# --------------login to account ------------------

elif choice == "L":
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    row = request.post(
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
        request.post(
            HOST + "/send",
            data={"username": username, "content": msg}
        )

        # get all messages
        row = request.get(HOST + "/messages")
        data = row.json()

        print("\n--- Chatroom Messages ---")
        for m in data["messages"]:
            print(f"{m['date']} {m['time']} - {m['username']}: {m['content']}")
        print("------------------------\n")


# ------------------ INVALID CHOICE ------------------
else:
    print("Invalid option. Please choose either N or L.")
