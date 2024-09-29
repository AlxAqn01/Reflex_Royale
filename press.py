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
player1_buttons = {'RED': 17, 'YELLOW': 27, 'GREEN': 3, 'WHITE': 4, 'BLUE': 2}
player1_leds = {'RED': 23, 'YELLOW': 24, 'GREEN': 15, 'WHITE': 18, 'BLUE': 14}
player2_buttons = {'RED': 26, 'YELLOW': 19, 'GREEN': 13, 'WHITE': 6, 'BLUE': 5}
player2_leds = {'RED': 21, 'YELLOW': 20, 'GREEN': 16, 'WHITE': 12, 'BLUE': 1}

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
NOT_SET, EASY, NORMAL, HARD = 0, 1, 2, 3
diffculty_set = NOT_SET
current_round = 1
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
normal_img = pygame.image.load('assets/normal.png').convert_alpha()
normal_button = Button(cen, 400, normal_img, 1)
hard_img = pygame.image.load('assets/hard.png').convert_alpha()
hard_button = Button(cen + 300, 400, hard_img, 1)

#sound FX
pygame.mixer.music.load('assets/driftveil.mp3')
music_playing = False
easy_sfx = pygame.mixer.Sound('assets/easy_mode.wav')
normal_sfx = pygame.mixer.Sound('assets/normal_mode.wav')
hard_sfx = pygame.mixer.Sound('assets/hard_mode.wav')
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

# Circle definitions for the menu screen
circles = [
    {'color': green, 'pos': [width // 4, height // 2], 'radius': random.choice(random_radius), 'speed_x': random.uniform(0.5, 1.5), 'speed_y': random.uniform(0.5, 1.5), 'dir_x': random.choice([-1, 1]), 'dir_y': random.choice([-1, 1])},
    {'color': blue, 'pos': [width // 2, height // 2], 'radius': random.choice(random_radius), 'speed_x': random.uniform(0.5, 1.5), 'speed_y': random.uniform(0.5, 1.5), 'dir_x': random.choice([-1, 1]), 'dir_y': random.choice([-1, 1])},
    {'color': red, 'pos': [3 * width // 4, height // 2], 'radius': random.choice(random_radius), 'speed_x': random.uniform(0.5, 1.5), 'speed_y': random.uniform(0.5, 1.5), 'dir_x': random.choice([-1, 1]), 'dir_y': random.choice([-1, 1])},
    {'color': yellow, 'pos': [width // 2, height // 1.5], 'radius': random.choice(random_radius), 'speed_x': random.uniform(0.5, 1.5), 'speed_y': random.uniform(0.5, 1.5), 'dir_x': random.choice([-1, 1]), 'dir_y': random.choice([-1, 1])},
    {'color': white, 'pos': [width // 2, height // 1.5], 'radius': random.choice(random_radius), 'speed_x': random.uniform(0.5, 1.5), 'speed_y': random.uniform(0.5, 1.5), 'dir_x': random.choice([-1, 1]), 'dir_y': random.choice([-1, 1])},
]

def menu_circles():
    # Update circles' positions with independent random movement
    for circle in circles:
        circle['pos'][0] += circle['speed_x'] * circle['dir_x']
        circle['pos'][1] += circle['speed_y'] * circle['dir_y']

        # Check for boundaries and reverse direction if needed
        if circle['pos'][0] < circle['radius'] or circle['pos'][0] > width - circle['radius']:
            circle['dir_x'] *= -1
        if circle['pos'][1] < circle['radius'] or circle['pos'][1] > height - circle['radius']:
            circle['dir_y'] *= -1

        # Create a surface for the blurred circle effect
        circle_surface = pygame.Surface((circle['radius'] * 2, circle['radius'] * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, circle['color'], (circle['radius'], circle['radius']), circle['radius'])
        circle_surface.set_alpha(150)  # Adjust the alpha for the blur effect
        screen.blit(circle_surface, (circle['pos'][0] - circle['radius'], circle['pos'][1] - circle['radius']))

def mirrored_text(font_type, text, select_color, x, y1, y2):
    mode_surface = font_type.render(text, True, select_color)
    rotated_text1 = pygame.transform.rotate(mode_surface, -90)
    rotated_text2 = pygame.transform.rotate(mode_surface, 90)
    text1_rect = rotated_text1.get_rect(center=((width / 2) - x, y1))
    text2_rect = rotated_text2.get_rect(center=((width / 2) + x, y2))
    screen.blit(rotated_text1, text1_rect)
    screen.blit(rotated_text2, text2_rect)

# Updated menu_screen function
def menu_screen():
    global time_elapsed
    
    screen.blit(menu_img,menu_rect)

    menu_circles()

    screen.blit(title_img, title_rect)

def set_difficulty():
    screen.blit(menu_img,menu_rect)
    menu_circles()
    screen.blit(diff_img,diff_rect)
    

def set_intro():
    global diffculty_set, app_state, state_start_time, play_once_sfx

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time

    if elapsed_time >= countdown_duration:
        app_state = READY
        play_once_sfx = False
        state_start_time = current_time
        return

    if diffculty_set == EASY:
        if not play_once_sfx:
            easy_sfx.play()
            play_once_sfx = True
        intro("EASY MODE", green, "Best of 9 Rounds")
        
    elif diffculty_set == NORMAL:
        if not play_once_sfx:
            normal_sfx.play()
            play_once_sfx = True
        intro("NORMAL MODE", yellow, "Best of 15 Rounds")
    
    elif diffculty_set == HARD:
        if not play_once_sfx:
            hard_sfx.play()
            play_once_sfx = True
        intro("HARD MODE", red, "Best of 21 Rounds")


def intro(mode_txt, mode_color, round_txt):
        screen.fill(black)
        screen.blit(border_img,border_rect)
        
        font1 = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 60)
        font2 = pygame.font.Font('assets/recharge bd.otf', 50)

        mirrored_text(font2, mode_txt, mode_color, 150, height / 2, height / 2)
        mirrored_text(font1, round_txt, white, 250, height / 2, height / 2)
        mirrored_text(font1, "HAVE FUN!", white, 350, height / 2, height / 2)


def get_word_by_color(color_value):
    for word, color in color_map.items():
        if color == color_value:
            return word
    return None  # If no matching color is found

def game_screen_and_timers():
    global current_word, state_start_time, current_round, app_state, text_color, has_player_scored, new_bg_color, round_duration, max_round, play_once_sfx
    global player_scored, player1_pressed, player2_pressed, prev_p1score, prev_p2score, invert_input  # Track if players have pressed a key

    current_time = pygame.time.get_ticks()
    
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
        if current_round == 9:
            max_round = True

    elif diffculty_set == NORMAL:
        if current_round <=2:
            round_duration = 3000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <=5:
            round_duration = 1800
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <=9:
            if current_round ==7:
                if not play_once_sfx:
                    word_sfx.play()
                    play_once_sfx = True
            round_duration = 2500
            current_color = text_color
            screen.fill(black)
        elif current_round <=12:
            round_duration = 1700
            current_color = text_color
            screen.fill(black)
        elif current_round > 12:
            if current_round ==13:
                if not play_once_sfx:
                    color_sfx.play()
                    play_once_sfx = True
            round_duration = 2500
            current_color = text_color
            screen.fill(black)
            invert_input = True
        if current_round == 15:
            max_round = True

    elif diffculty_set == HARD:
        if current_round <=2:
            round_duration = 3000
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <=5:
            round_duration = 1800
            current_color = color_map[current_word]
            screen.fill(black)
        elif current_round <=9:
            if current_round ==7:
                if not play_once_sfx:
                    word_sfx.play()
                    play_once_sfx = True
            round_duration = 2500
            current_color = text_color
            screen.fill(black)
        elif current_round <=12:
            round_duration = 1700
            current_color = text_color
            screen.fill(black)
        elif current_round <= 15:
            if current_round ==13:
                if not play_once_sfx:
                    color_sfx.play()
                    play_once_sfx = True
            round_duration = 2500
            current_color = text_color
            screen.fill(black)
            invert_input = True
        elif current_round > 15:
            current_color = text_color
            screen.fill(new_bg_color)
        if current_round == 21:
            max_round = True

    screen.blit(border_img,border_rect)

    # Display what to press
    game_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 130)
    mirrored_text(game_font,current_word,current_color, 200, height / 2, height / 2)

    # "ROUND     SCORE" text display
    disp_round_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 40)
    mirrored_text(disp_round_font, "ROUND                   SCORE" ,current_color, 350, height / 2, height / 2)

    # Round counter display
    round_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 70)
    mirrored_text(round_font,str(current_round), current_color, 400, 100, 500)

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

def ready_count():
    global app_state, state_start_time, current_word, play_once_sfx
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time
    countdown_time = 3 - int(elapsed_time / 1000)
    
    screen.fill(black)

    if elapsed_time >= countdown_duration:
        app_state = GAME
        state_start_time = current_time
        current_word = random.choice(words_color)
        play_once_sfx = False
        return

    screen.blit(border_img,border_rect)

    game_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 140)
    mirrored_text(game_font,"READY", white, 200, height / 2, height / 2)

    # Countdown numbers
    font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 120)
    mirrored_text(font,str(max(countdown_time, 1)), white, 400, height / 2, height / 2)

    if not play_once_sfx:
        beep_sfx.play()
        play_once_sfx = True


def right_wrong():
    global player1_score, player2_score, prev_p1score, prev_p2score, app_state, state_start_time, max_round, play_once_sfx
    
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time
    wait_time = 3000
    
    if elapsed_time >= wait_time:  # Wait for 3 seconds before going back to the ready screen 
        if max_round == False:    
            app_state = READY
        elif max_round:
            if player1_score == player2_score:
                app_state = TIEBREAK
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
    
def tie_break():
    global app_state, state_start_time, play_tie_sfx

    screen.fill(black)
    screen.blit(border_img,border_rect)
    
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time

    if elapsed_time >= countdown_duration:
        app_state = READY
        state_start_time = current_time
        return

    font1 = pygame.font.Font('assets/recharge bd.otf', 50)
    font2 = pygame.font.Font('assets/recharge bd.otf', 50)
    mirrored_text(font2, "TIE BREAKER", white, 150, height / 2)
    mirrored_text(font1, "SUDDEN DEATH", red, 250, height / 2)

    if not play_tie_sfx:
        tie_sfx.play()
        play_tie_sfx = True  # Mark music as playing


def declare_winner():
    global app_state, state_start_time, current_round, music_playing, play_once_sfx, play_tie_sfx, diffculty_set
    global player1_score, player2_score, prev_p1score, prev_p2score, invert_input,max_round
    
    
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - state_start_time
    wait_time = 5000

    if elapsed_time >= wait_time:  
        app_state = MENU
        diffculty_set = NOT_SET
        current_round = 1
        player1_score, player2_score, prev_p1score, prev_p2score = 0, 0, 0, 0
        invert_input = False
        music_playing = False
        play_once_sfx = False
        play_tie_sfx = False
        max_round = False
        state_start_time = current_time
        return

    if player1_score > player2_score:
        screen.blit(p1win, p1win_rect)
        if not play_once_sfx:
            p1_sfx.play()
            play_once_sfx = True  # Mark music as playing
    else:
        screen.blit(p2win, p2win_rect)
        if not play_once_sfx:
            p2_sfx.play()
            play_once_sfx = True  # Mark music as playing
      
    screen.blit(border_img,border_rect)

    
    score_font = pygame.font.Font('assets/TT Fors Trial ExtraBold.ttf', 60)
    mirrored_text(score_font, "FINAL SCORE", white, 70, (height / 2) - 20, (height / 2) + 20)
    
    # Display each player score
    score1_display = str(player1_score)  
    score2_display = str(player2_score)  
    score1_surface = score_font.render(score1_display, True, white)
    score2_surface = score_font.render(score2_display, True, white)

    rotated_score1 = pygame.transform.rotate(score1_surface, -90)
    rotated_score2 = pygame.transform.rotate(score2_surface, 90)

    score1_rect = rotated_score1.get_rect(center=((width / 2) - 70, (height / 2) + 230))
    score2_rect = rotated_score2.get_rect(center=((width / 2) + 70, (height / 2) - 230))

    screen.blit(rotated_score1, score1_rect)
    screen.blit(rotated_score2, score2_rect)

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
            pygame.mixer.music.play(-1)  # -1 means loop forever
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
            if normal_button.draw(screen):
                diffculty_set = NORMAL
            if hard_button.draw(screen):
                diffculty_set = HARD
                
        if diffculty_set != NOT_SET:
            app_state = RULES
            state_start_time = pygame.time.get_ticks()
            
        if back_button.draw(screen):
            app_state = MENU

    elif app_state == RULES:
        pygame.mixer.music.stop()
        set_intro()

    elif app_state == READY:
        ready_count()

    elif app_state == GAME:        
        game_screen_and_timers()
        handle_button_press()

    elif app_state == SCORING:
        right_wrong()

    elif app_state == TIEBREAK:
        tie_break()

    elif app_state == WINNER:
        declare_winner()

    pygame.display.flip()
    clock.tick(60)

GPIO.cleanup()
