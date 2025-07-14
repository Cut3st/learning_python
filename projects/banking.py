#Python Banking Program, includes, show balance, deposit, withdraw, exit
import time
#Registration

# #Login

#Banking Choice

def show_balance(balance):
    print("\n=======================")
    print(f"Balance: ${balance:.2f}")
    print("=======================\n")
    time.sleep(1)

def deposit(balance):
    amount = float(input("\nHow much would you like to deposit? "))
    if amount < 0:
        print("Invalid amount")
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
        print("Insufficient Funds.")
    else:
        balance -= amount
        print("\n=======================")
        print(f"Withdraw: -${amount}")
        print(f"New Balance: ${balance:.2f}")
        print("=======================\n")  
        time.sleep(1)
    return balance

def main():
    balance = 0
    is_running = True
    choices = ("Balance", "Deposit", "Withdraw", "Exit")
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
            case "3":
                balance = withdraw(balance)
            case "4":
                is_running = False
            case _:
                print("\nNot valid choice pick again.\n")

if __name__ == '__main__':
    main()