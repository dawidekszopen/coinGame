import pygame

#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów


pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('coinGame')

running = True

def main():
    global running

    pygame.draw.rect(screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)
    pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)
    pygame.draw.rect(screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()


if __name__ == "__main__":
    main()