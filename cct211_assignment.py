import pygame
import sys  
import random
from basket import Basket
from fruit import Fruit
from bomb import Bomb
from magnet import Magnet

WIDTH = 800 
HEIGHT = 600
FPS = 60

def safe_fruit_y(other_fruits, new_y):
    for other in other_fruits:
        if abs(other.rect.y - new_y) < 400:
            new_y = other.rect.y - 400
    return min(new_y, -50)

def draw_text_with_shadow(screen, text, font, x, y):
    shadow = font.render(text, True, (0, 0, 0))
    white_text = font.render(text, True, (255, 255, 255))

    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(white_text, (x, y))

# Main function to run the game
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Image assets used in this game were found through Google Images and Vecteezy.
    garden = pygame.image.load("garden.png").convert()
    garden = pygame.transform.scale(garden, (WIDTH, HEIGHT))
    pygame.display.set_caption("Catch the fruit")

    clock = pygame.time.Clock()
    dt = 0

    # Image assets used in this game were found through Google Images and Vecteezy.
    basket = Basket(WIDTH // 2, HEIGHT - 35)
    fruit = Fruit(random.randint(50, WIDTH - 50), -50, "apple.png")
    banana = Fruit(random.randint(50, WIDTH - 50), -350, "banana.png")
    orange = Fruit(random.randint(50, WIDTH - 50), -650, "orange.png")
    bomb = Bomb(random.randint(50, WIDTH - 50), random.randint(-500, -350))
    golden_apple = Fruit(random.randint(50, WIDTH - 50), -2200, "golden_apple.png")

    # create the falling magnet power up
    magnet = Magnet(WIDTH)
    score = 0 
    highest_score = 0
    font = pygame.font.Font(None, 36)

    # store floating score effects
    floating_scores = []

    # combo system
    combo = 0
    # magnet power up
    magnet_active = False
    magnet_timer = 0

    lives = 3
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(basket)
    all_sprites.add(fruit)
    all_sprites.add(banana)
    all_sprites.add(orange)
    all_sprites.add(bomb)
    all_sprites.add(golden_apple)
    all_sprites.add(magnet)

    running = True
    game_over = False
    game_started = False
    paused = False
    show_instructions = False

    while running:

        # 1. events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_started:
                    mouse_x, mouse_y = event.pos

                    if (mouse_x - 760) ** 2 + (mouse_y - 40) ** 2 <= 20 ** 2:
                        show_instructions = not show_instructions

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if not game_started and event.key == pygame.K_SPACE:
                    game_started = True

                if game_started and not game_over and event.key == pygame.K_p:
                    paused = not paused

                if game_over and event.key == pygame.K_r:
                    score = 0
                    lives = 3
                    combo = 0
                    floating_scores.clear()
                    game_over = False
                    paused = False

                    magnet_active = False
                    magnet_timer = 0
                    magnet.reset(WIDTH)

                    fruit.rect.y = -50
                    fruit.rect.x = random.randint(0, WIDTH - fruit.rect.width)

                    banana.rect.y = -350
                    banana.rect.x = random.randint(0, WIDTH - banana.rect.width)

                    orange.rect.y = -650
                    orange.rect.x = random.randint(0, WIDTH - orange.rect.width)

                    bomb.rect.y = random.randint(-500, -350)
                    bomb.rect.x = random.randint(0, WIDTH - bomb.rect.width)

                    basket.rect.center = (WIDTH // 2, HEIGHT - 35)

                    golden_apple.rect.y = random.randint(-2200, -1800)
                    golden_apple.rect.x = random.randint(0, WIDTH - golden_apple.rect.width)

        # 2. update
        if game_started and not game_over and not paused:
            basket.update(dt)
            fruit.update(dt)
            banana.update(dt)
            orange.update(dt)
            bomb.update(dt)
            golden_apple.update(dt)

            # make the magnet fall by its own class
            magnet.update(dt, fruit.speed)

            # respawn the magnet after it leaves the screen
            if magnet.rect.top > HEIGHT:
                magnet.respawn(WIDTH)     

            # check if the basket catches the magnet
            if basket.rect.colliderect(magnet.rect):
                magnet_active = True
                magnet_timer = 3.0

                # respawn the magnet
                magnet.respawn(WIDTH)

            # count down the time for magnet
            if magnet_active:
                magnet_timer -= dt

                if magnet_timer <= 0:
                    magnet_active = False
                    magnet_timer = 0
                
            # attract nearby fruits
            if magnet_active:
                magnet_pull_speed = 480 * dt

                for item in [fruit, banana, orange, golden_apple]:
                    pull = round(magnet_pull_speed)

                    if item.rect.centerx < basket.rect.centerx:
                        item.rect.x += min(pull, basket.rect.centerx - item.rect.centerx)

                    elif item.rect.centerx > basket.rect.centerx:
                        item.rect.x -= min(pull, item.rect.centerx - basket.rect.centerx)

                    # Move fruit downward toward basket
                    if item.rect.bottom < basket.rect.top + 35:
                        item.rect.y += min(pull, basket.rect.top + 35 - item.rect.bottom)

            if score >= 100:
                fruit.speed = 10
                banana.speed = 10
                orange.speed = 10
                golden_apple.speed = 10
                bomb.speed = 11

            elif score >= 80:
                fruit.speed = 9
                banana.speed = 9
                orange.speed = 9
                golden_apple.speed = 9
                bomb.speed = 10

            elif score >= 60:
                fruit.speed = 8.5
                banana.speed = 8.5
                orange.speed = 8.5
                golden_apple.speed = 8.5
                bomb.speed = 9.5

            elif score >= 40:
                fruit.speed = 8
                banana.speed = 8
                orange.speed = 8
                golden_apple.speed = 8
                bomb.speed = 9
            
            elif score >= 30:
                fruit.speed = 7
                banana.speed = 7
                orange.speed = 7
                golden_apple.speed = 7
                bomb.speed = 8

            elif score >= 20:
                fruit.speed = 6
                banana.speed = 6
                orange.speed = 6
                golden_apple.speed = 6
                bomb.speed = 7
            
            elif score >= 10:
                fruit.speed = 5
                banana.speed = 5
                orange.speed = 5
                golden_apple.speed = 5
                bomb.speed = 6

            else:
                fruit.speed = 4
                banana.speed = 4
                orange.speed = 4
                golden_apple.speed = 4
                bomb.speed = 5

            if fruit.rect.bottom >= basket.rect.top + 30 and \
                fruit.rect.top < basket.rect.bottom and \
                fruit.rect.centerx > basket.rect.left and \
                fruit.rect.centerx < basket.rect.right:
                
                score += 1

                # increase combo when an apple is caught
                combo += 1

                floating_scores.append({
                    "text": f"{combo} COMBO!",
                    "x": basket.rect.centerx - 50,
                    "y": basket.rect.top - 65,
                    "timer": 1.0
                })

                # create a floating +1 above the basket
                floating_scores.append({
                    "text": "+1",
                    "x": basket.rect.centerx,
                    "y": basket.rect.top - 20,
                    "timer": 1.0
                })

                fruit.rect.y = safe_fruit_y([banana,orange], random.randint(-200,-50))
                fruit.rect.x = random.randint(0, WIDTH - fruit.rect.width)

            # to see the lives
            if fruit.rect.top > HEIGHT:
                lives -= 1
                combo = 0

                fruit.rect.y = safe_fruit_y([banana,orange], -40)
                fruit.rect.x = random.randint(0, WIDTH - fruit.rect.width)

            if banana.rect.bottom >= basket.rect.top + 30 and \
                banana.rect.top < basket.rect.bottom and \
                banana.rect.centerx > basket.rect.left and \
                banana.rect.centerx < basket.rect.right:
                
                score += 2
                combo += 1

                floating_scores.append({
                    "text": f"{combo} COMBO!",
                    "x": basket.rect.centerx - 50,
                    "y": basket.rect.top - 65,
                    "timer": 1.0
                })
                

                floating_scores.append({
                    "text": "+2",
                    "x": basket.rect.centerx,
                    "y": basket.rect.top - 20,
                    "timer": 1.0
                })


                banana.rect.y = safe_fruit_y([fruit,orange], random.randint(-700,-450))
                banana.rect.x = random.randint(0, WIDTH - banana.rect.width)

            if banana.rect.top > HEIGHT:
                lives -= 1
                combo = 0

                banana.rect.y = safe_fruit_y([fruit,orange], -150)
                banana.rect.x = random.randint(0, WIDTH - banana.rect.width)

            if orange.rect.bottom >= basket.rect.top + 30 and \
                orange.rect.top < basket.rect.bottom and \
                orange.rect.centerx > basket.rect.left and \
                orange.rect.centerx < basket.rect.right:
                
                score += 3
                combo += 1

                floating_scores.append({
                    "text": f"{combo} COMBO!",
                    "x": basket.rect.centerx - 50,
                    "y": basket.rect.top - 65,
                    "timer": 1.0
                })

                floating_scores.append({
                    "text": "+3",
                    "x": basket.rect.centerx,
                    "y": basket.rect.top - 20,
                    "timer": 1.0
                })
                orange.rect.y = safe_fruit_y([fruit,banana], random.randint(-700,-400))
                orange.rect.x = random.randint(0, WIDTH - orange.rect.width)

            if orange.rect.top > HEIGHT:
                lives -= 1
                combo = 0

                orange.rect.y = safe_fruit_y([fruit,banana], random.randint(-700,-400))
                orange.rect.x = random.randint(0, WIDTH - orange.rect.width)


            if bomb.rect.top > HEIGHT:
                bomb.rect.y = random.randint(-600, -300)
                bomb.rect.x = random.randint(0, WIDTH - bomb.rect.width)

            if bomb.rect.bottom >= basket.rect.top + 30 and \
                bomb.rect.top < basket.rect.bottom and \
                bomb.rect.centerx > basket.rect.left and \
                bomb.rect.centerx < basket.rect.right:
                
                lives -= 1
                combo = 0

                bomb.rect.y = -200
                bomb.rect.x = random.randint(0, WIDTH - bomb.rect.width)

            # Check whether the basket catch the golden apple which worth 5 points
            if golden_apple.rect.bottom >= basket.rect.top + 30 and \
                golden_apple.rect.top < basket.rect.bottom and \
                golden_apple.rect.centerx > basket.rect.left and \
                golden_apple.rect.centerx < basket.rect.right:
                
                score += 5
                combo += 1

                floating_scores.append({
                    "text": f"{combo} COMBO!",
                    "x": basket.rect.centerx - 50,
                    "y": basket.rect.top - 65,
                    "timer": 1.0
                })

                floating_scores.append({
                    "text": "+5",
                    "x": basket.rect.centerx,
                    "y": basket.rect.top - 20,
                    "timer": 1.0
                })
                
                if lives < 3:
                    lives += 1


                golden_apple.rect.y = random.randint(-1200, -900)
                golden_apple.rect.x = random.randint(0, WIDTH - golden_apple.rect.width)

            if golden_apple.rect.top > HEIGHT:
                golden_apple.rect.y = random.randint(-1200, -900)
                golden_apple.rect.x = random.randint(0, WIDTH - golden_apple.rect.width)
                    
            # Update the highest score after checking all fruit collision
            if score > highest_score:
                highest_score = score  
            
            # end game
            if lives <= 0:
                game_over = True

        # 3. draw
        screen.blit(garden,(0,0))

        # start screen
        if not game_started:
            pygame.draw.circle(screen, (255, 255, 255), (760, 40), 20)
            pygame.draw.circle(screen, (0, 0, 0), (760, 40), 20, 2)

            info_text = font.render("i", True, (0, 0, 0))
            screen.blit(info_text, info_text.get_rect(center=(760, 40)))

            title_text = font.render("Catch the Fruit!", True, (255, 255, 255))
            start_text = font.render("Press SPACE to start", True, (255, 255, 255))

            draw_text_with_shadow(screen, "Catch the Fruit!", font, WIDTH // 2 - title_text.get_width() // 2, 270 - title_text.get_height() // 2)
            draw_text_with_shadow(screen, "Press SPACE to start", font, WIDTH // 2 - start_text.get_width() // 2, 330 - start_text.get_height() // 2)

            if show_instructions:
                # draw the popup box
                pygame.draw.rect(screen, (255, 255, 255), (90, 120, 620, 360), border_radius=15)
                pygame.draw.rect(screen, (0, 0, 0), (90, 120, 620, 360), 3, border_radius=15)

                # instructions inside the box
                instructions = ["HOW TO PLAY",
                                "Move: Arrow Keys or A/D",
                                "Catch apple = 1 point",
                                "Catch banana = 2 points",
                                "Catch Orange = 3 points",
                                "Golden apple = +5 points and +1 life",
                                "Magnet = attracts all fruits for 3 seconds",
                                "Avoid bombs and don't miss fruit!",
                                "Press P to pause during the game"]
                for i, line in enumerate(instructions):
                    text_surface = font.render(line, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, 155 + i * 35))
                    screen.blit(text_surface, text_rect)


        if game_started and not game_over:
            all_sprites.draw(screen)

            # show the score
            draw_text_with_shadow(screen, "Score: " + str(score), font, 10, 10)
            # show the highest score
            draw_text_with_shadow(screen, "High Score: " + str(highest_score), font, 10, 90)
            

            # show the lives, filled if alive, outlined if lost
            for i in range(3):
                x = 25 + i * 40
                y = 65

                # create heart shape
                heart = pygame.Surface((40, 40), pygame.SRCALPHA)

                color = (255, 0, 0)

                pygame.draw.circle(heart, color, (12, 12), 9)
                pygame.draw.circle(heart, color, (28, 12), 9)
                pygame.draw.polygon(heart, color, [(3, 15), (37, 15), (20, 37)])

                if i >= lives:
                    # remove the middle to create a transparent outline
                    pygame.draw.circle(heart, (0, 0, 0, 0), (12, 12), 6)
                    pygame.draw.circle(heart, (0, 0, 0, 0), (28, 12), 6)
                    pygame.draw.polygon(heart, (0, 0, 0, 0), [(9, 17), (31, 17), (20, 30)])

                screen.blit(heart, (x - 20, y - 15))
                

        if paused:
            paused_text = font.render("PAUSED - Press P to resume", True, (255, 255, 255))
            draw_text_with_shadow(screen, "PAUSED - Press P to resume", font, WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - paused_text.get_height() // 2)

        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 255, 255))
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
            restart_text = font.render("Press R to restart", True, (255, 255, 255))

            draw_text_with_shadow(screen, "GAME OVER", font, WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 90 - game_over_text.get_height() // 2)
            draw_text_with_shadow(screen, f"Final Score: {score}", font, WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 30 - final_score_text.get_height() // 2)
            draw_text_with_shadow(screen, f"Highest Score: {highest_score}", font, WIDTH // 2 - highest_score_text.get_width() // 2, HEIGHT // 2 + 20 - highest_score_text.get_height() // 2)
            draw_text_with_shadow(screen, "Press R to restart", font, WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 90 - restart_text.get_height() // 2)

        # draw and animate floating score effects
        for effect in floating_scores[:]:
            # move upward
            if not paused:
                effect["y"] -= 40 * dt

                # count down the timer
                effect["timer"] -= dt

            # remove the effect after 1 second
            if effect["timer"] <= 0:
                floating_scores.remove(effect)
                continue

            # make the text fade away
            alpha = int(255 * effect["timer"])

            if "COMBO!" in effect["text"]:
                score_surface = font.render(effect["text"], True, (220, 20, 100))
                score_surface = pygame.transform.rotate(score_surface, 45)
            else:
                score_surface = font.render(effect["text"], True, (100, 0, 150))
            score_surface.set_alpha(alpha)

            score_rect = score_surface.get_rect(center=(effect["x"], int(effect["y"])))
            screen.blit(score_surface, score_rect)

        pygame.display.flip()

        

        # calculate elapsed time in sec for frame independent movement
        dt = clock.tick(FPS) / 1000  # convert to seconds



    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
