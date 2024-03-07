from random import randint
from pygame_widgets.button import Button
from pygame_widgets.progressbar import ProgressBar

class player():
    def __init__(self) -> None:
        self.name =''
        self.hp = 100
        self.attack = 5

    
    def attackEnemy(self):
        if randint(0, 100) > 51:
            print('attack udany')
            return self.attack
        else:
            print('attack nie udany')
            return 0


class enemy():
    def __init__(self, hp, attack) -> None:
        self.hp = hp
        self.attack = attack

    def getDmg(self, dmg):
        self.hp -= dmg



class game():
    def __init__(self, screenNew) -> None:
        self.screen = screenNew

        self.doAttack = False

        


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
            lambda: 100 * 0.01
        )


        self.orzel = Button(
            self.screen,
            637, 625, 100, 100,
            radius=100,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            text="orzeł"
        )

        self.reszka = Button(
            self.screen,
            454, 625, 100, 100,
            radius=100,
            inactiveColour=(53, 55, 75),
            pressedColour=(120, 160, 131),
            hoverColour=(80, 114, 123),
            text="reszka"
        )

        self.reszka.hide()
        self.orzel.hide()

    def update(self):
        self.attack.draw()
        self.items.draw()
        self.defe.draw()
        self.enemyHp.draw()
        self.reszka.draw()
        self.orzel.draw()

  
    def attackCoin(self):
        self.doAttack = True
        self.attack.hide()
        self.items.hide()
        self.defe.hide()

        self.reszka.show()
        self.orzel.show()


