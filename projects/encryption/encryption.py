#Encrypt any messages
#And able to decrypt the same encrpted message
#Bonus: Save encrypted messages into json

import string
import random
import json

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)
key = chars.copy()

def encryption():
    random.shuffle(key)
    user_input = input("Enter message to encrypt: ")
    cipher_text = ""
    for letter in user_input:
        index = chars.index(letter)
        cipher_text += key[index]
    print(f"Encrypted text: {cipher_text}")
    return cipher_text, key, user_input

def decryption():
    cipher_text = input("Enter message to decrypt: ")
    try:
        with open("keys.json","r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        print("No log file found.")
        return
    
    for keys, messages in logs.items():
        if messages["encrypted"] == cipher_text:
            key = list(keys)
            user_input = ""
            for letter in cipher_text:
                index = key.index(letter)
                user_input += chars[index]
            print(f"Decrypted message: {user_input}")
            return
    print("Message not found in logs.")

def logs(cipher_text, key, user_input):
    try:
        with open("keys.json","r") as f:
            keys = json.load(f)
    except FileNotFoundError:
            keys = {}
    keys["".join(key)] = {"encrypted": cipher_text , "original text": user_input}

    with open("keys.json", "w") as f:
        json.dump(keys, f, indent=1)    

def main():
    is_running = True
    while is_running:
        print("Welcome to Cutest Encryptions")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose your options (1-3): ")
        if choice == "1":
            cipher_text, user_input, key = encryption()
            logs(cipher_text, user_input, key)
        elif choice == "2":
            decryption()
        elif choice == "3":
            is_running = False
        else:
            print("Invalid Input.")
        
        
            
        

if __name__ == '__main__':
    main()
        