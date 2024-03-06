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
wybor = pygame.display.set_mode((800, 800))

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
        onClick= lambda: enemy.getDmg(gracz.attackEnemy()),
        inactiveColour=(200, 50, 0),
        pressedColour=(0,200,0)
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

    enemyHp = ProgressBar(screen, 
        454, 50, 154, 20, 
        lambda: enemy.hp * 0.01
    )

    tlo = pygame.draw.rect(wybor, (120, 160, 131), pygame.Rect(163, 150, 500, 500))

    orzel = Button(
        wybor,
        189, 325, 150, 150,
        radius=100,
        inactiveColour=(53, 55, 75),
        pressedColour=(80, 114, 123),
        hoverColour=(52, 73, 85),
        text="orzeł"
    )

    reszka = Button(
        wybor,
        485, 325, 150, 150,
        radius=100,
        inactiveColour=(53, 55, 75),
        pressedColour=(80, 114, 123),
        hoverColour=(52, 73, 85),
        text="reszka"
    )


    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False


        attack.draw()
        items.draw()
        defe.draw()
        enemyHp.draw()

        orzel.draw()
        reszka.draw()
        
       

        pygame_widgets.update(events)
        pygame.display.update()


if __name__ == "__main__":
    main()