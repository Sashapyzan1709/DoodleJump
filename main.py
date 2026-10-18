import pygame

from src.sprite import Sprite
from src.player import Player

def main():  
    window = pygame.Window("Doodle Jump", [400, 600])
    surface = window.get_surface()

    platform_image = pygame.image.load("asset/platform.png")
    platform = Sprite([200, 550],platform_image)
    
    player_image = pygame.image.load("asset/player.png")
    player = Player([200, 450], player_image, 6)
    window.set_icon(player_image)

    background_image = pygame.image.load("asset/background.png")
    background_image = pygame.transform.scale(background_image, [400, 600])

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
        clock.tick(60)
        player.update()

        surface.blit(background_image)
        platform.render(surface)
        player.render(surface)

        window.flip()

if __name__ == "__main__":
    main()