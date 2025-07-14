#Python Banking Program, includes, show balance, deposit, withdraw, exit
import time
import json
#Registration
def register():
    while True:
        username = input("Choose your username: ")
        password = input("Choose your password: ")
        try:
            with open("users.json","r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {}
        if username in users:
            print("❌ Username already exists.")
            continue
        users[username] = {"password": password, "balance": 0}

        with open("users.json", "w") as f:
            json.dump(users, f)

        print("✅ Registration Succesful")
        break
#Login
def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            print("No user data found")
            return None

        if username in users and users[username]["password"] == password:
            print(f"🎉 Welcome back, {username}!")
            return username
        else:
            print("❌ Invalid credentials.")
        continue
#Banking Choice

def show_balance(balance):
    print("\n=======================")
    print(f"Balance: ${balance:.2f}")
    print("=======================\n")
    time.sleep(1)

def deposit(balance):
    amount = float(input("\nHow much would you like to deposit? "))
    if amount < 0:
        print("❌ Invalid amount")
    else:
        balance += amount
        print("\n=======================")
        print(f"Deposit: +${amount}")
        print(f"New Balance: ${balance:.2f}")
        print("=======================\n")
        time.sleep(1)
    return balance

def withdraw(balance):
    amount = float(input("\nHow much would you like to withdraw? "))
    if amount > balance:
        print("❌ Insufficient Funds.")
    else:
        balance -= amount
        print("\n=======================")
        print(f"Withdraw: -${amount}")
        print(f"New Balance: ${balance:.2f}")
        print("=======================\n")  
        time.sleep(1)
    return balance

def main():
    is_running = False
    choices = ("Balance", "Deposit", "Withdraw", "Exit")
    print("====================================")
    print("            CUTEST BANK             ")
    print("====================================")
    print("Welcome! What would you like to do?")
    print("1. Register")
    print("2. Login")
    login_choice = input("Enter 1 or 2: ")
    if login_choice == "1":
        register()
        username = login()
        is_running = True
    elif login_choice == "2":
        username = login()
        is_running = True
    else:
        print("Invalid option. Try again.")
    with open("users.json", "r") as f:
        users = json.load(f)

    balance = users[username]["balance"]
    while is_running:
        print("=======================")
        print("      CUTEST BANK      ")
        print("=======================")
        for types in range(len(choices)):
            print(f"{types+1}. {choices[types]}")
        print()
        choice = input("Enter your choice (1-4): ")

        match choice:
            case "1":
                show_balance(balance)
            case "2":
                balance = deposit(balance)
                users[username]["balance"] = balance
                with open("users.json", "w") as f:
                    json.dump(users, f)
            case "3":
                balance = withdraw(balance)
                users[username]["balance"] = balance
                with open("users.json", "w") as f:
                    json.dump(users, f)
            case "4":
                is_running = False
            case _:
                print("\nNot valid choice pick again.\n")

if __name__ == '__main__':
    main()