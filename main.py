from random import randint

import pygame

from src.sprite import Sprite
from src.player import Player
from src.config import WIN_HEIGHT, WIN_SIZE, WIN_WIGHT, SPAWN_STEP, WIN_HEIGHT, PLAYER_SPEED

def main():
    pygame.init()  
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()

    platform_image = pygame.image.load("asset/platform.png")
    platforms = [Sprite([200, 550],platform_image)]
    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Sprite([randint(0, WIN_WIGHT), y],platform_image))

    font = pygame.Font("asset/pixel.ttf", 32)

    btn_image = pygame.image.load("asset/platform.png")
    x = WIN_WIGHT / 2
    Y = WIN_HEIGHT / 3 * 2
    btn = Sprite([x, y], btn_image)

    player_image = pygame.image.load("asset/player.png")
    player = Player([200, 450], player_image, PLAYER_SPEED)
    window.set_icon(player_image)

    background_image = pygame.image.load("asset/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    clock = pygame.time.Clock()
    offset_y = 0
    running = True
    lose = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
        clock.tick(60)

        if not lose:
            player.update(platforms)
            if player.rect.top - offset_y >= WIN_HEIGHT:
                lose = True
            if player.rect.y - offset_y < WIN_HEIGHT/ 3:
                offset_y = player.rect.y - WIN_HEIGHT / 3

            if platforms[-1].rect.y - offset_y >= SPAWN_STEP:
                platforms.pop(0)
                y = platforms[-1].rect.y - SPAWN_STEP
                platforms.append(Sprite([randint(0, WIN_WIGHT), y],platform_image))


        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface, -offset_y)
        player.render(surface, -offset_y)

        text = str(round(-offset_y / 100))
        img = font.render(text, True, "black")
        rect = img.get_rect(midtop=[WIN_WIGHT / 2, 20])
        surface.blit(img, rect)

        if lose:
            img = font.render("Вы проиграли!\n\nВаш результат: " + text, True, "black")
            rect = img.get_rect(midtop=[WIN_WIGHT / 2, WIN_HEIGHT / 3])
            surface.blit(img, rect)

            btn.render(surface, 0)

        window.flip()

if __name__ == "__main__":
    main()