import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Revolver Man")

clock = pygame.time.Clock()

character_width = 25  
character_height = 25  
character_x = (SCREEN_WIDTH - character_width) // 2
character_y = (SCREEN_HEIGHT - character_height) // 2  
character_speed = 5

revolver_width = 20
revolver_height = 10
revolver_image = pygame.Surface((revolver_width, revolver_height), pygame.SRCALPHA)  
pygame.draw.rect(revolver_image, WHITE, (0, 0, revolver_width, revolver_height))  

arrow_length = 20  
arrow_width = 1  
arrow_speed = 10  
num_arrows = 7  # Increased the number of arrows to 7
arrows = []

STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
game_state = STATE_START

pygame.font.init()
dialogue_font = pygame.font.SysFont("Arial", 20)

def draw_arrow(surface, color, start, angle, length, width):
    end_x = start[0] + length * math.cos(angle)
    end_y = start[1] + length * math.sin(angle)
    pygame.draw.line(surface, color, start, (end_x, end_y), width)
    
    arrowhead_length = 6  
    arrowhead_angle = math.pi / 6
    left_head = (end_x + arrowhead_length * math.cos(angle + arrowhead_angle),
                 end_y + arrowhead_length * math.sin(angle + arrowhead_angle))
    right_head = (end_x + arrowhead_length * math.cos(angle - arrowhead_angle),
                  end_y + arrowhead_length * math.sin(angle - arrowhead_angle))
    pygame.draw.line(surface, color, (end_x, end_y), left_head, width)
    pygame.draw.line(surface, color, (end_x, end_y), right_head, width)

def generate_arrow():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        start_x = 0
        start_y = random.randint(0, SCREEN_HEIGHT)
        end_x = SCREEN_WIDTH
        end_y = random.randint(0, SCREEN_HEIGHT)
    elif side == 'right':
        start_x = SCREEN_WIDTH
        start_y = random.randint(0, SCREEN_HEIGHT)
        end_x = 0
        end_y = random.randint(0, SCREEN_HEIGHT)
    elif side == 'top':
        start_x = random.randint(0, SCREEN_WIDTH)
        start_y = 0
        end_x = random.randint(0, SCREEN_WIDTH)
        end_y = SCREEN_HEIGHT
    else:
        start_x = random.randint(0, SCREEN_WIDTH)
        start_y = SCREEN_HEIGHT
        end_x = random.randint(0, SCREEN_WIDTH)
        end_y = 0

    angle = math.atan2(end_y - start_y, end_x - start_x)
    return [start_x, start_y, math.cos(angle) * arrow_speed, math.sin(angle) * arrow_speed, angle]

def initialize_arrows():
    arrows.clear()
    for _ in range(num_arrows):
        arrows.append(generate_arrow())

def check_collision(player_x, player_y):
    for arrow in arrows:
        if (arrow[0] + arrow_length / 2 > player_x and arrow[0] - arrow_length / 2 < player_x + character_width and
                arrow[1] + arrow_width / 2 > player_y and arrow[1] - arrow_width / 2 < player_y + character_height):
            return True
    return False

def restart_game():
    global game_state, character_x, character_y
    initialize_arrows()
    character_x = (SCREEN_WIDTH - character_width) // 2
    character_y = (SCREEN_HEIGHT - character_height) // 2
    game_state = STATE_PLAYING

initialize_arrows()

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == STATE_START:
                    game_state = STATE_PLAYING
                elif game_state == STATE_GAME_OVER:
                    restart_game()

    if game_state == STATE_START:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to Start", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

    elif game_state == STATE_PLAYING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and character_x > 0:
            character_x -= character_speed
        if keys[pygame.K_d] and character_x < SCREEN_WIDTH - character_width:
            character_x += character_speed
        if keys[pygame.K_w] and character_y > 0:
            character_y -= character_speed
        if keys[pygame.K_s] and character_y < SCREEN_HEIGHT - character_height:
            character_y += character_speed

        if keys[pygame.K_a]:
            revolver_angle = 180
        elif keys[pygame.K_d]:
            revolver_angle = 0
        elif keys[pygame.K_w]:
            revolver_angle = 90
        elif keys[pygame.K_s]:
            revolver_angle = 270
        else:
            revolver_angle = 0  

        for arrow in arrows:
            arrow[0] += arrow[2]
            arrow[1] += arrow[3]

            if (arrow[0] < -arrow_length or arrow[0] > SCREEN_WIDTH + arrow_length or
                arrow[1] < -arrow_length or arrow[1] > SCREEN_HEIGHT + arrow_length):
                arrow[:] = generate_arrow()

            if check_collision(character_x, character_y):
                game_state = STATE_GAME_OVER

            screen.fill(BLACK)
            pygame.draw.rect(screen, BLUE, (character_x, character_y, character_width, character_height))
            
            rotated_revolver = pygame.transform.rotate(revolver_image, revolver_angle)
            revolver_rect = rotated_revolver.get_rect(center=(character_x + character_width // 2,
                                                              character_y + character_height // 2))
            screen.blit(rotated_revolver, revolver_rect)
            
            for arrow in arrows:
                draw_arrow(screen, WHITE, (arrow[0], arrow[1]), arrow[4], arrow_length, arrow_width)

            pygame.display.flip()
            clock.tick(160)

    elif game_state == STATE_GAME_OVER:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over - Press SPACE to Restart", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()

pygame.quit()
