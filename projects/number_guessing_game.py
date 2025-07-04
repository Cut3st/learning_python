import random
#User will guess the randomly generated number between 1 - 100
low = 1
high = 100
#Makes it so the random number can be regenerated for user to play over and over
while True:
    answer = random.randint(low,high)
    guesses = 0

    while True:
        guesses += 1
        guess = int(input("Guess the random number between 1 - 100: "))
        if guess < low or guess > high:
            print()
            print(f"Your guess is not within range please guess within {low} and {high}.\n")
        elif guess < answer:
            print()
            print("📉 Too low try again!\n")
        elif guess > answer:
            print()
            print("📈 Too high try again!\n")    
        else:
            print()
            print(f"✅ {answer}! YOU'VE GUESS CORRECTLY WELL DONE!")
            print(f"You guessed {guesses} times before getting it right!")
            break
    play_again = input("Would you like to play again? (Y/N):" ).upper()
    if play_again != "Y":
        break
    