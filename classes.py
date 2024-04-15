from random import randint

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import pygame

import jsonSaveLoad
#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów

class MobClass():
    def __init__(self, hp, attack, critRate: int, defence: list, name: str, img: str, x:int, y:int) -> None:
        self.hp = hp
        self.attack = attack
        self.lastDmgGiven = 0
        self.critRate = critRate
        self.defence = defence
        self.defenceON = False
        self.name = name
        self.img = pygame.image.load(img)
        self.pos = pygame.Vector2(x, y) 


    def getDmg(self, dmg):
        self.hp -= dmg

    def attackFunction(self, defene: bool):
        if randint(0, 100) < 50:
            if randint(0, 100) < self.critRate:
                dmg = self.attack * randint(2, 5)
            else:
                dmg = self.attack

            if defene:
                dmg = dmg - randint(self.defence[0], self.defence[1])
                
            self.lastDmgGiven = dmg
            
            return dmg
        else:
            self.lastDmgGiven = 0
            return 0

    def heal(self, hpUP):
        self.hp += hpUP


class PlayerClass(MobClass):
    def __init__(self) -> None:
        super().__init__(100, 10, 5, (2, 8), 'gracz', 'img/player.png', 62, 231)
        self.eq = [
            {'name': 'Pitne mleko smoka', 'value': 99, 'regeneration': 2},
            {'name': 'Górska Potęga', 'value': 99, 'regeneration': 4},
            {'name': 'Placek trolla', 'value': 99, 'regeneration': 5},
            {'name': 'Placki minotaura', 'value': 99, 'regeneration': 6},
            {'name': 'Mglisty Eliksir', 'value': 99, 'regeneration': 15},
            {'name': 'Eliksir zdrowia', 'value': 99, 'regeneration': 20}
        ]
        self.animaton = False    

class EnemyClass(MobClass):
    def __init__(self, hp:int, attack:int, img:str, name:str, x:int, y:int) -> None:
        super().__init__(hp, attack, 7, (1, 2), name, img, x, y) 
        self.fullHp = hp


class GameClass():
    def __init__(self, playerClass: PlayerClass) -> None:
        self.player = playerClass
        self.running = True



        self.enemy: EnemyClass 
        self.enemyList = jsonSaveLoad.load('enemy.json')
        self.generateNewEnemy()


        self.givenDmg = 0

        self.playerTour = True

        self.eqOn = False

        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('coinGame')

        self.clock = pygame.time.Clock()

        self.dt = None 



        self.font = pygame.font.Font('font/JMH Typewriter.ttf', 25)


        self.infoText = f'hp: {self.player.hp}/100\n'

        self.ENEMYATTACKTIMER = pygame.event.custom_type()
        self.enemyAttackTimer = pygame.event.Event(self.ENEMYATTACKTIMER)

        self.bg = pygame.display.set_mode((800, 800))
        self.bgImg = pygame.image.load('img/dangeon.png')

        #*LAYOUT

        #*FIRST
        self.attack = Button(
            self.screen,
            443, 574, 305, 64,
            text="attack",
            onClick= lambda: self.tourChoose('A'),
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font,
            textColour=(189,220,222)
        )

        self.defence = Button(
            self.screen,
            443, 643, 305, 64,
            text="def",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font,
            onClick= lambda: self.tourChoose('D'),
            textColour=(189,220,222)
        )
        
        self.items = Button(
            self.screen,
            443, 712, 305, 64,
            text="items",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font,
            textColour=(189,220,222),
            onClick= lambda: self.tourChoose('I')
        )

        #* MONETA
        monetaImg = pygame.image.load('img/coin.png')
        self.moneta = Button(
            self.screen,
            521, 601, 150, 150,
            radius=100,
            inactiveColour=(207, 155, 31),
            hoverColour=(207, 177, 31),
            pressedColour=(209, 201, 39),
            onClick= lambda: self.coinFlip(),
            image=monetaImg
        )
    
        self.moneta.hide()

        #*DEF

        self.defencebutton = Button(
            self.screen,
            443, 643, 306, 64,
            text="chcesz to zrobić?",
            font=self.font,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            textColour=(189,220,222),
            onClick= lambda: self.defenceTour()
        )

        self.defencebutton.hide()


        #*ITEMS

        self.itemsButton = []
        self.makeItemsButton()
        self.updateTextItemButon()

        for i in range(len(self.itemsButton)):
            self.itemsButton[i].hide()

        #*RETURN
        returnImg = pygame.image.load('img/return.png')
        self.returnButton1 = Button(
            self.screen,
            717, 576, 35, 35,
            image=returnImg,
            inactiveColour=(52, 73, 85),
            hoverColour=(52, 73, 85),
            pressedColour=(52, 73, 85),
            onClick= lambda: self.tourChoose('R')
        )

        self.returnButton2 = Button(
            self.screen,
            751, 558, 35, 35,
            image=returnImg,
            inactiveColour=(53, 55, 75),
            hoverColour=(53, 55, 75),
            pressedColour=(53, 55, 75),
            onClick= lambda: self.tourChoose('R')
        )

        self.returnButton1.hide()
        self.returnButton2.hide()

        #*ENEMY HP
        self.enemyHp = ProgressBar(
            self.screen, 
            587, 200, 150, 20, 
            lambda: ((self.enemy.hp * 100)/self.enemy.fullHp) * 0.01
        )

        #*NEXT ENEMY

        self.yesNextEnemyB = Button(
            self.screen,
            243, 355, 120, 120,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font,
            textColour=(189,220,222),
            text="tak",
            onClick= lambda: self.nextEnemy()
        )

        self.noNextEnemyB = Button(
            self.screen,
            436, 355, 120, 120,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            font=self.font,
            textColour=(189,220,222),
            text="nie",
            onClick= lambda: self.exitGame()
        )

        self.yesNextEnemyB.hide()
        self.noNextEnemyB.hide()

        self.ifPlayerDidLoop = False

        self.nextEnemyCheck = False



    def generateNewEnemy(self):
        randEnemy = randint(1, len(self.enemyList)) 

        enemy = self.enemyList[randEnemy-1]
    
        self.enemy = EnemyClass(enemy['hp'], enemy['attack'], enemy['image'], enemy['name'], enemy['position'][0], enemy['position'][1])       


#!=======================================================================================
#!FUNKCJA UPDATE
#!=======================================================================================

    def update(self, events):
        self.clock.tick(60)
        self.dt = self.clock.tick(60) / 1000

        self.bg.blit(self.bgImg, (0, 0))#*tło


        pygame.draw.rect(self.screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)
        
        
        if self.eqOn == False:
            pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)
            self.infoTextRenderer(self.infoText, (48,577), (333, 220))
            pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)



        self.attack.draw()
        self.items.draw()
        self.defence.draw()
        self.moneta.draw()

        self.defencebutton.draw()

        self.returnButton1.draw()
        self.returnButton2.draw()

        for i in range(len(self.itemsButton)):
            self.itemsButton[i].draw()

        self.enemyHp.draw()


        if self.enemy.hp <= 0 and self.nextEnemyCheck == False:
            self.askNextRound()
        elif self.enemy.hp > 0:
            self.screen.blit(self.enemy.img, self.enemy.pos)#*enemy


        if self.player.hp <= 0:
            self.updateInfo('zostałeś pokonany')

            self.attack.hide()
            self.defence.hide()
            self.items.hide()
        else:
            self.screen.blit(self.player.img, self.player.pos)#* gracz

        if self.player.animaton:
            if self.player.pos.x >= 952:
                self.player.pos.x = -152
                self.ifPlayerDidLoop = True

            
            self.player.pos.x += 450 * self.dt

            if self.player.pos.x >= 61 and self.ifPlayerDidLoop:
                self.generateNewEnemy()
                self.enemyHp.show()
                self.player.animaton = False        
                self.updateInfo('napotkałeś kolejnego przeciwnika')
                self.playerTour = True
                self.attack.show()
                self.items.show()
                self.defence.show()




        for event in events:
            if event == self.enemyAttackTimer:
                    if self.playerTour == False and self.enemy.hp > 0:
                        self.player.getDmg(self.enemy.attackFunction(self.player.defenceON))
                        self.playerTour = True



                        if self.enemy.lastDmgGiven == 0:
                            self.updateInfo(f'przeciwnik chybił swój atak')
                        else:
                            self.updateInfo(f'przeciwnik zadał ci {self.enemy.lastDmgGiven} obrażeń')
                        
                        self.attack.show()
                        self.items.show()
                        self.defence.show()

                        self.returnButton1.hide()
                        self.returnButton2.hide()

                        pygame.time.set_timer(self.ENEMYATTACKTIMER, 0)

                        if self.player.defenceON:
                            self.player.defenceON = False

        
        

        pygame_widgets.update(events)
        pygame.display.update()

        
        

#!=======================================================================================
#!WYBRANIE AKCJI
#!=======================================================================================
    def tourChoose(self, choose:str):
        if choose == 'A':
            self.returnButton1.show()

            self.attack.hide()
            self.items.hide()
            self.defence.hide()

            self.moneta.show()
        elif choose == 'D':
            self.returnButton1.show()

            self.defencebutton.show()

            self.attack.hide()
            self.items.hide()
            self.defence.hide()
            
        elif choose == 'I':
            self.returnButton2.show()


            self.attack.hide()
            self.items.hide()
            self.defence.hide()
            self.eqOn = True

            for i in range(len(self.itemsButton)):
                self.itemsButton[i].show()
        elif choose == 'R':
            self.eqOn = False
            for i in range(len(self.itemsButton)):
                self.itemsButton[i].hide()
            
            self.moneta.hide()

            self.attack.show()
            self.items.show()
            self.defence.show()

            self.returnButton1.hide()
            self.returnButton2.hide()
            self.defencebutton.hide()

#!=======================================================================================
#!ATAK
#!=======================================================================================

    def coinFlip(self):
        self.returnButton1.hide()
        self.enemy.getDmg(self.player.attackFunction(self.enemy.defenceON))
        self.playerTour = False
        
        pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)

        if self.player.lastDmgGiven == 0:
            self.updateInfo(f'nie udało ci się zaatakować przeciwnika')
        else:
            self.updateInfo(f'zadałeś przeciwnikowi {self.player.lastDmgGiven} obrażeń')

        self.moneta.hide()

#!=======================================================================================
#!UŻYCIE DEFENSYWY
#!=======================================================================================

    def defenceTour(self):
        self.returnButton1.hide()
        self.defencebutton.hide()
        self.player.defenceON = True
        self.playerTour = False
        pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)
        self.updateInfo(f'postanowiłeś się ochronić')

#!=======================================================================================
#!AKTUALIZACJA TEKSTU
#!=======================================================================================
        
    def updateInfo(self, text:str):
        self.infoText = f'hp: {self.player.hp}/100\n\n'\
                f'{text}'
    
#!=======================================================================================
#!WYŚWIETLANIE TEKSTU
#!=======================================================================================

    def infoTextRenderer(self, text, pos, size: pygame.Vector2):
        words = [word.split(' ') for word in text.splitlines()]
        space = self.font.size(' ')[0]

        maxWidth = size[0]
        x,y = pos

        for line in words:
            for word in line:
                wordSurface = self.font.render(word, True, (242, 240, 240))
                wordWidth, wordHeight = wordSurface.get_size()

                if x + wordWidth >= maxWidth:
                    x = pos[0]
                    y += wordHeight
                
                self.screen.blit(wordSurface, (x, y))
                x += wordWidth + space
            x = pos[0]
            y += wordHeight

#!=======================================================================================
#!PRZYCISKI DO INVENTORY
#!=======================================================================================

    def makeItemsButton(self):
        butonpos = [[57, 576], [57, 649], [57, 723], 
                    [418, 576], [418, 649], [418, 723]]
        for i in range(6):
            self.itemsButton.append(
                Button(
                    self.screen,
                    butonpos[i][0], butonpos[i][1], 325, 53,
                    inactiveColour=(52, 73, 85),
                    pressedColour=(120, 160, 131),
                    hoverColour=(80, 114, 123),
                    font=self.font,
                    textColour=(189,220,222),
                    text=f'{i}'
                )
            )

        self.itemsButton[0].setOnClick(lambda: self.useItem(0, self.player.eq[0]['regeneration']))
        self.itemsButton[1].setOnClick(lambda: self.useItem(1, self.player.eq[1]['regeneration']))
        self.itemsButton[2].setOnClick(lambda: self.useItem(2, self.player.eq[2]['regeneration']))
        self.itemsButton[3].setOnClick(lambda: self.useItem(3, self.player.eq[3]['regeneration']))
        self.itemsButton[4].setOnClick(lambda: self.useItem(4, self.player.eq[4]['regeneration']))
        self.itemsButton[5].setOnClick(lambda: self.useItem(5, self.player.eq[5]['regeneration']))

    def updateTextItemButon(self):
        for i in range(len(self.itemsButton)):
            self.itemsButton[i].setText(f'{self.player.eq[i]['name']} {self.player.eq[i]['value']}')
            
#!=======================================================================================
#!UŻYWANIE PRZEDMIOTÓW
#!=======================================================================================

    def useItem(self, id:int, hp:int):
        if(self.player.hp < 100):
            self.eqOn = False


            for i in range(len(self.itemsButton)):
                self.itemsButton[i].hide()
            
            self.player.eq[id]['value'] -= 1
            self.updateTextItemButon()
            
            self.returnButton2.hide()

            self.player.heal(hp)
            pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)
            self.updateInfo(f'użyłeś przedmiotu {self.player.eq[id]['name']}')
            self.playerTour = False
        else:
            self.tourChoose('R')

#!=======================================================================================
#!NASTĘPNY PRZECIWNIK
#!=======================================================================================

    def askNextRound(self):
        self.updateInfo(f'udało ci się pokonać przeciwnika')
        self.enemyHp.hide()
        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(215, 275, 370, 250), border_radius=25)
        text = self.font.render("chcesz grać dalej?", True, (255, 255, 255))
        self.screen.blit(text, (280,291))

        self.yesNextEnemyB.show()
        self.noNextEnemyB.show()



    def nextEnemy(self):
        self.yesNextEnemyB.hide()
        self.noNextEnemyB.hide()

        self.nextEnemyCheck = True

        self.player.animaton = True


    def exitGame(self):
        self.running = False