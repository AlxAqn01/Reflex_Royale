import pygame
import RPi.GPIO as GPIO
from button import Button

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
SERVO_PIN = 27
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz frequency
pwm.start(0)

start_img = pygame.image.load('assets/start_but.png').convert_alpha()
start_button = Button(100,400, start_img, 1)
but_pressed = False

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
        

        if start_button.draw(screen):
            if not but_pressed:
                set_servo_angle(0)
                but_pressed = True
            else: 
                set_servo_angle(90)
                but_pressed = False

        # Control the frame rate
        clock.tick(30)

finally:
    pwm.stop()
    GPIO.cleanup()
    pygame.quit()
