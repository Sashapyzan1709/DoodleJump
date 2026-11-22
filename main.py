from random import randint

import pygame

from src.bullet import Bullet
from src.config import (
    DESTROY_PLATFORM,
    PLAYER_SPEED,
    SPAWN_STEP,
    WIN_HEIGHT,
    WIN_SIZE,
    WIN_WIDTH,
)
from src.monsters import Monster
from src.platforms import BatutPlatform, MovingPlatform, Platform, TrapPlatform
from src.player import Player
from src.sprite import Sprite


def main():
    pygame.init()

    window = pygame.Window("Jumper", WIN_SIZE)
    surface = window.get_surface()
    clock = pygame.Clock()

    font = pygame.Font("asset/pixel.ttf", 32)

    jump_sound = None
    if pygame.mixer.get_init():
        pygame.mixer_music.load("asset/background.mp3")
        pygame.mixer_music.set_volume(0.1)
        pygame.mixer_music.play(-1)

        fall_sound = pygame.Sound("asset/fall.mp3")
        fall_sound.set_volume(0.1)
        jump_sound = pygame.Sound("asset/jump.wav")
        jump_sound.set_volume(0.1)

    button_image = pygame.image.load("asset/button.png")
    button_image = pygame.transform.scale(
        button_image,
        [WIN_WIDTH / 5 * 4, WIN_WIDTH / 5],
    )
    img = font.render("Заново", True, "white")
    rect = img.get_rect(center=[button_image.width / 2, button_image.height / 2])
    button_image.blit(img, rect)

    x = WIN_WIDTH / 2
    y = WIN_HEIGHT / 3 * 2
    button = Sprite([x, y], button_image)

    monster_image = pygame.image.load("asset/player.png")

    bullet_image = pygame.image.load("asset/platform.png")
    bullet_image = pygame.transform.scale(bullet_image, (10, 10))
    bullets = []

    background_image = pygame.image.load("asset/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    platform_image = pygame.image.load("asset/platform.png")
    batut_image = pygame.image.load("asset/batut_image.png")
    trap_image = pygame.image.load("asset/trap_image.png")
    move_image = pygame.image.load("asset/move_image.png")
    platforms = [Platform([200, 550], platform_image)]
    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Platform([randint(0, WIN_WIDTH), y], platform_image))

    player_image = pygame.image.load("asset/player.png")
    player = Player([200, 450], player_image, PLAYER_SPEED, jump_sound)
    window.set_icon(player_image)

    monster = None
    running = True
    lose = False
    offset_y = 0
    spawn_platform_y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b = Bullet(player.rect.midtop, bullet_image, 10)
                bullets.append(b)
            elif event.type == DESTROY_PLATFORM:
                platforms.remove(event.platform)
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and button.rect.collidepoint(pygame.mouse.get_pos())
                and lose
            ):
                spawn_platform_y = 0
                player.rect.center = [200, 450]
                platforms = [Platform([200, 550], platform_image)]
                for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
                    platforms.append(
                        Platform([randint(0, WIN_WIDTH), y], platform_image)
                    )
                offset_y = 0
                lose = False

        if not lose:
            player.update(platforms)
            if monster != None:
                monster.update()
                if monster.rect.top - offset_y >= WIN_HEIGHT:
                    monster = None
                elif monster.rect.colliderect(player.rect):
                    lose = True
            for platform in platforms:
                platform.update()
            for bullet in bullets:
                bullet.update()
                if bullet.rect.bottom - offset_y <= 0:
                    bullets.remove(bullet)
                elif monster != None and monster.rect.colliderect(bullet.rect):
                    monster = None
                    bullets.remove(bullet)

            if player.rect.top - offset_y >= WIN_HEIGHT:
                if pygame.mixer.get_init():
                    fall_sound.play()
                lose = True
            if player.rect.y - offset_y < WIN_HEIGHT / 3:
                offset_y = player.rect.y - WIN_HEIGHT / 3

            if abs(offset_y) - spawn_platform_y >= SPAWN_STEP:
                spawn_platform_y = abs(offset_y)
                y = offset_y
                r = randint(1, 100)
                if r <= 10:
                    platform = MovingPlatform([randint(0, WIN_WIDTH), y], move_image)
                elif r <= 20:
                    platform = TrapPlatform([randint(0, WIN_WIDTH), y], trap_image)
                elif r <= 30:
                    platform = BatutPlatform([randint(0, WIN_WIDTH), y], batut_image)
                else:
                    platform = Platform([randint(0, WIN_WIDTH), y], platform_image)
                platforms.append(platform)

                if randint(1, 100) <= 10 and monster == None:
                    y = y - monster_image.width
                    x = platform.rect.centerx
                    monster = Monster([x, y], monster_image, randint(1, 3), 1.5)

        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface, -offset_y)
        for bullet in bullets:
            bullet.render(surface, -offset_y)
        if monster != None:
            monster.render(surface, -offset_y)
        player.render(surface, -offset_y)

        text = str(round(-offset_y / 200))
        img = font.render(text, True, "black")
        rect = img.get_rect(midtop=[WIN_WIDTH / 2, 10])
        surface.blit(img, rect)

        if lose:
            img = font.render("Вы проиграли!\n\nВаш результат: " + text, True, "black")
            rect = img.get_rect(midtop=[WIN_WIDTH / 2, WIN_HEIGHT / 3])
            surface.blit(img, rect)

            button.render(surface, 0)

        window.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()