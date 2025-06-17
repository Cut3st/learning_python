#Validate User Input Exercise
#1. Username is no more than 12 characters
#2. Username must not contain spaces
#3. Username must not contain digits
while True:
    username = input("Please type your preferred username: ")
    if len(username) > 12:
        print("Your username cannot contain more than 12 characters.")
    elif not username.find(" ") == -1:
        print("Your username cannot contain spaces.")
    elif not username.isalpha():
        print("Your username cannot contain numbers/special characters.")
    else:
        print(f"You have chosen {username} as your username.")
        break
