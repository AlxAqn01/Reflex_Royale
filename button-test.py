import pygame
import RPi.GPIO as GPIO

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button and LED Demo")

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 18
LED_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# Main game loop
running = True
led_state = False

try:
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read button state
        button_state = GPIO.input(BUTTON_PIN)

        # Update LED state based on button
        if button_state == GPIO.LOW:  # Button is pressed
            led_state = True
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            led_state = False
            GPIO.output(LED_PIN, GPIO.LOW)

        # Clear the screen
        screen.fill(WHITE)

        # Draw a circle to represent the LED
        if led_state:
            pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), 50)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)

finally:
    pygame.quit()
    GPIO.cleanup()
