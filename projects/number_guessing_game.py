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
        print(f"Your guess is not within range please guess within {low} and {high}.")
    elif guess < answer:
        print("📉 Your guess is too low try again!")
    elif guess > answer:
        print("📈 Your guess is too high try again!")    
    else:
        print(f"\n✅{answer}! YOU'VE GUESS CORRECTLY WELL DONE!")
        print(f"You guessed {guesses} times before getting it right!")
        break
    