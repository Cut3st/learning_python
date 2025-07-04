import random

dice_art = {
    1: ("┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
        ),
    2: ("┌─────────┐",
        "│ ●       │",
        "│         │",
        "│       ● │",
        "└─────────┘"
        ),
    3: ("┌─────────┐",
        "│ ●       │",
        "│    ●    │",
        "│       ● │",
        "└─────────┘"
        ),
    4: ("┌─────────┐",
        "│ ●     ● │",
        "│         │",
        "│ ●     ● │",
        "└─────────┘"
        ),
    5: ("┌─────────┐",
        "│ ●     ● │",
        "│    ●    │",
        "│ ●     ● │",
        "└─────────┘"
        ),
    6: ("┌─────────┐",
        "│ ●     ● │",
        "│ ●     ● │",
        "│ ●     ● │",
        "└─────────┘"
        )
    }
dice = []
total = 0
num_of_dice = int(input("How many dices?: "))

#You generate the user inputted amount of dices and have the die number of each die added to the dice list
for die in range(num_of_dice): 
    dice.append(random.randint(1, 6))

#For all 5 lines of the ACSII dice art to be printed
for line in range(5):
    #Loop will go through each die face user rolled, lets say example number 5 in the list
    for die in dice:
        #dice_art.get(5) gets the dice art(value) from key 5. 
        #[line] tells the program which line to print from the key 5 art
        #this "line" aligns with the initial for loop amount
        print(dice_art.get(die)[line], end="")
    print()

for die in dice:
    total += die
print(f"Total: {total}")