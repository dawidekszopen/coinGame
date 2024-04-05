import pygame
import classes

gracz = classes.PlayerClass()

enemy = classes.EnemyClass(100, 12, 'img/enemy.png')

gra = classes.GameClass(gracz, enemy)


def main():
    while gra.running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                gra.running = False

        gra.update(events)


if __name__ == "__main__":
    main()