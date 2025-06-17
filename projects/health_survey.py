#Getting the user temperature in (C/F), weight(kg/lb) and height.

temp = float(input("What is your temperature?" ))
temp_unit = input("In Celcius (C) or Ferenhiet (F): ")
qns1 = input("Would you like to convert the following to the other (Y/N)? ")
if qns1 == "Y":
    if temp_unit == "C":
        temp = ((9/5) * temp) + 32
    elif temp_unit == "F":
        temp = ((5/9) * temp) - 32
elif qns1 != "N":
    print("Invalid Input use Y/N only")

#Askiing the user for their weight, and converting from kg to lb or lb to kg
weight = float(input("What is your weight? "))
weight_unit = input("Is it in kg/lb? ")
qns2 = input("Would you like to convert the following to the other (Y/N)? ")
if qns2 == "Y":
    if weight_unit == "kg":
        weight = weight * 2.205
        weight_unit = "lb"
    elif weight_unit == "lb":
        weight = weight / 2.205
        weight_unit = "kg"
elif qns2 != "N":
    print("Invalid Input use Y/N only")

#Asking the user for their height, and converting from ft to cm or cm to ft
height = float(input("What is your height? "))
height_unit = input("Is it in cm/ft? ")
qns3 = input("Would you like to convert the following to the other (Y/N)? ")
if qns3 == "Y":
    if height_unit == "cm":
        height = height / 30.48
        height_unit = "ft"
    elif height_unit == "ft":
        height = height * 30.48
        height_unit = "cm"
elif qns3 != "N":
    print("Invalid Input use Y/N only")

#Converting the weight back to kg and height to cm for BMI calculation
if weight_unit == "lb":
    weight = weight / 2.205
if height_unit == "ft":
    height = height * 30.48
bmi = weight / ((height/100) ** 2)

#Final results printed out
print(f"Your give height is {height: .2f} cm/ft, weight is {weight: .2f} kg/lbs.")
if temp > 40:
    print(f"Temperature taken is {temp: .1f} F. ")
elif temp <= 40:
    print(f"Temperature taken is {temp: .1f} F. ")
print(f"BMI calculated to be {bmi: .2f}.")

