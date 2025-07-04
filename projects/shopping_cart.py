items = []
prices = [0.0] #Make sure the list is made of floats only
prices.pop() # Removes the starter value; list is now empty
total = 0

while True:
    item = input("Enter your selected item (Type 'Q' to quit): ").upper()
    #Make sures no matter lower or upper case input it'll prompt the break
    if item == "Q":
        break
    else:
        items.append(item)
        price = float(input("Enter the prices of the item: $"))
        prices.append(price)

total = sum(prices)
print("---------- RECIEPT ----------")
#Completed this with the help of Copilot but with my ideas
#Items will get listed such as it is:
#1.
#2.
#3.
#len() should be used to get the items range for for loop based on how many items there are in the list
#{item[i]} and {prices[i]} will display the items respectively based on the list order from 0 - end of list
for i in range(len(items)):
	print(f"{i+1}. {items[i]} - ${prices[i]}")
    
print("\n")
print(f"TOTAL: ${total: .2f}")
