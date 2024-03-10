import pygame
import classes

#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów

gracz = classes.PlayerClass()

enemy = classes.EnemyClass(100, 5)

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