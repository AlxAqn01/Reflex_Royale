import RPi.GPIO as GPIO
import time

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin we'll be using
PIN = 18  # You can change this to any available GPIO pin

# Function to set up the pin as an input (for button)
def setup_input():
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to set up the pin as an output (for LED)
def setup_output():
    GPIO.setup(PIN, GPIO.OUT)

try:
    while True:
        # Set up as input to read button
        setup_input()
        time.sleep(0.01)  # Short delay for stability
        
        # Read button state
        button_state = GPIO.input(PIN)
        
        # If button is pressed (it will read LOW)
        if button_state == GPIO.LOW:
            # Set up as output to control LED
            setup_output()
            GPIO.output(PIN, GPIO.HIGH)  # Turn on LED
            time.sleep(0.05)  # Debounce delay
        else:
            # Set up as output and turn off LED
            setup_output()
            GPIO.output(PIN, GPIO.LOW)
        
        time.sleep(0.01)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()  # Clean up GPIO on normal exit
