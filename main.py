import pygame
from pygame_widgets.button import Button

import classes

#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów

gracz = classes.player()

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('coinGame')

running = True


def main():
    global running

    pygame.draw.rect(screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)
    pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)
    pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)

    pygame.draw.rect(screen, (217, 217, 217), pygame.Rect(454, 75, 153, 286))


    attack = Button(
        screen,
        443, 574, 305, 64,
        text="attack",
    )

    items = Button(
        screen,
        443, 643, 305, 64,
        text="items",
    )

    defe = Button(
        screen,
        443, 712, 305, 64,
        text="def",
    )

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False



        attack.draw()
        items.draw()
        defe.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()