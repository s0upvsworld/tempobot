import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TEXT_BOX_HEIGHT = 150
FONT_SIZE = 24
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (0, 0, 0, 200)  # RGBA for semi-transparency
FPS = 60

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tempobot")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Function to draw a semi-transparent rectangle
def draw_text_box(surface, rect, color):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)  # Per-pixel alpha
    s.fill(color)
    surface.blit(s, rect.topleft)

# Text rendering function
def render_text_char_by_char(text, display_text_length):
    return text[:display_text_length]

# Main game loop variables
text = "Hello there! This is a test of the floating text box system. Pygame is great for making games!"
text_index = 0
text_speed = 3  # Number of frames between each character
counter = 0
running = True

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Skip to full text on SPACE
                text_index = len(text)

    # Update logic
    if text_index < len(text):
        counter += 1
        if counter % text_speed == 0:
            text_index += 1

    # Draw background
    screen.fill((50, 50, 50))  # Dark grey background

    # Draw text box
    box_rect = pygame.Rect(50, SCREEN_HEIGHT - TEXT_BOX_HEIGHT - 50, SCREEN_WIDTH - 100, TEXT_BOX_HEIGHT)
    draw_text_box(screen, box_rect, BOX_COLOR)

    # Draw text
    display_text = render_text_char_by_char(text, text_index)
    rendered_text = font.render(display_text, True, TEXT_COLOR)
    screen.blit(rendered_text, (box_rect.x + 20, box_rect.y + 20))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
