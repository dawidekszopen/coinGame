from random import randint

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