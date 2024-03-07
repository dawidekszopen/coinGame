import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import classes

#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów

gracz = classes.player()

enemy = classes.enemy(100, 5)

pygame.init()

screen = pygame.display.set_mode((800, 800))

pygame.display.set_caption('coinGame')


gra = classes.game(screen)

running = True


def main():
    global running

    pygame.draw.rect(screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)
    pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)


    pygame.draw.rect(screen, (217, 217, 217), pygame.Rect(454, 75, 153, 286))

    while running:
        pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        
        gra.update()

        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == "__main__":
    main()