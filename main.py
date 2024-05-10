import pygame
import classes

gracz = classes.PlayerClass()

gra = classes.GameClass(gracz)


def main():
    while gra.running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                gra.running = False

        gra.update(events)


if __name__ == "__main__":
    main()