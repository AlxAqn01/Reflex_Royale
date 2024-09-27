import pygame
import sys
import random
from button import Button
import RPi.GPIO as GPIO

# Initialize pygame
pygame.init()
pygame.mixer.init()
Running = True

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for buttons and LEDs
player1_buttons = {'RED': 14, 'YELLOW': 15, 'GREEN': 18, 'WHITE': 23, 'BLUE': 24}
player1_leds = {'RED': 4, 'YELLOW': 17, 'GREEN': 27, 'WHITE': 22, 'BLUE': 10}
player2_buttons = {'RED': 25, 'YELLOW': 8, 'GREEN': 7, 'WHITE': 1, 'BLUE': 12}
player2_leds = {'RED': 9, 'YELLOW': 11, 'GREEN': 0, 'WHITE': 5, 'BLUE': 6}

# Set up GPIO pins
for pin in player1_buttons.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in player2_buttons.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in player1_leds.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
for pin in player2_leds.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Screen dimensions
width, height = 1024, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Reflex Royale')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Game states
MENU, SELECT, RULES, GAME, READY, SCORING, TIEBREAK, WINNER = 0, 1, 2, 3, 4, 5, 6, 7
app_state = MENU
NOT_SET, EASY, MEDIUM, HARD = 0, 1, 2, 3
diffculty_set = NOT_SET
current_round = 1
max_round = False
player1_score, player2_score = 0, 0
prev_p1score, prev_p2score = 0, 0
player_scored = False
player1_pressed = False
player2_pressed = False
invert_input = False
play_once_sfx = False

# ... [rest of the initialization code remains the same] ...

def reset_leds_and_buttons():
    global player1_pressed, player2_pressed
    for led in player1_leds.values():
        GPIO.output(led, GPIO.LOW)
    for led in player2_leds.values():
        GPIO.output(led, GPIO.LOW)
    player1_pressed = False
    player2_pressed = False

def game_screen_and_timers():
    global current_word, state_start_time, current_round, app_state, text_color, has_player_scored, new_bg_color, round_duration, max_round, play_once_sfx
    global player_scored, player1_pressed, player2_pressed, prev_p1score, prev_p2score, invert_input

    current_time = pygame.time.get_ticks()

    # Check if the round is over
    if current_time - state_start_time > round_duration:
        app_state = SCORING
        current_round += 1
        state_start_time = current_time
        has_player_scored = False
        text_color = None
        new_bg_color = None
        player_scored = False
        reset_leds_and_buttons()
        play_once_sfx = False
        return

    # ... [rest of the game_screen_and_timers code] ...

    if diffculty_set == EASY:
        # ... [EASY difficulty code] ...
    elif diffculty_set == MEDIUM:
        if current_round <= 3:
            round_duration = 3000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <= 6:
            round_duration = 2000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round > 6:
            if current_round == 7:
                if not play_once_sfx:
                    word_sfx.play()
                    play_once_sfx = True
            round_duration = 3000
            current_color = text_color
            screen.fill(black)
            invert_input = True
        if current_round == 9:
            max_round = True
    elif diffculty_set == HARD:
        # ... [HARD difficulty code] ...

    # ... [rest of the game_screen_and_timers code] ...

def handle_button_press():
    global player_scored, player1_score, player2_score, player1_pressed, player2_pressed, invert_input
    
    color_word = get_word_by_color(text_color)

    if not player_scored:
        # Check Player 1 buttons
        for color, pin in player1_buttons.items():
            if not GPIO.input(pin) and not player1_pressed:
                player1_pressed = True
                GPIO.output(player1_leds[color], GPIO.HIGH)
                if not invert_input:
                    if color == current_word:
                        player_scored = True
                        player1_score += 1
                elif invert_input:
                    if color == color_word:
                        player_scored = True
                        player1_score += 1

        # Check Player 2 buttons
        for color, pin in player2_buttons.items():
            if not GPIO.input(pin) and not player2_pressed:
                player2_pressed = True
                GPIO.output(player2_leds[color], GPIO.HIGH)
                if not invert_input:
                    if color == current_word:
                        player_scored = True
                        player2_score += 1
                elif invert_input:
                    if color == color_word:
                        player_scored = True
                        player2_score += 1

def right_wrong():
    global player1_score, player2_score, prev_p1score, prev_p2score, app_state, state_start_time, max_round, play_once_sfx
    
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time
    wait_time = 3000
    
    if elapsed_time >= wait_time:
        if max_round == False:    
            app_state = GAME
        elif max_round:
            if player1_score == player2_score:
                app_state = TIEBREAK
            else:
                play_once_sfx = False
                app_state = WINNER
        state_start_time = current_time
        reset_leds_and_buttons()
        return
    
    # ... [rest of the right_wrong code] ...

# Main loop
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GPIO.cleanup()
            pygame.quit()
            sys.exit()

    if app_state == MENU:
        if not music_playing:
            pygame.mixer.music.play(-1)
            music_playing = True
        menu_screen()

        if start_button.draw(screen):
            app_state = SELECT

        if exit_button.draw(screen):
            GPIO.cleanup()
            pygame.quit()
            sys.exit()

    elif app_state == SELECT:
        set_difficulty()
        if diffculty_set == NOT_SET:
            if easy_button.draw(screen):
                diffculty_set = EASY
            if medium_button.draw(screen):
                diffculty_set = MEDIUM
            if hard_button.draw(screen):
                diffculty_set = HARD
                
        if diffculty_set != NOT_SET:
            app_state = GAME
            state_start_time = pygame.time.get_ticks()
        
        if back_button.draw(screen):
            app_state = MENU

    elif app_state == GAME:  
        game_screen_and_timers()
        handle_button_press()

    elif app_state == SCORING:  
        right_wrong()

    pygame.display.flip()
    clock.tick(60)

# Cleanup GPIO on exit
GPIO.cleanup()
