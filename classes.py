from random import randint

class player():
    def __init__(self) -> None:
        self.name =''
        self.hp = 100
        self.attack = 5

    
    def attackEnemy(self):
        print('attack')
        if randint(100) < 51:
            return self.attack
            print('attack udany')
        else:
            print('attack nie udany')


class enemy():
    def __init__(self, hp, attack) -> None:
        self.hp = hp
        self.attack = attack

    def getDmg(slef, dmg):
        self.hp -= dmg