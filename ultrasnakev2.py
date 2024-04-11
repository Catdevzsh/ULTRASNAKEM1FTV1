import pygame
import random
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Colors (using RGB values)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Screen dimensions
display_width = 800
display_height = 600

# Set up the display
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

# Clock for controlling game speed
clock = pygame.time.Clock()

# Snake properties
snake_block_size = 10
snake_speed = 15

# Font for displaying score
font_style = pygame.font.SysFont(None, 35)

def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    game_display.blit(value, [0, 0])

def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_display, green, [x[0], x[1], snake_block_size, snake_block_size])

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Sound effects
eat_food_sound = generate_square_wave(660, 0.1, 0.1)
game_over_sound = generate_square_wave(220, 0.1, 0.5)

def game_start_screen():
    start = False
    while not start:
        game_display.fill(black)
        start_message = font_style.render("Press 'Z' or 'Enter' to Start", True, white)
        game_display.blit(start_message, [display_width / 4, display_height / 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    start = True

def game_loop():
    game_over = False
    game_close = False

    # Starting position of the snake
    x1 = display_width / 2
    y1 = display_height / 2

    # Initial change in position
    x1_change = 0
    y1_change = 0

    # Initial snake length and food position
    snake_list = []
    snake_length = 1
    foodx = round(random.randrange(0, display_width - snake_block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block_size) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            game_display.fill(black)
            message = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, white)
            game_display.blit(message, [display_width/6, display_height/3])
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block_size
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_over_sound.play()
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_display.fill(black)
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block_size, snake_block_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_over_sound.play()
                game_close = True

        draw_snake(snake_block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block_size) / 10.0) * 10.0
            snake_length += 1
            eat_food_sound.play()

        clock.tick(snake_speed)

game_start_screen()
game_loop()
