from gpiozero import Button
from signal import pause

# Define the button with pull-up resistor
button = Button(12, pull_up=True)

def button_pressed():
    print("Button pressed!")

# Attach the button press event to the function
button.when_pressed = button_pressed

# Keep the program running
pause()
