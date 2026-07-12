import time
import threading
from time import sleep 

# Hal Layers
from hal import hal_keypad as Keypad
from hal import hal_lcd as LCD

# Implementation of Parent Class
class Menu():
    def __init__(self):
        self.lcd = LCD.lcd()
        self.pressed = []
        self.last_activity = time.time()
        self.low_power = False
        self.idle_timeout = 10

        Keypad.init(self.on_key_pressed)
        self.keypad_thread = threading.Thread(target = Keypad.get_key, daemon = True)
        self.idle_thread = threading.Thread(target=self.idle_check, daemon = True)

    def startkeypt(self):
        self.keypad_thread.start()
        self.idle_thread.start()
        self.welcome()
        while True:
            sleep(0.1)
    
    def idle_check(self):
        while True:
            elapsed = time.time() - self.last_activity
            if elapsed >= self.idle_timeout and not self.low_power:
                self.enter_low_power()
            sleep(0.5)

    def enter_low_power(self):
        self.low_power = True
        self.lcd.lcd_display_string("Entering Low Power",1)
        self.lcd.lcd_display_string("Goodbye!",2)
        time.sleep(5)

        self.lcd.backlight(0)

    def exit_low_power(self):
        self.low_power = False
        self.lcd.backlight(1)
        self.last_activity = time.time()




# Implementation of Child class
class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        self.state = "w"
        
    
    def welcome(self):
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("Welcome to the",1)
        self.lcd.lcd_display_string("VLSLPM!",2)
        time.sleep(1)
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("Press 0 to start",1)

    def show_main_menu(self):
        self.state = "1mm"
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("1. Ctrl Car Sys",1)
        self.lcd.lcd_display_string("2. Monit. Car Sys",2)
    
    def on_key_pressed(self,key):
        self.pressed.append(key)
        print(self.pressed)
        print(self.pressed[-1])

        if self.low_power:
            self.exit_low_power()
            return
        
        self.last_activity = time.time()

        if self.state == "w":
            if self.pressed[-1] == 0:
                self.show_main_menu()

    




    

if __name__ == "__main__":
   start = StartMenu()
   start.startkeypt()