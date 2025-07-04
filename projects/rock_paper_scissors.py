import random
#Best of three rock paper scissors
options = ("rock", "paper", "scissors")
while True:
    wins = 0
    losses = 0
    round = 1
    player = None
    while wins < 2 and losses < 2:
        option = random.choice(options)
        print()
        guess = input("ROCK✊, PAPER🖐️, SCISSORS✌️? ").lower()
        print()
        if guess == option:
           print(f"🤝 YOU DRAW ROUND {round}")
        elif guess == "rock" and option == "scissors":
            print(f"✅ YOU WIN ROUND {round}.")
            wins += 1
        elif guess == "paper" and option == "rock":
            print(f"✅ YOU WIN ROUND {round}.")
            wins += 1
        elif guess == "scissors" and option == "paper":
            print(f"✅ YOU WIN ROUND {round}.")
            wins += 1
        else:
            print(f"❌ YOU LOST ROUND {round}.")
            losses += 1
        print()
        print(f"🙂 PLAYER: {guess}")
        print(f"🤖 COMPUTER: {option}\n")
        round += 1
    if wins == 2:
        print("🎊 YOU WIN THE BEST OF 3!\n")
    elif losses == 2:
        print("😿 YOU LOST THE BEST OF 3!\n")
    if not input("Would you want to play another round? (Y/N): ").upper() == "Y":
        print()
        print("😄 Thanks for playing!")
        break
    