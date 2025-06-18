import time
timer = int(input("Enter the time to countdown from in seconds: "))

for countdown in reversed(range(0,timer+1)):
    #This formula means that after taking away minutes in the input and whats the seconds left over
    seconds = countdown % 60
    #This formula means that after taking away hours in the input and whats the minutes left over
    minutes = int( countdown / 60 ) % 60
    #This formula just gets the hours
    hours = int(countdown / 3600)
    print(f"{hours:02}:{minutes:02}:{seconds:02}")
    time.sleep(1)

print("TIMES UP!")