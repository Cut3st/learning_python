questions = ("What is the capital city of France?",
             "Which planet is known as the Red Planet?",
             "What is 5 + 3?",
             "Which animal is known as the King of the Jungle?",
             "What is the boiling point of water at standard atmospheric pressure?")
choices = (("A. Berlin", "B. Madrid", "C. Paris", "D. Rome"),
           ("A. Earth", "B. Mars", "C. Jupiter", "D. Venus"),
           ("A. 6", "B. 7", "C. 8", "D. 9"),
           ("A. Tiger", "B. Elephant", "C. Lion", "D. Cheetah"),
           ("A. 100°C", "B. 90°C", "C. 120°C", "D. 80°C"))
answers = ("C", "B", "C", "C", "A")
guesses = []
question_num = 0
score = 0
while question_num < len(questions):
        print("------------------------------------------------------------")
        print(questions[question_num])
        print()
        for choice in choices[question_num]:
            print(choice)
        guess = input("\nPlease select your answer: ").upper()
        guesses.append(guess)
        if guess.isalpha() and guess in ("A", "B", "C", "D"):
            if guess == answers[question_num]:
                score += 1
                print("\n✅ CORRECT ANSWER\n")
            else:
                 print("\n❌ WRONG ANSWER\n")
            question_num += 1
        else:
            print("\n❌Invalid Input Choose (A, B, C, D)\n")
            guesses.remove(guess)
        
print("------------------------------------------------------------")
print("                          RESULTS                           ")
print("------------------------------------------------------------")
print("ANSWERS: ", end="")
for answer in answers:
    print(answer, end=" ")

print("\nGUESSES: ", end="")
for guess in guesses:
    print(guess, end=" ")

percentage = (score/question_num) * 100
print(f"\n\nYou scored: {score}/{question_num} ({percentage: .1f}%)              ")
print("------------------------------------------------------------")    
