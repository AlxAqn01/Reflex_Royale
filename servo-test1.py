import pygame
import RPi.GPIO as GPIO
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Servo Control Demo")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
current_angle = 90  # Start at middle position

try:
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_angle > 0:
                    current_angle -= 10
                elif event.key == pygame.K_RIGHT and current_angle < 180:
                    current_angle += 10
                set_servo_angle(current_angle)

        # Clear the screen
        screen.fill(WHITE)

        # Draw a line to represent servo position
        line_start = (WIDTH // 2, HEIGHT // 2)
        angle_rad = pygame.math.Vector2().from_polar((100, -current_angle + 90))
        line_end = (line_start[0] + angle_rad.x, line_start[1] + angle_rad.y)
        pygame.draw.line(screen, RED, line_start, line_end, 5)

        # Draw text to show current angle
        font = pygame.font.Font(None, 36)
        text = font.render(f"Angle: {current_angle}", True, BLACK)
        screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.Clock().tick(60)

finally:
    pwm.stop()
    GPIO.cleanup()
    pygame.quit()
