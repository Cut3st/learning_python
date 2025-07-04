#Basically movie theatre menu   
#List the items available
#Allow the user to order the item and calculate the total price they have to pay
menu = {"POPCORN": 5.00,
        "HOTDOGS": 4.50,
        "FRIES": 6.00,
        "ICECREAM": 3.50,
        "NUGGETS": 6.50,
        "CHIPS": 5.50,
        "SODA": 4.00,
        "WATER": 2.50}
total = 0.00
orders = []
print("-------------MENU-------------")
for key, value in menu.items():
    print(f"{key:10}: ${value:.2f}")
    
while True:
    print()
    order = input("What would you like to have? (q to quit): ").upper()
    if order == "Q": 
        break
    elif menu.get(order) is not None:
        orders.append(order)
    elif menu.get(order) is None:
        print()
        print("❌ Item is not on the menu.")

for order in orders:
    total += menu.get(order, 0.0)

print("-----------RECIEPT-----------")
print()
if not orders:
    print("❌ NO ITEMS")
else:
    for i in range(len(orders)):   
        print(f"{i+1}. {orders[i]}")

print()
print(f"TOTAL: ${total}")

    