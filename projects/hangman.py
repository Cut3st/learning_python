from wordlist import words
import random
hangman_art = {0: ("|───",
                   "|   ",
                   "|   ",
                   "|   "),
               1: ("|─|─",
                   "| 😶 ",
                   "|   ",
                   "|   "),
               2: ("|─|─",
                   "| 😐 ",
                   "| | ",
                   "|   "),
               3: ("|─|─",
                   "| 😟 ",
                   "|/| ",
                   "|   "),
               4: ("|─|─",
                   "| 😢 ",
                   "|/|\\",
                   "|   "),
               5: ("|─|─",
                   "| 😭 ",
                   "|/|\\",
                   "|/  "),
               6: ("|─|─",
                   "| 💀 ",
                   "|/|\\",
                   "|/ \\")}

def print_hangman(wrong_guesses):
    print()   
    for line in hangman_art[wrong_guesses]:
            print(line)
    print()
            
def print_hint(hint):
    print("Hint:", end=" ")
    print(" ".join(hint))
    
def print_answer(answer):
    print("Answer:", end=" ")
    print(" ".join(answer))

def main():
    is_running = True
    wrong_guesses = 0
    guessed_letters = set()
    answer = random.choice(words)
    hint = ["_"] * len(answer)
    while is_running:
        print_hangman(wrong_guesses)
        print_hint(hint)
        guess = input("Guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("\n❌ Invalid Input")
            continue
        if guess in guessed_letters:
            print(f"You have already guessed {guess}.")
            continue
        
        guessed_letters.add(guess)
    
        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            wrong_guesses +=1
                
        if "_" not in hint:
            print_hangman(wrong_guesses)
            print_answer(answer)
            print("🎊 YOU WIN!")
            is_running = False
        elif wrong_guesses >= 6:
            print_hangman(wrong_guesses)
            print_answer(answer)
            print("🪦  GAME OVER")
            is_running = False   

if __name__ == '__main__':
    main()