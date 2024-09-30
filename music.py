import pygame
from button import Button

# Initialize Pygame and Pygame mixer
pygame.init()
pygame.mixer.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music")

# Set up colors
WHITE = (255, 255, 255)

# Load the button image
start_img = pygame.image.load('assets/start_but.png').convert_alpha()
start_button = Button(100, 400, start_img, 1)

# Load the music file (located in the assets folder)
sound = None  # Initialize sound object

but_pressed = False
music_playing = False  # Track music state

# Function to play or stop music
def toggle_music():
    global sound, music_playing
    if music_playing:
        if sound:
            sound.stop()  # Stop the current sound
        music_playing = False
    else:
        sound = pygame.mixer.Sound('assets/driftveilWAV.wav')  # Load and play the sound
        sound.play()
        music_playing = True

# Main game loop
running = True
clock = pygame.time.Clock()

try:
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Check if start button is pressed
        if start_button.draw(screen):
            if not but_pressed:
                toggle_music()  # Toggle music on button press
                but_pressed = True
        else:
            but_pressed = False  # Reset the button state

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

finally:
    pygame.quit()
