import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
BUTTON_PIN = 18
LED_PIN = 17

# Set up pins
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        # Read button state
        button_state = GPIO.input(BUTTON_PIN)
        
        # If button is pressed (it will read LOW due to pull-up resistor)
        if button_state == GPIO.LOW:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
        else:
            GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
        
        time.sleep(0.01)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    GPIO.cleanup()  # Clean up GPIO on normal exit
