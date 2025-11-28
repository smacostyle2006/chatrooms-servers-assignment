

choice = input("Would you like to create a new account [N] or to login [L]?\n").upper()

if choice == "N":
    print("Enter a unique username and memorable password.")
    username = input("Choose a username: ").strip()
    password = input("Enter a password: ").strip()

    print("\nAccount created successfully!")
    print("Login Successful!\n")

    print("Type messages to send. Press Ctrl+C to exit.")
    while True:
        msg = input("> ")
        print("your message:", msg)

elif choice == "L":
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    print("Login Successful! \n")
    print("Type messages to send. press Ctrl+C to exit.")
    while True:
        msg = input("> ")
        print("your message:", msg)

else:
    print("Invalid option. Please choose either N or L.")
