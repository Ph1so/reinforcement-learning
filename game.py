import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Balls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
BUCKET_COLOR = (0, 0, 255)

# Game clock
clock = pygame.time.Clock()

# Bucket settings
bucket_width = 100
bucket_height = 20
bucket_x = WIDTH // 2 - bucket_width // 2
bucket_y = HEIGHT - bucket_height - 10
bucket_speed = 8

# Ball settings
ball_radius = 10
ball_x = random.randint(ball_radius, WIDTH - ball_radius)
ball_y = 0
ball_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move bucket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bucket_x > 0:
        bucket_x -= bucket_speed
    if keys[pygame.K_RIGHT] and bucket_x < WIDTH - bucket_width:
        bucket_x += bucket_speed

    # Update ball position
    ball_y += ball_speed

    # Ball reset & scoring
    if bucket_y < ball_y + ball_radius < bucket_y + bucket_height:
        if bucket_x < ball_x < bucket_x + bucket_width:
            score += 1
            ball_y = 0
            ball_x = random.randint(ball_radius, WIDTH - ball_radius)

    # Missed ball
    if ball_y > HEIGHT:
        score -= 1
        ball_y = 0
        ball_x = random.randint(ball_radius, WIDTH - ball_radius)

    pygame.draw.rect(screen, BUCKET_COLOR, (bucket_x, bucket_y, bucket_width, bucket_height))
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), ball_radius)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    game_state = [ball_y, ball_x, bucket_x]

pygame.quit()
