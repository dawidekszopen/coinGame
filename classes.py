from random import randint, uniform
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

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
    def __init__(self, screenNew, playerClass: PlayerClass ,enemyClass: EnemyClass) -> None:
        self.screen = screenNew
        self.enemy = enemyClass

        self.player = playerClass


        self.attack = Button(
            self.screen,
            443, 574, 305, 64,
            text="attack",
            onClick= lambda: self.attackCoin(),
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
        )

        self.items = Button(
            self.screen,
            443, 643, 305, 64,
            text="items",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
        )

        self.defe = Button(
            self.screen,
            443, 712, 305, 64,
            text="def",
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
        )

        self.enemyHp = ProgressBar(
            self.screen, 
            454, 50, 154, 20, 
            lambda: self.enemy.hp * 0.01
        )


        self.moneta = Button(
            self.screen,
            521, 601, 150, 150,
            radius=100,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            text="rzuć monetą",
            onClick= lambda: self.coinFlip()
        )

        self.moneta.hide()

    def updateEnemyClass(self, enemyClass: EnemyClass):
        self.enemy = enemyClass

    def update(self):
        self.attack.draw()
        self.items.draw()
        self.defe.draw()
        self.enemyHp.draw()
        self.moneta.draw()

  
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