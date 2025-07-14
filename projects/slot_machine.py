#🍒🍉🍋7️⃣⭐
#User will have balance, ask them to top up at the start
#Symbols will be randomised, 3 will be displayed at once
#payouts, 💰💰💰 - x50, 🍒🍒🍒 x20, 🍋🍋🍋 x 10, 🍒🍒⭐ (two of a kind) x5

import random

def spin():
    symbols = ['🍒', '🍉', '🍋', '💰', '⭐']
    return [random.choice(symbols) for _ in range(3)]
def print_spin(row):
    print(" | ".join(row))

def payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '💰':
            return bet * 50
        elif row[0] == "🍒":
            return bet * 20
        elif row[0] == "🍋":
            return bet * 5
    elif row[0] == row[1] and row[0] != row[2] or \
     row[0] == row[2] and row[0] != row[1] or \
     row[1] == row[2] and row[1] != row[0]:
        return bet * 2
        


def topup(balance):
    topup = float(input("How much would you like to topup? $"))
    if topup <= 0:
        print("Invalid amount.")
    else:
        balance += topup
        print(f"Topup: +${topup}")
        print(f"Your new balance is ${balance}")
    return balance

def main():
    is_running = True
    menu = ("Spin", "Help", "Balance/Topup", "Exit")
    balance = 0
    while is_running:
        print("Welcome to Cutest Slots")
        for items in range(len(menu)):
            print(f"{items+1}. {menu[items]}")
        choice = input("Please select your options(1-4): ")
        match choice:
            case "1":
                while True:
                    if balance == 0:
                        print("You have no money in your balance please topup!")
                        break
                    else:
                        bet = float(input("How much do you want to bet? "))
                        balance -= bet
                        row = spin()
                        print_spin(row)

                        pay = payout(row, bet)
                        if pay > 0:
                            print(f"You won ${pay}!")
                            balance += pay
                        elif pay == 0:
                            print(f"You lost!")
                    choice = input("Do you want to continue?(Y/N) ").upper()
                    if choice == "Y":
                        continue
                    else:
                        break

                
            case "2":
                print(f"{'RESULT':<9} {'OUTCOME':^} {'WINNINGS':>15}")
                print("=" * 35)
                print(f"{'💰💰💰':<6} {'Jackpot!':<15} {'x50':<10}")
                print(f"{'🍒🍒🍒':<6} {'Full match':<15} {'x20':<10}")
                print(f"{'🍋🍋🍋':<6} {'Full match':<15} {'x10':<10}")
                print(f"{'⭐🍒🍒':<6} {'Two of a kind':<15} {'x2':<10}")
                print(f"{'🔔🍋⭐':<6} {'No match':<15} {'x0':<10}")
            case "3":
                print(f"Balance: ${balance}")
                choice = input("Do you want to topup?(Y/N) ").upper()
                if choice == "Y":
                    balance = topup(balance)
                elif choice == "N":
                    continue
                else:
                    print("Invalid Choice (Y/N) only.")
            case "4":
                is_running = False
            case _:
                print("Invalid Input select 1-4 only.")

if __name__ == '__main__':
    main()

            