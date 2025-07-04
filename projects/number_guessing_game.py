import random
#User will guess the randomly generated number between 1 - 100
low = 1
high = 100
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
        print("📉 Your guess is too low try again!\n")
    elif guess > answer:
        print()
        print("📈 Your guess is too high try again!\n")    
    else:
        print()
        print(f"✅ {answer}! YOU'VE GUESS CORRECTLY WELL DONE!")
        print(f"You guessed {guesses} times before getting it right!")
        break
    