import time
import datetime
import pygame

def validate_time_format(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False
    
def set_alarm(alarm_time):
    print(f"\n⏰ Alarm set at {alarm_time}")
    sound_file = "my_music.mp3"
    is_running = True
    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)
        time.sleep(1)
        if current_time == alarm_time:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play(start=15)
            
            time.sleep(10)
            pygame.mixer.music.stop()
            is_running = False
            print("TIMES UP!! ⏰")
            
            
    
if __name__ == "__main__":
    
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current Time: {now}")
        alarm_time = input("Set your Alarm (HH:MM:SS): ")
        if not validate_time_format(alarm_time):
            print("\n⚠️ Invalid format. Please use HH:MM:SS.\n")
            continue 
        if alarm_time <= datetime.datetime.now().strftime("%H:%M:%S"):
            print("\n❌ Alarm is past current time.\n")
            continue
        else:
            set_alarm(alarm_time)
        exit = input("\nAnother Alarm? (Y/N): ")
        if exit != "Y":
            break
    
    
    

   
                   
                   
