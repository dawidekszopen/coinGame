from random import randint

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

import pygame

import jsonSaveLoad
#https://colorhunt.co/palette/35374b34495550727b78a083 - paleta kolorów

class MobClass():
    def __init__(self, hp:int, dmg:int, critRate: int, defence: list, name: str, img: str, x:int, y:int) -> None:
        self.hp = hp
        self.fullHp = hp
        self.dmg = dmg
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
                dmg = self.dmg * randint(2, 5)
            else:
                dmg = self.dmg

            if defene:
                dmg = dmg - randint(self.defence[0], self.defence[1])
                
            self.lastDmgGiven = dmg
            
            return dmg
        else:
            self.lastDmgGiven = 0
            return 0

    def heal(self, hpUP):
        self.hp += hpUP

        if self.hp > 100:
            self.hp -= self.hp - self.fullHp


class PlayerClass(MobClass):
    def __init__(self) -> None:
        super().__init__(100, 10, 5, (2, 8), 'gracz', 'img/player.png', 62, 231)
        self.eq = [
            [
                {'name': 'Pitne mleko smoka', 'value': 99, 'regeneration': 20},
                {'name': 'Górska Potęga', 'value': 99, 'regeneration': 40},
                {'name': 'Placek trolla', 'value': 99, 'regeneration': 50},
                {'name': 'Placki minotaura', 'value': 99, 'regeneration': 60},
                {'name': 'Mglisty Eliksir', 'value': 99, 'regeneration': 65},
                {'name': 'Eliksir zdrowia', 'value': 99, 'regeneration': 100}
            ],
            [
                {'miejsce': 'głowa', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
                {'miejsce': 'klatka', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
                {'miejsce': 'nogi', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
                {'miejsce': 'stopy', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
                {'miejsce': 'broń', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
                {'miejsce': 'palce', 'item': '', 'rarity': '', 'stats': {}, 'img': ''},
            ]
        ]
        self.animaton = False    
        self.itemsList = jsonSaveLoad.load('items.json')
        self.newItem = {}

    def setNewItem(self):
        for i in range(len(self.eq[1])):
            if self.newItem['miejsce'] == self.eq[1][i]['miejsce']:
                self.eq[1][i]['item'] = self.newItem['item']
                self.eq[1][i]['rarity'] = self.newItem['rarity']
                self.eq[1][i]['stats'] = self.newItem['stats']
                self.eq[1][i]['img'] = self.newItem['img']
                break

    def updateStats(self):
        for i in range(len(self.eq[1])):
            if 'hp' in self.eq[1][i]['stats']:
                self.fullHp += self.eq[1][i]['stats']['hp']

                if self.fullHp < self.hp:
                    self.hp = self.fullHp
            elif 'dmg' in self.eq[1][i]['stats'] and 'crit' in self.eq[1][i]['stats']:
                self.critRate += self.eq[1][i]['stats']['crit']
                self.dmg += self.eq[1][i]['stats']['crit']

                if self.dmg <= 0:
                    self.dmg = 1

    def printStats(self):
        print(f'''
-hp: {self.hp} / {self.fullHp}
-dmg: {self.dmg}
-crit: {self.critRate}
''')
#!=======================================================================================
#!ITEMY PO PRZECIWNIKU
#!=======================================================================================

    def createItem(self) -> dict:
        rarity = self.itemsList[0][randint(0, len(self.itemsList[0]))-1]
        item = self.itemsList[1][randint(0, len(self.itemsList[1]))-1]

        newItem = {'item': item['nazwa'], 
                   'rarity': rarity['nazwa']}

        if 'hp' in item['stats']:
            newItem['stats'] = {'hp': item['stats']['hp'] + randint(rarity['stats']['hp'][0], rarity['stats']['hp'][1])}
        elif 'dmg' in item['stats'] and 'crit' in item['stats']:
            newItem['stats'] = {
                'dmg': item['stats']['dmg'] + randint(rarity['stats']['dmg'][0], rarity['stats']['dmg'][1]),
                'crit': item['stats']['crit'] + randint(rarity['stats']['crit'][0], rarity['stats']['crit'][1])
                }

        newItem['miejsce'] = item['miejsce']

        if item['imgNazwa'] == '?':
            newItem['img'] = 'idk'
        else:
            newItem['img'] = f'{item['imgNazwa']}{self.itemsList[0].index(rarity)+1}'
            

        self.newItem = newItem

class EnemyClass(MobClass):
    def __init__(self, hp:int, attack:int, img:str, name:str, x:int, y:int) -> None:
        super().__init__(hp, attack, 7, (1, 2), name, img, x, y) 


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
            font=self.font,
            onClick= lambda: self.tourChoose('D'),
            textColour=(189,220,222),
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
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
            751, 10, 35, 35,
            image=returnImg,
            inactiveColour=(53, 55, 75),
            hoverColour=(53, 55, 75),
            pressedColour=(53, 55, 75),
            onClick= lambda: self.tourChoose('R')
        )

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
            onClick= lambda: self.tourChoose('NI')
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

        self.hideWidgets(self.yesNextEnemyB, self.noNextEnemyB, self.returnButton1, self.returnButton2, self.defencebutton, self.moneta)



        self.ifPlayerDidLoop = False

        self.nextEnemyCheck = False


        self.chooseItemOn = False

        self.yesNewItem = Button(
            self.screen,
            243, 583, 120, 120,
            textColour=(189,220,222),
            inactiveColour=(80, 114, 123),
            pressedColour=(53, 55, 75),
            hoverColour=(120, 160, 131),
            font=self.font,
            text="tak",
            onClick= lambda: self.tourChoose('NIW')
        )

        self.noNewItem = Button(
            self.screen,
            437, 583, 120, 120,
            textColour=(189,220,222),
            inactiveColour=(80, 114, 123),
            pressedColour=(53, 55, 75),
            hoverColour=(120, 160, 131),
            font=self.font,
            text="nie",
            onClick= lambda: self.tourChoose('W')
        )
        self.hideWidgets(self.yesNewItem, self.noNewItem)


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
        self.drawWidgets()
#!=======================================================================================
#!WYBUR PRZEDMIOTU
#!=======================================================================================
        if self.chooseItemOn == True:
            self.drawEqLayout()

            self.textRenderer(f'''Znalazłeś {self.player.newItem['item']} Miejsce: {self.player.newItem['miejsce']}
Statystyki:
{f"* hp: ??" if 'hp' in self.player.newItem['stats'] else ''}
{f'* dmg: ??' if 'dmg' in self.player.newItem['stats'] else ''}
{f'* critRate: ??' if 'crit' in self.player.newItem['stats'] else ''}

Chcesz wziąć ten przedmiot?
''',
            [198, 347], pygame.Vector2(1000, 149))
#!=======================================================================================
#!WALKA
#!=======================================================================================
        else:
            self.bg.blit(self.bgImg, (0, 0))#*tło

            pygame.draw.rect(self.screen, (53, 55, 75), pygame.Rect(0, 550, 800, 250), border_top_left_radius=20, border_top_right_radius=20)

            if self.eqOn == False:
                self.enemyHp.show()
                pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(38, 566, 333, 220), border_radius=10)
                self.textRenderer(self.infoText, (48,577), (333, 220))
                pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(429, 566, 333, 220), border_radius=10)
            else:
                self.drawEqLayout()
                self.textRenderer(f'''Twoje statystki:
hp: {self.player.hp} / {self.player.fullHp}
dmg: {self.player.dmg}
critRate: {self.player.critRate}''', [238, 315], pygame.Vector2(1000, 120))


            if self.player.hp <= 0:
                self.updateInfo('zostałeś pokonany')

                self.hideWidgets(self.attack, self.defence, self.items)
            elif self.player.hp > 0 and self.eqOn == False:
                self.screen.blit(self.player.img, self.player.pos)#* gracz


            if self.enemy.hp <= 0 and self.nextEnemyCheck == False:
                self.askNextRound()
            elif self.enemy.hp > 0 and self.eqOn == False:
                self.screen.blit(self.enemy.img, self.enemy.pos)#*enemy


            if self.player.animaton:
                if self.player.pos.x >= 952:
                    self.player.pos.x = -152
                    self.ifPlayerDidLoop = True

                
                self.player.pos.x += 450 * self.dt

                if self.player.pos.x >= 61 and self.ifPlayerDidLoop:
                    self.generateNewEnemy()
                    self.player.animaton = False        
                    self.updateInfo('napotkałeś kolejnego przeciwnika')
                    self.playerTour = True


                    self.showWidgets(self.attack, self.items, self.defence, self.enemyHp)

                    self.nextEnemyCheck = False
                    self.ifPlayerDidLoop = False 


        for event in events:
            if event == self.enemyAttackTimer:
                    if self.playerTour == False and self.enemy.hp > 0:
                        self.player.getDmg(self.enemy.attackFunction(self.player.defenceON))
                        self.playerTour = True



                        if self.enemy.lastDmgGiven == 0:
                            self.updateInfo(f'przeciwnik chybił swój atak')
                        else:
                            self.updateInfo(f'przeciwnik zadał ci {self.enemy.lastDmgGiven} obrażeń')


                        self.showWidgets(self.attack, self.defence, self.items)


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
            self.hideWidgets(self.attack, self.defence, self.items)
            
            self.returnButton1.show()

            self.moneta.show()
        elif choose == 'D':
            self.hideWidgets(self.attack, self.defence, self.items)
            
            self.returnButton1.show()

            self.defencebutton.show()
        elif choose == 'I':
            self.hideWidgets(self.attack, self.defence, self.items, self.enemyHp)

            self.returnButton2.show()

            self.eqOn = True

            for i in range(len(self.itemsButton)):
                self.itemsButton[i].show()

        elif choose == 'R':
            self.eqOn = False
            for i in range(len(self.itemsButton)):
                self.itemsButton[i].hide()
            
            self.showWidgets(self.attack, self.defence, self.items, self.enemyHp)
            self.hideWidgets(self.returnButton1, self.returnButton2, self.defencebutton, self.moneta)
        elif choose == 'W':
            self.chooseItemOn = False
            self.hideWidgets(self.yesNewItem, self.noNewItem)

            self.nextEnemyCheck = True
            self.player.animaton = True
            self.updateInfo(f'Zostawiłeś ze sobą {self.player.newItem['item']} {self.player.newItem['rarity']}')
        elif choose == 'NIW':
            self.chooseItemOn = False
            self.player.setNewItem()
            self.hideWidgets(self.yesNewItem, self.noNewItem)

            self.nextEnemyCheck = True
            self.player.animaton = True
            self.player.updateStats()
            self.player.printStats()
            self.updateInfo(f'Wziełeś ze sobą {self.player.newItem['item']} {self.player.newItem['rarity']}')
        elif choose == 'NI':
            self.player.createItem()
            self.chooseItemOn = True
            self.hideWidgets(self.attack, self.items, self.defence, self.enemyHp, self.yesNextEnemyB, self.noNextEnemyB)
            self.showWidgets(self.yesNewItem, self.noNewItem)

    
#!=======================================================================================
#!ATAK
#!=======================================================================================

    def coinFlip(self):
        self.enemy.getDmg(self.player.attackFunction(self.enemy.defenceON))
        self.playerTour = False
        
        pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)

        if self.player.lastDmgGiven == 0:
            self.updateInfo(f'nie udało ci się zaatakować przeciwnika')
        else:
            self.updateInfo(f'zadałeś przeciwnikowi {self.player.lastDmgGiven} obrażeń')

        self.hideWidgets(self.moneta, self.returnButton1)

#!=======================================================================================
#!UŻYCIE DEFENSYWY
#!=======================================================================================

    def defenceTour(self):
        self.hideWidgets(self.defencebutton, self.returnButton1)

        self.player.defenceON = True
        self.playerTour = False
        pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)
        self.updateInfo(f'postanowiłeś się ochronić')

#!=======================================================================================
#!AKTUALIZACJA miejsce
#!=======================================================================================
        
    def updateInfo(self, text:str):
        self.infoText = f'hp: {self.player.hp}/{self.player.fullHp}\n\n'\
                f'{text}'
    
#!=======================================================================================
#!WYŚWIETLANIE TEKSTU
#!=======================================================================================

    def textRenderer(self, text: str, pos: list[int], size: pygame.Vector2):
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
    def drawEqLayout(self):
        self.screen.fill((53, 55, 75))

        self.screen.blit(pygame.image.load('img/stickMan.png'), (29, 25))

        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(91, 45, 48, 48), width=2)#głowa
        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(21, 264, 48, 48), width=2)#palce
        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(162, 264, 48, 48), width=2)#broń
        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(91, 190, 48, 48), width=2)#klata
        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(91, 323, 48, 48), width=2)#nogi
        pygame.draw.rect(self.screen, (252, 81, 81), pygame.Rect(91, 420, 48, 48), width=2)#stopy


        self.textRenderer(f'''Twoje rzeczy:
-głowa: {self.player.eq[1][0]['item']} {self.player.eq[1][0]['rarity']}  {f"hp: {self.player.eq[1][0]['stats']['hp']}" if 'hp' in self.player.eq[1][0]['stats'] else ''}
-klata: {self.player.eq[1][1]['item']} {self.player.eq[1][1]['rarity']} {f"hp: {self.player.eq[1][1]['stats']['hp']}" if 'hp' in self.player.eq[1][1]['stats'] else ''}
-palce: {self.player.eq[1][5]['item']} {self.player.eq[1][5]['rarity']} {f'hp: {self.player.eq[1][5]['stats']['hp']}' if 'hp' in self.player.eq[1][5]['stats'] else ''}
-broń: {self.player.eq[1][4]['item']} {self.player.eq[1][4]['rarity']} {f'dmg: {self.player.eq[1][4]['stats']['dmg']}\n' if 'dmg' in self.player.eq[1][4]['stats'] else ''} {f'critRate: {self.player.eq[1][4]['stats']['crit']}' if 'crit' in self.player.eq[1][4]['stats'] else ''}
-nogi: {self.player.eq[1][2]['item']} {self.player.eq[1][2]['rarity']} {f'hp: {self.player.eq[1][2]['stats']['hp']}' if 'hp' in self.player.eq[1][2]['stats'] else ''}
-stopy: {self.player.eq[1][3]['item']} {self.player.eq[1][3]['rarity']} {f'hp: {self.player.eq[1][3]['stats']['hp']}' if 'hp' in self.player.eq[1][3]['stats'] else ''}''', 
        [238, 64], pygame.Vector2(1000, 239))

        #głowa
        if self.player.eq[1][0]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][0]['img']}.png'), (91, 45))
        
        #klata
        if self.player.eq[1][1]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][1]['img']}.png'), (91, 190))

        #palce
        if self.player.eq[1][5]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][5]['img']}.png'), (21, 264))
    
        #bron
        if self.player.eq[1][4]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][4]['img']}.png'), (162, 264))

        #nogi
        if self.player.eq[1][2]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][2]['img']}.png'), (91, 323))

        #stopy
        if self.player.eq[1][3]['img'] != '':
            self.screen.blit(pygame.image.load(f'img/icons/{self.player.eq[1][3]['img']}.png'), (91, 420))

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

        self.itemsButton[0].setOnClick(lambda: self.useItem(0, self.player.eq[0][0]['regeneration']))
        self.itemsButton[1].setOnClick(lambda: self.useItem(1, self.player.eq[0][1]['regeneration']))
        self.itemsButton[2].setOnClick(lambda: self.useItem(2, self.player.eq[0][2]['regeneration']))
        self.itemsButton[3].setOnClick(lambda: self.useItem(3, self.player.eq[0][3]['regeneration']))
        self.itemsButton[4].setOnClick(lambda: self.useItem(4, self.player.eq[0][4]['regeneration']))
        self.itemsButton[5].setOnClick(lambda: self.useItem(5, self.player.eq[0][5]['regeneration']))


    def updateTextItemButon(self):
        for i in range(len(self.itemsButton)):
            self.itemsButton[i].setText(f'{self.player.eq[0][i]['name']} {self.player.eq[0][i]['value']}')
            
#!=======================================================================================
#!UŻYWANIE PRZEDMIOTÓW
#!=======================================================================================

    def useItem(self, id:int, hp:int):
        if(self.player.hp < 100):
            self.eqOn = False


            for i in range(len(self.itemsButton)):
                self.itemsButton[i].hide()
            
            self.player.eq[0][id]['value'] -= 1
            self.updateTextItemButon()
            
            self.returnButton2.hide()

            self.player.heal(hp)
            pygame.time.set_timer(self.ENEMYATTACKTIMER, 1500)
            self.updateInfo(f'użyłeś przedmiotu {self.player.eq[0][id]['name']}')
            self.playerTour = False
        else:
            self.tourChoose('R')

#!=======================================================================================
#!NASTĘPNY PRZECIWNIK
#!=======================================================================================

    def askNextRound(self):
        pygame.draw.rect(self.screen, (52, 73, 85), pygame.Rect(215, 275, 370, 250), border_radius=25)
        self.updateInfo(f'udało ci się pokonać przeciwnika')
        self.enemyHp.hide()
        text = self.font.render("chcesz grać dalej?", True, (255, 255, 255))
        self.screen.blit(text, (280,291))

        self.hideWidgets(self.attack, self.defence, self.items)

        self.showWidgets(self.yesNextEnemyB, self.noNextEnemyB)


#!=======================================================================================
#!WIDGETS
#!=======================================================================================

    def showWidgets(self, *widgets):
        for widget in widgets:
            widget.show()

    def hideWidgets(self, *widgets):
        for widget in widgets:
            widget.hide()

    def drawWidgets(self):
        self.attack.draw()
        self.items.draw()
        self.defence.draw()
        self.moneta.draw()
        self.defencebutton.draw()
        self.returnButton1.draw()
        self.returnButton2.draw()
        self.enemyHp.draw()

        for i in range(len(self.itemsButton)):
            self.itemsButton[i].draw()

    def exitGame(self):
        self.running = False