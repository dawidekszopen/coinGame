from random import randint, uniform

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import pygame



class MobClass():
    def __init__(self, hp, attack, minCrit, maxCrit) -> None:
        self.hp = hp
        self.attack = attack
        self.lastDmgGiven = 0
        self.crit = {'min': minCrit, 'max': maxCrit}

    def getDmg(self, dmg):
        self.hp -= dmg
        self.hp = round(self.hp, 1)

    def attackFunction(self):
        if randint(0, 100) < 50:
            dmg = round(self.attack * uniform(self.crit['min'], self.crit['max']), 1)
            self.lastDmgGiven = dmg
            return dmg
        else:
            self.lastDmgGiven = 0
            return 0



class PlayerClass(MobClass):
    def __init__(self) -> None:
        super().__init__(100, 5, 1.0, 1.5)
        self.name =''
       

class EnemyClass(MobClass):
    def __init__(self, hp, attack) -> None:
        super().__init__(hp, attack, 1.2, 1.7)



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


        self.infoText = f'hp: {self.player.hp}/100\n'

        self.ENEMYATTACKTIMER = pygame.event.custom_type()
        self.enemyAttackTimer = pygame.event.Event(self.ENEMYATTACKTIMER)

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

        self.monetaImg = pygame.image.load('img/coin.png')
        self.moneta = Button(
            self.screen,
            521, 601, 150, 150,
            radius=100,
            inactiveColour=(207, 155, 31),
            hoverColour=(207, 177, 31),
            pressedColour=(209, 201, 39),
            onClick= lambda: self.coinFlip(),
            font=pygame.font.Font('font/JMH Typewriter.ttf', 20),
            image=self.monetaImg
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

    def update(self, events):
        #*INFO

        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)


        self.infoTextRenderer(self.infoText, (48,577), (333, 220))


        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)
        self.attack.draw()
        self.items.draw()
        self.defe.draw()
        self.enemyHp.draw()
        self.moneta.draw()

        for event in events:
            if event == self.enemyAttackTimer:
                    if self.playerTour == False:
                        self.player.getDmg(self.enemy.attackFunction())
                        self.playerTour = True
                        self.updateInfo()
                        self.attack.show()
                        self.items.show()
                        self.defe.show()







        pygame_widgets.update(events)
        pygame.display.update()


    def infoTextRenderer(self, text, pos, size: pygame.Vector2):
        words = [word.split(' ') for word in text.splitlines()]
        space = self.font.size(' ')[0]

        maxWidth = size[0]
        x,y = pos

        for line in words:
            for word in line:
                wordSurface = self.font.render(word, True, pygame.Color('white'))
                wordWidth, wordHeight = wordSurface.get_size()

                if x + wordWidth >= maxWidth:
                    x = pos[0]
                    y += wordHeight
                
                self.screen.blit(wordSurface, (x, y))
                x += wordWidth + space
            x = pos[0]
            y += wordHeight

  
    def attackCoin(self):
        if self.playerTour:
            self.attack.hide()
            self.items.hide()
            self.defe.hide()

            self.moneta.show()

    def coinFlip(self):
        self.enemy.getDmg(self.player.attackFunction())
        self.playerTour = False
        
        pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)

        self.updateInfo()

        self.moneta.hide()

    def updateInfo(self):
        if self.playerTour == False:
            if self.player.lastDmgGiven == 0:
                self.infoText = f'hp: {self.player.hp}/100\n\n'\
                                'Nie udało ci się zaatakować przeciwnik\n'
            else:
                self.infoText = f'hp: {self.player.hp}/100\n\n'\
                                'Zadałeś przeciwnikowi\n'\
                                f'{self.player.lastDmgGiven} obrażeń'
        else:
            if self.enemy.lastDmgGiven == 0:
                self.infoText = f'hp: {self.player.hp}/100\n\n'\
                                'Przeciwnikowi nie udało się ciebie zaatakować\n'
            else:
                self.infoText = f'hp: {self.player.hp}/100\n\n'\
                                'przeciwnik zadał\n'\
                                f'{self.enemy.lastDmgGiven} obrażeń'
