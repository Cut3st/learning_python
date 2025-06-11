import math
#My first ever calculator in Python 11th June 2025 (I hope to make my own GUI calculator in the future)
while True:
    operator = input("What would you like to calculate today? (+, -, *, /, sqrt, circle, expo): " )
    if operator == "":
        print("You did not enter an operator.")
    elif operator == "+":
        num1 = float(input("Select your first number: "))
        num2 = float(input("Select your second number: "))
        result = num1 + num2
        
    elif operator == "-":
        num1 = float(input("Select your first number: "))
        num2 = float(input("Select your second number: "))
        result = num1 - num2  
        
    elif operator == "*":
        num1 = float(input("Select your base number: "))
        num2 = float(input("Select the number to multiply by: "))
        result = num1 * num2
        
    elif operator == "/":
        num1 = float(input("Select your base number: "))
        num2 = float(input("Select the number to divide by: "))
        result = num1 / num2
        
    elif operator == "sqrt":
        num1 = float(input("Select your number: "))
        result = math.sqrt(num1)  
         
    elif operator == "circle":
        circle_result = input("Would you like to find it's circumference (C), area (A) or diameter (D): ")
        if circle_result == "A":
            dimensions = input("Would you like to use the radius (R) or diameter (D) or circumference (C)?")
            if dimensions == "R":
                radius = float(input("Enter the radius: "))
                result = math.ceil(math.pi * pow(radius, 2))
            elif dimensions == "D":
                diameter = float(input("Enter the diameter: "))
                result = math.ceil((math.pi * pow(diameter, 2))/4)
            elif dimensions == "C":
                circumferece = float(input("Enter the circumference: "))
                result = math.ceil((pow(circumferece,2))/(4*math.pi))       
    elif operator == "expo":
        num1 = float(input("Select your base number: "))
        num2 = float(input("Select your exponent: "))
        result = pow(num1, num2)
                
    print(f"Result: {result}")
    cont = input("Would you like to continue?(Y/N) ")
    if cont != "Y":
     print("Thank you for using the calculator!")
     break