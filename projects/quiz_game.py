#List of questions
questions = ("What is the capital city of France?",
             "Which planet is known as the Red Planet?",
             "What is 5 + 3?",
             "Which animal is known as the King of the Jungle?",
             "What is the boiling point of water at standard atmospheric pressure?")
#2D collection of choices
choices = (("A. Berlin", "B. Madrid", "C. Paris", "D. Rome"),
           ("A. Earth", "B. Mars", "C. Jupiter", "D. Venus"),
           ("A. 6", "B. 7", "C. 8", "D. 9"),
           ("A. Tiger", "B. Elephant", "C. Lion", "D. Cheetah"),
           ("A. 100°C", "B. 90°C", "C. 120°C", "D. 80°C"))
#List of answers
answers = ("C", "B", "C", "C", "A")
#Empty List of Guesses
guesses = []
question_num = 0
score = 0

#Whilst 0 < 4 Length of questions is (0-4)
while question_num < len(questions):
        print("------------------------------------------------------------")
        print(questions[question_num])
        print()
        #For the list in choices number 0 (Initially)
        for choice in choices[question_num]:
            print(choice)
        #User input in convertted to uppercase
        guess = input("\nPlease select your answer: ").upper()
        #Add guess to guesses list
        guesses.append(guess)
        #Check if guess was an alphabet and whether it was A, B, C or D
        if guess.isalpha() and guess in ("A", "B", "C", "D"):
            #Check if the guess is the same as the answer for that question
            if guess == answers[question_num]:
                score += 1
                print("\n✅ CORRECT ANSWER\n")
            else:
                 print("\n❌ WRONG ANSWER\n")
            #User move on to next question only if answer is an alphabet within choice range 
            #And determined if it is correct or wrong answer
            question_num += 1
        else:
            #If user did not type an alphabet or did not choose A, B, C or D
            print("\n❌Invalid Input Choose (A, B, C, D)\n")
            #Invalid inputs will not be added to guesses list
            guesses.remove(guess)
        
print("------------------------------------------------------------")
print("                          RESULTS                           ")
print("------------------------------------------------------------")
#Print out original answers
print("ANSWERS: ", end="")
for answer in answers:
    print(answer, end=" ")

#Print out user's guesses
print("\nGUESSES: ", end="")
for guess in guesses:
    print(guess, end=" ")

percentage = (score/question_num) * 100
print(f"\n\nYou scored: {score}/{question_num} ({percentage: .1f}%)              ")
print("------------------------------------------------------------")    
