import pygame
import RPi.GPIO as GPIO
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Servo Control")

# Set up colors
WHITE = (255, 255, 255)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz frequency
pwm.start(0)

# Function to set servo angle
def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

# Main game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

try:
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Update the display
        pygame.display.flip()

        # Control servo based on time
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # Convert to seconds

        if elapsed_time < 1:
            set_servo_angle(0)
        elif 1 <= elapsed_time < 3:
            set_servo_angle(90)
        elif 3 <= elapsed_time < 5:
            set_servo_angle(0)
        elif elapsed_time >= 5:
            start_time = current_time  # Reset the cycle

        # Control the frame rate
        clock.tick(30)

finally:
    pwm.stop()
    GPIO.cleanup()
    pygame.quit()
