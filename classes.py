from random import randint, uniform

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import pygame

class PlayerClass():
    def __init__(self) -> None:
        self.name =''
        self.hp = 100
        self.attack = 5
        self.crit = {'min': 1.0, 'max': 1.5}

    
    def attackEnemy(self):
        if randint(0, 100) < 50:
            dmg = round(self.attack * uniform(self.crit['min'], self.crit['max']), 1)
            print(dmg)
            return dmg
        else:
            print('attack nie udany')
            return 0


class EnemyClass():
    def __init__(self, hp, attack) -> None:
        self.hp = hp
        self.attack = attack

    def getDmg(self, dmg):
        self.hp -= dmg



class GameClass():
    def __init__(self, playerClass: PlayerClass ,enemyClass: EnemyClass) -> None:
        self.enemy = enemyClass
        self.player = playerClass
        self.running = True

        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('coinGame')

        self.font = pygame.font.Font('font/JMH Typewriter.ttf', 32)


        pygame.draw.rect(self.screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)
        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)

        pygame.draw.rect(self.screen, (217, 217, 217), pygame.Rect(454, 75, 153, 286)) #todo: zmienić to w teksture enemy



        self.attack = Button(
            self.screen,
            443, 574, 305, 64,
            text="attack",
            onClick= lambda: self.attackCoin(),
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font
        )

        self.items = Button(
            self.screen,
            443, 643, 305, 64,
            text="items",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font
        )

        self.defe = Button(
            self.screen,
            443, 712, 305, 64,
            text="def",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font
        )



        self.moneta = Button(
            self.screen,
            521, 601, 150, 150,
            radius=100,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            text="rzuć monetą",
            onClick= lambda: self.coinFlip(),
            font=pygame.font.Font('font/JMH Typewriter.ttf', 20)
        )
    
        self.moneta.hide()

        self.enemyHp = ProgressBar(
            self.screen, 
            454, 50, 154, 20, 
            lambda: self.enemy.hp * 0.01
        )

    def updateEnemyClass(self, enemyClass: EnemyClass):
        self.enemy = enemyClass

    def update(self):


        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)
        self.attack.draw()
        self.items.draw()
        self.defe.draw()
        self.enemyHp.draw()
        self.moneta.draw()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()


  
    def attackCoin(self):
        self.attack.hide()
        self.items.hide()
        self.defe.hide()

        self.moneta.show()

    def coinFlip(self):
        self.enemy.getDmg(self.player.attackEnemy())

        self.attack.show()
        self.items.show()
        self.defe.show()

        self.moneta.hide()