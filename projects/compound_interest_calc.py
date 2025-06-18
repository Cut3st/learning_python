#Python compound interest calculator
#A = P * (1 + r/n)**t
#A = Final Amount
#P = Initial principal balance
#r = Interest rate 
#t = number of time period elapsed (years) 
#n = how often is interest compound (monthly, quarterly, yearly)

while True:
    principle = float(input("Please input your initial balance: "))
    if principle < 0:
        print("Principle cannot be less than 0.")
    else:
        break
while True:
    interest = float(input("What is the annual interest on balance: "))
    if interest < 0:
        print("Interest cannot be lower than 0%.")
    else:
        interest = interest / 100
        break
while True:
    time = int(input("How many years has it been? "))
    if time < 0:
        print("Years passed cannot be lower than 0.")
    else:
        break
    
while True:
    compound = input("How often (monthly, quarterly, annually) is your interest compounded? ")
    if compound == "monthly":
        compound_months = 12
        ctime = time * compound_months
        break
    elif compound == "quarterly":
        compound_months = 4
        ctime = time * compound_months
        break
    elif compound == "annually":
        compound_months = 1
        ctime = time * compound_months
        break
    else:
        print("Please enter either, monthly, quarterly and annually.")
    
result = principle * (1 + (interest/compound_months))**ctime
print(f"Your final sum after {time} years with a {compound} interest of {interest*100}% is ${result:5,.250f}")