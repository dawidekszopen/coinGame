from random import randint, uniform

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import pygame

class MobClass():
    def __init__(self, hp, attack) -> None:
        self.hp = hp
        self.attack = attack
        self.lastDmgGiven = 0

    def getDmg(self, dmg):
        self.hp -= dmg

    def attackFunction(self):
        if randint(0, 100) < 50:
            dmg = round(self.attack * uniform(self.crit['min'], self.crit['max']), 1)
            self.lastDmgGiven = dmg
            print(dmg)
            return dmg
        else:
            print('attack nie udany')
            self.lastDmgGiven = 0
            return 0

class PlayerClass(MobClass):
    def __init__(self) -> None:
        super().__init__(100, 5)
        self.name =''
        self.crit = {'min': 1.0, 'max': 1.5}


class EnemyClass(MobClass):
    def __init__(self, hp, attack) -> None:
        super().__init__(hp, attack)



class GameClass():
    def __init__(self, playerClass: PlayerClass ,enemyClass: EnemyClass) -> None:
        self.enemy = enemyClass
        self.player = playerClass
        self.running = True

        self.givenDmg = 0

        self.playerTour = True

        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('coinGame')

        self.font = pygame.font.Font('font/JMH Typewriter.ttf', 25)

        #*LAYOUT
        pygame.draw.rect(self.screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)

        pygame.draw.rect(self.screen, (217, 217, 217), pygame.Rect(454, 75, 153, 286)) #todo: zmienić to w teksture enemy



        #*PRZYCISKI

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

        #*ENEMY HP
        self.enemyHp = ProgressBar(
            self.screen, 
            454, 50, 154, 20, 
            lambda: self.enemy.hp * 0.01
        )

    def updateEnemyClass(self, enemyClass: EnemyClass):
        self.enemy = enemyClass

    def update(self):
        #*INFO

        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)
        self.infoHp = self.font.render(f'hp: {self.player.hp}/100', True, (255, 255, 255))
        self.screen.blit(self.infoHp, ((166 - (self.infoHp.get_size()[0]/2))+38, 577))

        self.infoAttack1 = self.font.render('Zadałeś przeciwnikowi', True, (255, 255, 255))
        self.infoAttack2 = self.font.render('Przeciwnik zadał', True, (255, 255, 255))
        self.infoDmg = self.font.render(f'{self.givenDmg} dmg', True, (255, 255, 255))



        if self.playerTour:
            self.screen.blit(self.infoAttack1, ((166 - (self.infoAttack1.get_size()[0]/2))+38, 643))
        else:
            self.screen.blit(self.infoAttack2, ((166 - (self.infoAttack2.get_size()[0]/2))+38, 643))

        self.screen.blit(self.infoDmg, ((166 - (self.infoDmg.get_size()[0]/2))+38, 673))



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
        self.enemy.getDmg(self.player.attackFunction())
        
        self.playerTour = False
        
        self.attack.show()
        self.items.show()
        self.defe.show()

        self.moneta.hide()