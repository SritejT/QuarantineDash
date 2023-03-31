import pygame
import sys
import random
from math import fabs

pygame.init()

# defines some pretty standard variables, including images and difficulty settings

black = (0, 0, 0)
grey = (158, 158, 158)

clock = pygame.time.Clock()

difficulty_settings = {

    'easy': {'start_vel': 20,
             'virus_vel': 2,
             'expansion_rate': 0.5,
             'powerup_spawn_time': 10,
             'virus_build_vel_multiplier': 0.5},

    'medium': {'start_vel': 20,
               'virus_vel': 3,
               'expansion_rate': 1,
               'powerup_spawn_time': 20,
               'virus_build_vel_multiplier': 1 / 3},

    'hard': {'start_vel': 15,
             'virus_vel': 4,
             'expansion_rate': 2,
             'powerup_spawn_time': 30,
             'virus_build_vel_multiplier': 0.25}

}

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption('Quarantine Dash')

splash_screen = pygame.image.load('game_images/splash_screen.png')
splash_screen = pygame.transform.scale(splash_screen, (1080, 720))
background = pygame.image.load('game_images/game_background.png')
background = pygame.transform.scale(background, (1080, 720))
character = pygame.image.load('game_images/game_character.png')
character = pygame.transform.scale(character, (72, 72))
toilet_roll = pygame.image.load('game_images/game_toilet_roll.png')
toilet_roll = pygame.transform.scale(toilet_roll, (72, 72))
game_over_screen = pygame.image.load('game_images/game_over.png')
game_over_screen = pygame.transform.scale(game_over_screen, (1080, 720))
powerup = pygame.image.load('game_images/game_powerup.png')
powerup = pygame.transform.scale(powerup, (72, 72))
virus = pygame.image.load('game_images/game_virus.png')
h_scaffolding = pygame.image.load('game_images/horizontal_scaffolding.png')
h_scaffolding = pygame.transform.scale(h_scaffolding, (120, 20))
v_scaffolding = pygame.image.load('game_images/vertical_scaffolding.png')
v_scaffolding = pygame.transform.scale(v_scaffolding, (20, 120))
building_background = pygame.image.load('game_images/building_background.png')
building_background = pygame.transform.scale(building_background, (1080, 720))
pygame.mixer.music.load('game_sounds/beep.mp3')

splash = True
game_running = False
game_over = False

# Loop for splash screen

while splash:

    # Detects if the user has pressed quit, and if so terminates program

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

        # Detects if user has pressed the buttons, and if they have displays the game with the appropriate difficulty

        if event.type == pygame.MOUSEBUTTONDOWN:

            if 410 <= pygame.mouse.get_pos()[1] <= 510:

                if 140 <= pygame.mouse.get_pos()[0] <= 400:

                    game_difficulty = 'easy'

                    splash = False

                    game_running = True

                if 420 <= pygame.mouse.get_pos()[0] <= 670:

                    game_difficulty = 'medium'

                    splash = False

                    game_running = True

                if 690 <= pygame.mouse.get_pos()[0] <= 950:

                    game_difficulty = 'hard'

                    splash = False

                    game_running = True

    screen.blit(splash_screen, (0, 0))

    pygame.display.update()

# Again defines some pretty standard variables

score = 0
character_x = 516
character_y = 336

font = pygame.font.Font('freesansbold.ttf', 32)

last_key = None


# Function that randomises the positions of the toilet roll and the powerup

def randomise_xy():

    x = random.randint(20, 988)
    y = random.randint(20, 628)

    return x, y


toilet_roll_x = randomise_xy()[0]
toilet_roll_y = randomise_xy()[1]

# Variable used to keep track of time. Utilises the fps of the game
counter = 0

# Yet again, pretty standard variables

display_powerup = False
char_direction = 'none'
powerup_x = None
powerup_y = None
velocity = difficulty_settings[game_difficulty]['start_vel']
virus_x = randomise_xy()[0]
virus_y = randomise_xy()[1]
virus_size = 24
display_v_scaffolding = False
display_h_scaffolding = False
character_stopped = False
virus_stopped = False

# Checks if the virus spawns directly on the player. If so, it randomises the position of the virus until it is not on the player

virus_killing = False

if virus_x + virus_size > character_x and virus_x < character_x + 72 and virus_y + virus_size > character_y and virus_y < character_y + 72:

    virus_killing = True

while virus_killing:

    virus_x = randomise_xy()[0]
    virus_y = randomise_xy()[1]

    if not (virus_x + virus_size > character_x and virus_x < character_x + 72 and virus_y + virus_size > character_y and virus_y < character_y + 72):

        break

building = False

# Main game loop

while game_running:

    # displays building template if the enter key is held

    if building:

        screen.blit(building_background, (0, 0))

    else:

        screen.blit(background, (0, 0))

    # Detects if user has pressed the quit button, and if they have terminates the program

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

        # Detects if the user has clicked while holding enter

        if event.type == pygame.MOUSEBUTTONDOWN and building:

            building_coordinates = pygame.mouse.get_pos()

            # Calculates if the user wants a vertical or horizontal wall based on the coordinates of their mouse

            if 110 < building_coordinates[0] < 970:

                if 110 < building_coordinates[0] - ((building_coordinates[0] // 140) * 140) < 130:

                    v_building_coordinates = building_coordinates

                    display_v_scaffolding = True

            if 70 < building_coordinates[1] < 650:

                if 70 < building_coordinates[1] - ((building_coordinates[1] // 140) * 140) < 90:

                    h_building_coordinates = building_coordinates

                    display_h_scaffolding = True

        # Allows character to move continuously if the arrow keys are held, but stops the character when they are not being pressed

        if event.type == pygame.KEYDOWN:

            last_key = event.key

            character_stopped = False

        elif event.type == pygame.KEYUP:

            last_key = None

    if not character_stopped:

        if last_key == pygame.K_UP:

            character_y -= velocity

        if last_key == pygame.K_DOWN:

            character_y += velocity

        if last_key == pygame.K_LEFT:

            character_x -= velocity

        if last_key == pygame.K_RIGHT:

            character_x += velocity

    # If the user is holding enter, the building mode is activated

    if last_key == pygame.K_RETURN:

        building = True

    else:

        building = False

    # Calculates which way the virus needs to go to get the character, and moves accordingly

    if not virus_stopped:

        if virus_y > character_y:

            virus_y -= difficulty_settings[game_difficulty]['virus_vel']

        if virus_y < character_y:

            virus_y += difficulty_settings[game_difficulty]['virus_vel']

        if virus_x > character_x:

            virus_x -= difficulty_settings[game_difficulty]['virus_vel']

        if virus_x < character_x:

            virus_x += difficulty_settings[game_difficulty]['virus_vel']

    # Enlarges virus, then displays the virus in the appropriate position

    enlarged_virus = pygame.transform.scale(virus, (virus_size, virus_size))

    screen.blit(enlarged_virus, (virus_x, virus_y))

    # displays character in appropriate position

    screen.blit(character, (character_x, character_y))

    # Detects whether or not the character is out of the game field, and if so, ends the game

    if not 20 <= character_x <= 988 or not 20 <= character_y <= 628:

        game_running = False

        game_over = True

    # Detects collision between toilet roll and character, and if they are colliding, it adds 1 to the score

    if fabs(character_x - toilet_roll_x) < 72 and fabs(character_y - toilet_roll_y) < 72:

        score += 1

        pygame.mixer.music.play(0)

        toilet_roll_x = randomise_xy()[0]
        toilet_roll_y = randomise_xy()[1]

    # Displays the powerup every so often, according to the difficulty settings, and sets the powerup's x and y coordinates

    if counter % (difficulty_settings[game_difficulty]['powerup_spawn_time'] * 20) == 0:

        display_powerup = True

        powerup_x = randomise_xy()[0]
        powerup_y = randomise_xy()[1]

    # Depending on the difficulty settings, increases the size of the virus every so often

    if counter % (20 / difficulty_settings[game_difficulty]['expansion_rate']) == 0:

        virus_size += 1

    # Detects collision between character and powerup, and if colliding, makes character faster and adds a point to score

    if fabs(character_x - powerup_x) < 72 and fabs(character_y - powerup_y) < 72:

        display_powerup = False

        pygame.mixer.music.play(0)

        powerup_x = -500
        powerup_y = -500

        velocity += 2
        score += 1

    # Detects if character and virus are colliding, and if they are, ends the game

    if virus_x + virus_size > character_x and virus_x < character_x + 72 and virus_y + virus_size > character_y and virus_y < character_y + 72:

        game_running = False

        game_over = True

    # Sets fps to 20

    clock.tick(20)

    screen.blit(toilet_roll, (toilet_roll_x, toilet_roll_y))

    # Displays powerup in the pre-calculated place

    if display_powerup:

        screen.blit(powerup, (powerup_x, powerup_y))

    # Calculates where the wall should be placed while building, according to where the user clicked, and then displays the wall appropriately

    if display_v_scaffolding:

        v_scaffolding_x = (v_building_coordinates[0] // 140 * 140) + 110

        v_scaffolding_y = (v_building_coordinates[1] - 90) // 140 * 140 + 90

        screen.blit(v_scaffolding, (v_scaffolding_x, v_scaffolding_y))

        # Detects whether the character is colliding with the wall, and if so, stops the player from moving until they press a different key

        if character_x + 72 > v_scaffolding_x and character_x < v_scaffolding_x + 20 and character_y + 72 > v_scaffolding_y and character_y < v_scaffolding_y + 120:

            character_stopped = True

        if virus_x + virus_size > v_scaffolding_x and virus_x < v_scaffolding_x + 20 and virus_y + virus_size > v_scaffolding_y and virus_y < v_scaffolding_y + 120:

            virus_stopped = True

    # Same thing as with the vertical walls, but now it displays a horizontal wall instead

    if display_h_scaffolding:

        h_scaffolding_x = (h_building_coordinates[0] - 120) // 140 * 140 + 130

        h_scaffolding_y = h_building_coordinates[1] // 140 * 140 + 70

        screen.blit(h_scaffolding, (h_scaffolding_x, h_scaffolding_y))

        # Same thing as with vertical walls

        if character_x + 72 > h_scaffolding_x and character_x < h_scaffolding_x + 120 and character_y + 72 > h_scaffolding_y and character_y < h_scaffolding_y + 20:

            character_stopped = True

        if virus_x + virus_size > h_scaffolding_x and virus_x < h_scaffolding_x + 120 and virus_y + virus_size > h_scaffolding_y and virus_y < h_scaffolding_y + 20:

            virus_stopped = True

    # Effectively slows down the virus whenever it needs to travel through walls

    if counter % (1 / difficulty_settings[game_difficulty]['virus_build_vel_multiplier']) == 0:

        virus_stopped = False

    # Displays score in the top right corner of the window

    text = font.render(str(score), True, black)
    text_rect = text.get_rect()
    text_rect.center = (1020, 50)
    screen.blit(text, text_rect)

    counter += 1

    pygame.display.update()

pygame.mixer.music.load('game_sounds/game_over_sound.wav')
pygame.mixer.music.play(0)

# Displays game over screen and score until user quits the game

while game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()

    screen.blit(game_over_screen, (0, 0))
    text = font.render('Your score was:', True, grey)
    text_rect = text.get_rect()
    text_rect.center = (540, 360)
    screen.blit(text, text_rect)

    score_text = font.render(str(score), True, grey)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (540, 424)
    screen.blit(score_text, score_text_rect)

    pygame.display.update()
