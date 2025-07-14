#🍒🍉🍋7️⃣⭐
#User will have balance, ask them to top up at the start
#Symbols will be randomised, 3 will be displayed at once
#payouts, 💰💰💰 - x50, 🍒🍒🍒 x20, 🍋🍋🍋 x 10, 🍒🍒⭐ (two of a kind) x5
import time
import random

def spin():
    symbols = ['🍒', '🍉', '🍋', '💰', '⭐']
    #Using list comprehension to generate the 3 random symbols
    return [random.choice(symbols) for _ in range(3)]

def print_spin(row):
    #Joins the elements in the list together with | inbetween
    print(" | ".join(row))

def payout(row, bet):
    #3 of a kind but each symbol has different values
    if row[0] == row[1] == row[2]:
        if row[0] == '💰':
            return bet * 50
        elif row[0] == '🍉':
            return bet *20
        elif row[0] == "🍒":
            return bet * 30
        elif row[0] == "🍋":
            return bet * 10
    #two of a kind
    elif row[0] == row[1] and row[0] != row[2] or \
     row[0] == row[2] and row[0] != row[1] or \
     row[1] == row[2] and row[1] != row[0]:
        return bet * 2
    else:
        return 0
        
def topup(balance):
    try:
        topup = float(input("\nHow much would you like to topup? $"))
        if topup <= 0:
            print("❌ Invalid amount.")
        else:
            balance += topup
            print(f"Topup: +${topup}")
            print(f"Your new balance is ${balance}")
    except ValueError:
        print("\n⁉️ Invalid input. Please enter a number.\n")
    return balance

def main():
    is_running = True
    menu = ("Spin", "Help", "Balance/Topup", "Exit")
    balance = 0
    while is_running:
        print("=" *20)
        print(f"{'🎰 CUTEST SLOTS 🎰':>17}")
        print("=" *20)
        #Prints the menu this looks nicer than just typing the menu
        #can add more menu in the future
        for items in range(len(menu)):
            print(f"{items+1}. {menu[items]}")
        choice = input("\nPlease select the options(1-4): ")
        match choice:
            #Slots spinning
            case "1":
                while True:
                    try:
                        print(f"\nBalance: ${balance}")
                        bet = float(input("How much do you want to bet? $"))
                        if balance == 0 or bet > balance:
                            print("\n❌ Insufficient funds, please topup!\n")
                            break
                        elif balance >= bet:
                            balance -= bet
                            
                            #Printing the 3 slot spins
                            row = spin()
                            print("\n⏳ Spinning...\n")
                            time.sleep(1)
                            print("=" *13)
                            print(f"{'CUTEST SLOTS':>12}")
                            print("=" * 13)
                            print_spin(row)
                            print("=" * 13)
                            
                            #Calculating the payout based on the spins result
                            pay = payout(row, bet)
                            if pay > 0:
                                print(f"\n🎊 You won ${pay}!\n")
                                balance += pay
                                print(f"Balance: ${balance}")
                            elif pay == 0:
                                print("\n😿 You lost!\n")
                                print(f"Balance: ${balance}")
                        choice = input("Do you want to continue?(Y/N): ").upper()
                        if choice != "Y":
                            break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    #Literally prints the result outcome and winnings menu         
            case "2":
                print("=" * 35)
                print(f"{'RESULT':<9} {'OUTCOME':^} {'WINNINGS':>15}")
                print("=" * 35)
                print(f"{'💰💰💰':<6} {'Jackpot!':<15} {'x50':<10}")
                print(f"{'🍒🍒🍒':<6} {'Full match':<15} {'x20':<10}")
                print(f"{'🍋🍋🍋':<6} {'Full match':<15} {'x10':<10}")
                print(f"{'⭐🍒🍒':<6} {'Two of a kind':<15} {'x2':<10}")
                print(f"{'🔔🍋⭐':<6} {'No match':<15} {'x0':<10}")
                time.sleep(5)
            #Balance
            case "3":
                print(f"\nBalance: ${balance}")
                choice = input("Do you want to topup?(Y/N): ").upper()
                if choice == "Y":
                    balance = topup(balance)
                elif choice == "N":
                    continue
                else:
                    print("Invalid Choice (Y/N) only.")
            #Exit
            case "4":
                is_running = False
            #Accept no other inputs
            case _:
                print("Invalid Input select 1-4 only.")

if __name__ == '__main__':
    main()

            