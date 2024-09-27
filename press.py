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
current_round = 6
max_round = False
player1_score, player2_score = 0, 0
prev_p1score, prev_p2score = 0, 0
player_scored = False
player1_pressed = False
player2_pressed = False
invert_input = False

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
purple = (127, 0, 255)

# Word-color pairs
words_color = ["RED", "YELLOW", "GREEN", "WHITE", "BLUE"]
color_map = {
    "RED": red,
    "YELLOW": yellow,
    "GREEN": green,
    "WHITE": white,
    "BLUE": blue,
}

# Clock to control frame rate
clock = pygame.time.Clock()

# Variables to manage text changing and timers
current_word = random.choice(words_color)
state_start_time = 0
round_duration = 2000  # 2 seconds
countdown_duration = 3000  # 3 seconds for ready count
rect_max_height = height
rect_width = 20
has_player_scored = False
text_color = None

# Key mappings for players
player1_keys = {'RED': pygame.K_q, 'YELLOW': pygame.K_w, 'GREEN': pygame.K_e, 'WHITE': pygame.K_r, 'BLUE': pygame.K_t}
player2_keys = {'RED': pygame.K_y, 'YELLOW': pygame.K_u, 'GREEN': pygame.K_i, 'WHITE': pygame.K_o, 'BLUE': pygame.K_p}

#buttons 
start_img = pygame.image.load('assets/start_but.png').convert_alpha()
img_width = start_img.get_width()
x = (width - img_width) // 2  # Center horizontally
start_button = Button(x,400, start_img, 1)
exit_img = pygame.image.load('assets/exit_but.png').convert_alpha()
exit_button = Button(970, 10, exit_img, 1)
back_img = pygame.image.load('assets/back_but.png').convert_alpha()
back_button = Button(970, 10, back_img, 1)
easy_img = pygame.image.load('assets/easy.png').convert_alpha()
img_x = easy_img.get_width()
cen = (width - img_x) // 2
easy_button = Button(cen - 300, 400, easy_img, 1)
medium_img = pygame.image.load('assets/medium.png').convert_alpha()
medium_button = Button(cen, 400, medium_img, 1)
hard_img = pygame.image.load('assets/hard.png').convert_alpha()
hard_button = Button(cen + 300, 400, hard_img, 1)

#sound FX
pygame.mixer.music.load('assets/driftveil.mp3')
music_playing = False
beep_sfx = pygame.mixer.Sound('assets/countdown.wav')
beep_sfx.set_volume(0.8)
go_sfx = pygame.mixer.Sound('assets/go.wav')
go_sfx.set_volume(0.4)
color_sfx = pygame.mixer.Sound('assets/color.wav')
word_sfx = pygame.mixer.Sound('assets/word.wav')
p1_sfx = pygame.mixer.Sound('assets/p1_wins.wav')
p2_sfx = pygame.mixer.Sound('assets/p2_wins.wav')
tie_sfx = pygame.mixer.Sound('assets/tie_break.wav')
play_tie_sfx = False
play_once_sfx = False

#images
menu_img = pygame.image.load('assets/menu_bg.jpg').convert()
menu_rect = menu_img.get_rect(topleft=(0, 0))
title_img = pygame.image.load('assets/title_menu.png').convert_alpha()
title_rect = title_img.get_rect(topleft=(0, 0))
diff_img = pygame.image.load('assets/difficulty.png').convert_alpha()
diff_rect = diff_img.get_rect(topleft=(0, 0))
border_img = pygame.image.load('assets/border.png').convert_alpha()
border_rect = border_img.get_rect(topleft=(0, 0))
p1right = pygame.image.load('assets/p1_right.jpg').convert()
p1right_rect = p1right.get_rect(topleft=(0, 0))
p2right = pygame.image.load('assets/p2_right.jpg').convert()
p2right_rect = p2right.get_rect(topleft=(0, 0))
both_wrong = pygame.image.load('assets/both_wrong.jpg').convert()
both_wrong_rect = both_wrong.get_rect(topleft=(0, 0))
p1win = pygame.image.load('assets/p1_win.jpg').convert()
p1win_rect = p1win.get_rect(topleft=(0, 0))
p2win = pygame.image.load('assets/p2_win.jpg').convert()
p2win_rect = p2win.get_rect(topleft=(0, 0))


time_elapsed = 0
random_radius = [80, 100, 120, 140]

# Updated menu_screen function
def menu_screen():
    global time_elapsed
    
    screen.blit(menu_img,menu_rect)

    screen.blit(title_img, title_rect)

def set_difficulty():
    screen.blit(menu_img,menu_rect)
    screen.blit(diff_img,diff_rect)

def get_word_by_color(color_value):
    for word, color in color_map.items():
        if color == color_value:
            return word
    return None  # If no matching color is found


def game_screen_and_timers():
    global current_word, state_start_time, current_round, app_state, text_color, has_player_scored, new_bg_color, round_duration, max_round, play_once_sfx
    global player_scored, player1_pressed, player2_pressed, prev_p1score, prev_p2score, invert_input  # Track if players have pressed a key

    current_time = pygame.time.get_ticks()
    
    # go_sfx.play()

    # Check if the round is over
    if current_time - state_start_time > round_duration:
        app_state = SCORING
        current_round += 1
        state_start_time = current_time
        has_player_scored = False
        text_color = None  # Reset the text color for the next round
        new_bg_color = None  # Reset the background color for the next round
        player_scored = False
        player1_pressed = False  # Reset player1's pressed flag
        player2_pressed = False  # Reset player2's pressed flag
        play_once_sfx = False
        return


    # Only update the word, text color, and background color at the start of a new round
    if text_color is None:  # This ensures the color is only set once per round
        prev_p1score = player1_score  # Store Player 1's previous score before the round
        prev_p2score = player2_score  # Store Player 2's previous score before the round
        current_color = color_map[current_word]
        
        # Choose a text color that is different from the word's color
        possible_text_colors = [color for color in color_map.values() if color != current_color]
        text_color = random.choice(possible_text_colors)
        
        # Choose a background color that is different from both the word's color and the text color
        possible_bg_colors = [color for color in color_map.values() if color != current_color and color != text_color]
        new_bg_color = random.choice(possible_bg_colors)

    # Color Change on difficulty
    
    if diffculty_set == EASY:
        if current_round <=3:
            round_duration = 3000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <=6:
            round_duration = 2000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round > 6:
            if current_round ==7:
                if not play_once_sfx:
                    word_sfx.play()
                    play_once_sfx = True
            round_duration = 3000
            current_color = text_color
            screen.fill(black)
            invert_input = True
        if current_round == 9:
            max_round = True


    elif diffculty_set == MEDIUM:
        pass

    elif diffculty_set == HARD:
        pass

    screen.blit(border_img,border_rect)

    color_text_size = 130
    game_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', color_text_size)
    
    round_text_size = 70
    round_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', round_text_size)

    disp_round_text_size = 40
    disp_round_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', disp_round_text_size)

    # Render the text once
    text_surface = game_font.render(current_word, True, current_color)
    
    # Rotate the text for both positions
    rotated_text1 = pygame.transform.rotate(text_surface, -90)
    rotated_text2 = pygame.transform.rotate(text_surface, 90)

    # Get the rects and set the positions
    text1_rect = rotated_text1.get_rect(center=((width / 2) - 200, height / 2))
    text2_rect = rotated_text2.get_rect(center=((width / 2) + 200, height / 2))

    # Blit the rotated text onto the screen
    screen.blit(rotated_text1, text1_rect)
    screen.blit(rotated_text2, text2_rect)

    # "ROUND     SCORE" text display
    disp_round_surface = disp_round_font.render("ROUND                   SCORE", True, current_color)

    disp_rotated_round1 = pygame.transform.rotate(disp_round_surface, -90)
    disp_rotated_round2 = pygame.transform.rotate(disp_round_surface, 90)

    disp_round_rect1 = disp_rotated_round1.get_rect(center=((width / 2) - 350, height / 2))
    disp_round_rect2 = disp_rotated_round2.get_rect(center=((width / 2) + 350, height / 2))

    screen.blit(disp_rotated_round1, disp_round_rect1)
    screen.blit(disp_rotated_round2, disp_round_rect2)

    # Round counter display
    round_display = str(current_round)  
    round_surface = round_font.render(round_display, True, current_color)

    rotated_round1 = pygame.transform.rotate(round_surface, -90)
    rotated_round2 = pygame.transform.rotate(round_surface, 90)

    round_rect1 = rotated_round1.get_rect(center=((width / 2) - 400, 100))
    round_rect2 = rotated_round2.get_rect(center=((width / 2) + 400, 500))

    screen.blit(rotated_round1, round_rect1)
    screen.blit(rotated_round2, round_rect2)

    # Player Scores display
    score1_display = str(player1_score)  
    score2_display = str(player2_score)  
    score1_surface = round_font.render(score1_display, True, current_color)
    score2_surface = round_font.render(score2_display, True, current_color)

    rotated_score1 = pygame.transform.rotate(score1_surface, -90)
    rotated_score2 = pygame.transform.rotate(score2_surface, 90)

    score1_rect = rotated_score1.get_rect(center=((width / 2) - 400, 500))
    score2_rect = rotated_score2.get_rect(center=((width / 2) + 400, 100))

    screen.blit(rotated_score1, score1_rect)
    screen.blit(rotated_score2, score2_rect)

    # Handle the timers
    elapsed_time = current_time - state_start_time
    
    if elapsed_time <= round_duration:
        rect_height = int(rect_max_height * (1 - (elapsed_time / round_duration)))
    else:
        rect_height = 0
    
    # Left timer (bottom to top)
    pygame.draw.rect(screen, current_color, (0, height - rect_height, rect_width, rect_height))
    
    # Right timer (top to bottom)
    pygame.draw.rect(screen, current_color, (width - rect_width, 0, rect_width, rect_height))

def right_wrong():
    global player1_score, player2_score, prev_p1score, prev_p2score, app_state, state_start_time, max_round, play_once_sfx
    
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time
    wait_time = 3000
    
    if elapsed_time >= wait_time:  # Wait for 3 seconds before going back to the ready screen 
        if max_round == False:    
            app_state = GAME
        elif max_round:
            if player1_score == player2_score:
                app_state = MENU
            else:
                play_once_sfx = False
                app_state = WINNER
        state_start_time = current_time
        reset_leds_and_buttons()
        return
    
    # Compare the previous and current scores to determine which player was correct
    if player1_score > prev_p1score and player2_score == prev_p2score:
        screen.blit(p1right, p1right_rect)  # Player 1 got the point
    elif player2_score > prev_p2score and player1_score == prev_p1score:
        screen.blit(p2right, p2right_rect)  # Player 2 got the point
    elif player1_score == prev_p1score and player2_score == prev_p2score:
        screen.blit(both_wrong, both_wrong_rect)  # Both players got it wrong

    screen.blit(border_img,border_rect)

def reset_leds_and_buttons():
    global player1_pressed, player2_pressed
    for led in player1_leds.values():
        GPIO.output(led, GPIO.LOW)
    for led in player2_leds.values():
        GPIO.output(led, GPIO.LOW)
    player1_pressed = False
    player2_pressed = False

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
        pygame.mixer.music.stop()      
        game_screen_and_timers()
        handle_button_press()

    elif app_state == SCORING:    
        right_wrong()

    pygame.display.flip()
    clock.tick(60)

# Cleanup GPIO on exit
GPIO.cleanup()
