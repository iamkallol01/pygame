import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)  # For lollipop stick
ORANGE = (255, 165, 0)  # For bomb fuse
GRAY = (128, 128, 128)  # For the bucket
YELLOW = (255, 255, 0)  # For recall card

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Clock to control the game loop speed
clock = pygame.time.Clock()

# Player properties (bucket dimensions)
bucket_width, bucket_height = 80, 40
player_x = WIDTH // 2 - bucket_width // 2
player_y = HEIGHT - bucket_height - 10
player_speed = 7

# Object properties
object_width, object_height = 30, 30
object_speed = 5
objects = []

# Bomb properties
bomb_width, bomb_height = 30, 30
bomb_speed = 6
bombs = []

# Green lollipop properties
green_lollipop_width, green_lollipop_height = 30, 30
green_lollipop_speed = 5
green_lollipop = None
green_lollipop_last_spawn = time.time()

# Recall card properties
recall_card_width, recall_card_height = 30, 30
recall_card_speed = 5
recall_card = None
recall_card_last_spawn = time.time()

# Score
score = 0
font = pygame.font.Font(None, 36)

# Pause state
paused = False

# Lives state (number of recall cards)
lives = 0

# Game over state
game_over = False

# Load background music
pygame.mixer.music.load('sound/game-music-loop-6-144641.mp3')  # Path to your background music file
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (optional)
pygame.mixer.music.play(-1, 0.0)  # Play music in a loop (-1), starting at time 0.0

# Load sound effects
collect_lollipop_sound = pygame.mixer.Sound('sound/90s-game-ui-6-185099.mp3')
collect_green_lollipop_sound = pygame.mixer.Sound('sound/game-bonus-144751.mp3')
bomb_explode_sound = pygame.mixer.Sound('sound/game-over-31-179699.mp3')
game_over_sound = pygame.mixer.Sound('sound/game-over-31-179699.mp3')
recall_card_sound = pygame.mixer.Sound('sound/game-bonus-144751.mp3')

# Optional: Control volume for sound effects
collect_lollipop_sound.set_volume(0.5)
collect_green_lollipop_sound.set_volume(0.5)
bomb_explode_sound.set_volume(0.2)
game_over_sound.set_volume(1.0)
recall_card_sound.set_volume(0.5)
def handler(request):
    return {
        "statusCode": 200,
        "body": "Hello from Vercel!"
    }
# Spawn objects randomly
def spawn_object():
    x = random.randint(0, WIDTH - object_width)
    y = -object_height
    objects.append([x, y])

# Spawn bombs randomly
def spawn_bomb():
    x = random.randint(0, WIDTH - bomb_width)
    y = -bomb_height
    bombs.append([x, y])

# Spawn green lollipop
def spawn_green_lollipop():
    global green_lollipop
    x = random.randint(0, WIDTH - green_lollipop_width)
    y = -green_lollipop_height
    green_lollipop = [x, y]

# Spawn recall card
def spawn_recall_card():
    global recall_card
    x = random.randint(0, WIDTH - recall_card_width)
    y = -recall_card_height
    recall_card = [x, y]

# Check collision between player and an object
def check_collision(player_rect, rect_list):
    for rect in rect_list:
        if player_rect.colliderect(rect):
            return rect
    return None

# Pause function
def toggle_pause():
    global paused
    paused = not paused
# Add this function for game over screen
def show_game_over_screen():
    global running, score, lives, player_x, player_y, objects, bombs, green_lollipop, recall_card, paused
    screen.fill(WHITE)

    # Display "Game Over" message
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    play_again_text = font.render("Click to Play Again", True, BLUE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 3 + 100))

    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
                waiting = False

    # Reset game state
    score = 0
    lives = 0
    player_x = WIDTH // 2 - bucket_width // 2
    player_y = HEIGHT - bucket_height - 10
    objects.clear()
    bombs.clear()
    green_lollipop = None
    recall_card = None
    paused = False

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Toggle pause with the Space key
                toggle_pause()

    if paused:
        # Display "Paused" message
        pause_text = font.render("Game Paused. Press 'Space' to Resume.", True, BLACK)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(30)
        continue

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - bucket_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - bucket_height:
        player_y += player_speed

    # Spawn objects and bombs
    if random.randint(1, 30) == 1:
        spawn_object()
    if random.randint(1, 50) == 1:
        spawn_bomb()

    # Spawn green lollipop every 10 or 15 seconds
    current_time = time.time()
    if current_time - green_lollipop_last_spawn >= random.choice([10, 15]):
        spawn_green_lollipop()
        green_lollipop_last_spawn = current_time

    # Spawn recall card every 20 seconds
    if current_time - recall_card_last_spawn >= 20:
        spawn_recall_card()
        recall_card_last_spawn = current_time

    # Update object positions
    for obj in objects:
        obj[1] += object_speed

    # Update bomb positions
    for bomb in bombs:
        bomb[1] += bomb_speed

    # Update green lollipop position
    if green_lollipop:
        green_lollipop[1] += green_lollipop_speed
        if green_lollipop[1] > HEIGHT:
            green_lollipop = None  # Remove off-screen green lollipop

    # Update recall card position
    if recall_card:
        recall_card[1] += recall_card_speed
        if recall_card[1] > HEIGHT:
            recall_card = None  # Remove off-screen recall card

    # Draw player (bucket)
    player_rect = pygame.Rect(player_x, player_y, bucket_width, bucket_height)
    pygame.draw.rect(screen, GRAY, player_rect)  # Bucket base
    pygame.draw.rect(screen, BLACK, (player_x + 10, player_y - 10, bucket_width - 20, 10))  # Bucket rim

    # Draw objects as lollipops
    for obj in objects:
        x, y = obj
        # Stick
        pygame.draw.rect(screen, BROWN, (x + object_width // 2 - 2, y + 10, 4, object_height - 10))
        # Candy
        pygame.draw.circle(screen, RED, (x + object_width // 2, y + 10), object_width // 2)

    # Draw bombs
    for bomb in bombs:
        x, y = bomb
        # Main body
        pygame.draw.circle(screen, BLACK, (x + bomb_width // 2, y + bomb_height // 2), bomb_width // 2)
        # Fuse
        pygame.draw.rect(screen, ORANGE, (x + bomb_width // 2 - 2, y - 5, 4, 10))

    # Draw green lollipop
    if green_lollipop:
        x, y = green_lollipop
        # Stick
        pygame.draw.rect(screen, BROWN, (x + green_lollipop_width // 2 - 2, y + 10, 4, green_lollipop_height - 10))
        # Candy
        pygame.draw.circle(screen, GREEN, (x + green_lollipop_width // 2, y + 10), green_lollipop_width // 2)

    # Draw recall card
    if recall_card:
        x, y = recall_card
        # Rectangle for the recall card
        pygame.draw.rect(screen, YELLOW, (x, y, recall_card_width, recall_card_height))

    # Check collisions with objects (lollipops)
    hit_object = check_collision(player_rect, [pygame.Rect(o[0], o[1], object_width, object_height) for o in objects])
    if hit_object:
        objects.remove([hit_object.x, hit_object.y])
        score += 1
        collect_lollipop_sound.play()  # Play sound when a lollipop is collected

    # Check collisions with green lollipop
    if green_lollipop:
        green_lollipop_rect = pygame.Rect(green_lollipop[0], green_lollipop[1], green_lollipop_width, green_lollipop_height)
        if player_rect.colliderect(green_lollipop_rect):
            green_lollipop = None
            score += 5
            collect_green_lollipop_sound.play()  # Play sound for green lollipop

    # Check collisions with bombs (black lollipop)
    hit_bomb = check_collision(player_rect, [pygame.Rect(b[0], b[1], bomb_width, bomb_height) for b in bombs])
    if hit_bomb:
        if lives > 0:  # If player has recall cards (lives), use one and continue
            lives -= 1  # Use one recall card as life
            print(f"Life saved! Remaining lives: {lives}")
        else:  # If no lives, game over
            bomb_explode_sound.play()  # Play sound when bomb explodes
            game_over_sound.play()  # Play game over sound
            show_game_over_screen()  # Display game over screen

    # Check collisions with recall card
    if recall_card:
        recall_card_rect = pygame.Rect(recall_card[0], recall_card[1], recall_card_width, recall_card_height)
        if player_rect.colliderect(recall_card_rect):
            recall_card = None  # Remove recall card
            lives += 1  # Add a life (recall card)
            recall_card_sound.play()  # Play sound when recall card is collected

    # Remove objects and bombs off-screen
    objects = [o for o in objects if o[1] < HEIGHT]
    bombs = [b for b in bombs if b[1] < HEIGHT]

    # Render score and lives
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Toggle pause with the Space key
                toggle_pause()

    if paused:
        # Display "Paused" message
        pause_text = font.render("Game Paused. Press 'Space' to Resume.", True, BLACK)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(30)
        continue

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - bucket_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - bucket_height:
        player_y += player_speed

    # Spawn objects and bombs
    if random.randint(1, 30) == 1:
        spawn_object()
    if random.randint(1, 50) == 1:
        spawn_bomb()

    # Spawn green lollipop every 10 or 15 seconds
    current_time = time.time()
    if current_time - green_lollipop_last_spawn >= random.choice([10, 15]):
        spawn_green_lollipop()
        green_lollipop_last_spawn = current_time

    # Spawn recall card every 20 seconds
    if current_time - recall_card_last_spawn >= 20:
        spawn_recall_card()
        recall_card_last_spawn = current_time

    # Update object positions
    for obj in objects:
        obj[1] += object_speed

    # Update bomb positions
    for bomb in bombs:
        bomb[1] += bomb_speed

    # Update green lollipop position
    if green_lollipop:
        green_lollipop[1] += green_lollipop_speed
        if green_lollipop[1] > HEIGHT:
            green_lollipop = None  # Remove off-screen green lollipop

    # Update recall card position
    if recall_card:
        recall_card[1] += recall_card_speed
        if recall_card[1] > HEIGHT:
            recall_card = None  # Remove off-screen recall card

    # Draw player (bucket)
    player_rect = pygame.Rect(player_x, player_y, bucket_width, bucket_height)
    pygame.draw.rect(screen, GRAY, player_rect)  # Bucket base
    pygame.draw.rect(screen, BLACK, (player_x + 10, player_y - 10, bucket_width - 20, 10))  # Bucket rim

    # Draw objects as lollipops
    for obj in objects:
        x, y = obj
        # Stick
        pygame.draw.rect(screen, BROWN, (x + object_width // 2 - 2, y + 10, 4, object_height - 10))
        # Candy
        pygame.draw.circle(screen, RED, (x + object_width // 2, y + 10), object_width // 2)

    # Draw bombs
    for bomb in bombs:
        x, y = bomb
        # Main body
        pygame.draw.circle(screen, BLACK, (x + bomb_width // 2, y + bomb_height // 2), bomb_width // 2)
        # Fuse
        pygame.draw.rect(screen, ORANGE, (x + bomb_width // 2 - 2, y - 5, 4, 10))

    # Draw green lollipop
    if green_lollipop:
        x, y = green_lollipop
        # Stick
        pygame.draw.rect(screen, BROWN, (x + green_lollipop_width // 2 - 2, y + 10, 4, green_lollipop_height - 10))
        # Candy
        pygame.draw.circle(screen, GREEN, (x + green_lollipop_width // 2, y + 10), green_lollipop_width // 2)

    # Draw recall card
    if recall_card:
        x, y = recall_card
        # Rectangle for the recall card
        pygame.draw.rect(screen, YELLOW, (x, y, recall_card_width, recall_card_height))

    # Check collisions with objects (lollipops)
    hit_object = check_collision(player_rect, [pygame.Rect(o[0], o[1], object_width, object_height) for o in objects])
    if hit_object:
        objects.remove([hit_object.x, hit_object.y])
        score += 1
        collect_lollipop_sound.play()  # Play sound when a lollipop is collected

    # Check collisions with green lollipop
    if green_lollipop:
        green_lollipop_rect = pygame.Rect(green_lollipop[0], green_lollipop[1], green_lollipop_width, green_lollipop_height)
        if player_rect.colliderect(green_lollipop_rect):
            green_lollipop = None
            score += 5
            collect_green_lollipop_sound.play()  # Play sound for green lollipop

    # Check collisions with bombs (black lollipop)
    hit_bomb = check_collision(player_rect, [pygame.Rect(b[0], b[1], bomb_width, bomb_height) for b in bombs])
    if hit_bomb:
        if lives > 0:  # If player has recall cards (lives), use one and continue
            lives -= 1  # Use one recall card as life
            print(f"Life saved! Remaining lives: {lives}")
            # Reset player position after saving life
            player_x = WIDTH // 2 - bucket_width // 2
            player_y = HEIGHT - bucket_height - 10
        else:  # If no lives, game over
            print("Game Over! Final Score:", score)
            bomb_explode_sound.play()  # Play sound when bomb explodes
            game_over_sound.play()  # Play game over sound
            pygame.quit()
            sys.exit()

    # Check collisions with recall card
    if recall_card:
        recall_card_rect = pygame.Rect(recall_card[0], recall_card[1], recall_card_width, recall_card_height)
        if player_rect.colliderect(recall_card_rect):
            recall_card = None  # Remove recall card
            lives += 1  # Add a life (recall card)
            print(f"Recall card collected! Lives: {lives}")
            recall_card_sound.play()  # Play sound when recall card is collected

    # Remove objects and bombs off-screen
    objects = [o for o in objects if o[1] < HEIGHT]
    bombs = [b for b in bombs if b[1] < HEIGHT]

    # Render score and lives
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)
