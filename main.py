import pygame
import random
from pygame.locals import (
    KEYDOWN,
    QUIT,
)


# Background class, responsible for managing and drawing the background
class Background:
    def __init__(self):
        # Load and resize background image
        self.sky_surface = pygame.image.load('Clouds/Background/Background.png').convert()
        self.sky_surface = pygame.transform.scale(self.sky_surface, (800, 600))
        # Crop a section from the image
        rect = pygame.Rect(0, 100, self.sky_surface.get_width(), self.sky_surface.get_height() - 100)
        self.sky_surface = self.sky_surface.subsurface(rect)
        self.bg_x = 0

    # Move the background image to the left to give an illusion of movement
    def move(self):
        self.bg_x -= 1
        if self.bg_x <= -800:
            self.bg_x = 0

    # Draw the background on the screen
    def draw(self, screen):
        screen.blit(self.sky_surface, (self.bg_x, 0))
        screen.blit(self.sky_surface, (self.bg_x + 800, 0))


# Bird class, representing the player character
class Bird:
    def __init__(self):
        # Load and resize bird images for animation
        self.images = [pygame.image.load(f'Clouds/Bird_Objects/Bird{i}.png').convert_alpha() for i in range(1, 6)]
        self.images = [pygame.transform.scale(image, (75, 75)) for image in self.images]
        self.index = 0
        self.bird_surface = self.images[self.index]
        self.rect = self.bird_surface.get_rect()
        self.gravity = 0
        self.anim_speed = 10

        # Load and resize bird introduction image
        self.bird_intro = pygame.image.load("Clouds/Bird_Objects/Bird2.png").convert_alpha()
        self.bird_intro = pygame.transform.scale(self.bird_intro, (250, 250))
        self.bird_intro_rect = self.bird_intro.get_rect()

    # Animate the bird by switching between different images
    def animate(self):
        self.index += 1
        if self.index >= len(self.images) * self.anim_speed:
            self.index = 0
        self.bird_surface = self.images[self.index // self.anim_speed]

    # Update bird's position based on gravity
    def update(self):
        self.animate()
        self.gravity += 1 / 6
        self.rect.y += self.gravity
        self.rect.x = 40
        if self.rect.top <= 0: self.rect.top = 0

    # Draw the bird on the screen
    def draw(self, screen):
        screen.blit(self.bird_surface, self.rect)


# Food class, representing the food items the bird can collect
class Food:
    def __init__(self):
        # Load and resize food image
        self.food_surface = pygame.image.load('Clouds/Bird_Objects/Food_1.png').convert_alpha()
        self.food_surface = pygame.transform.scale(self.food_surface, (25, 25))
        self.rect = self.food_surface.get_rect()
        self.x = 800
        self.y = random.randint(0, 425)

    # Update food's position
    def update(self):
        self.x -= 1
        if self.x <= -25:
            self.x = 800
            self.y = random.randint(0, 425)
        self.rect.topleft = (self.x, self.y)

    # Draw the food on the screen
    def draw(self, screen):
        screen.blit(self.food_surface, (self.x, self.y))


pygame.init()
pygame.display.set_caption("Hungry Bird!")
screen = pygame.display.set_mode((800, 450))
font = pygame.font.Font('Clouds/Font/Pixeltype.ttf', 50)
text_intro = font.render('Hungry Boya ', False, (255, 0, 0))
text_instructions = font.render('(Press SPACE to fly, eat the food to survive!)', False, (0, 0, 0))

# Main game loop
running = True
game_active = False
current_health = 100
max_health = 100
playerScore = 0

background = Background()
bird = Bird()

# Create multiple food objects
foods = [Food() for _ in range(5)]

clock = pygame.time.Clock()

while running:
    # Handle keyboard and window events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                # On spacebar press, make the bird fly and start the game if not already active
                if not game_active:
                    game_active = True
                    current_health = max_health
                    playerScore = 0
                    bird.rect.y = 0
                    bird.gravity = 0
                bird.gravity -= 20 / 4
            elif event.key == pygame.K_q:
                # On 'q' press, quit the game
                running = False
                pygame.quit()
        elif event.type == QUIT:
            # On window close, quit the game
            running = False

    if game_active:
        # Update game objects and check for collisions
        background.move()
        bird.update()
        for food in foods:
            food.update()
            if bird.rect.colliderect(food.rect):
                # Increase score when bird collides with food
                playerScore += 1
                food.x = 800
                food.y = random.randint(0, 425)

        # End game if bird hits the ground
        if bird.rect.y >= 400:
            game_active = False

        # Decrease health over time and end game if health is depleted
        current_health -= 1 / 60
        if current_health <= 0:
            game_active = False

        # Draw game objects and health bar
        screen.fill((94, 129, 162))
        background.draw(screen)
        bird.draw(screen)
        for food in foods:
            food.draw(screen)

        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = screen.get_width() / 2 - health_bar_width / 2
        health_bar_y = 10
        health_label = font.render('Time:', True, ('Black'))

        screen.blit(health_label, (health_bar_x - health_label.get_width() - 10, health_bar_y))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0),
                         pygame.Rect(health_bar_x, health_bar_y, health_bar_width * (current_health / max_health),
                                     health_bar_height))

    else:
        # Draw introduction screen when game is not active
        screen.fill((94, 129, 162))
        bird.bird_intro_rect.center = (400, 225)
        screen.blit(bird.bird_intro, bird.bird_intro_rect)
        screen.blit(text_intro, (275, 50))
        screen.blit(text_instructions, (50, 100))

    # Draw player's score
    score_text = font.render('Score: ' + str(playerScore), False, ('Black'))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
