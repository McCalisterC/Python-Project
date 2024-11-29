import CharValues
import random

class char:

    def __init__(self, vitality, strength, defense, dexterity, name, sprite_index):
        self.health = 100 + (vitality * 10)
        self.vitality = vitality
        self.strength = strength
        self.defense = defense
        self.dexterity = dexterity
        self.name = name
        self.sprite_index = sprite_index
        self.mana = 100
        self.attackCrit = False
        self.windUp = False
        self.windUpTurns = 0
        self.buffs = {}
        self.debuffs = {}

    def turnUpdate(self):
        if self.mana + 5 > 100:
            self.mana = 100
        else:
            self.mana += 5

        for buff, turns in list(self.buffs.items()):
            print(f"{buff} has {turns} left")
            if turns != 0:
                turns -= 1
                self.buffs.update({buff: turns})
                if turns == 0:
                    self.removeBuff(buff)
        for debuff, turns in list(self.debuffs.items()):
            if turns != 0:
                turns -= 1
                if turns == 0:
                    self.removeBuff(debuff)

    def removeBuff(self, name):
        del self.buffs[name]
        match name:
            case "Attack Up":
                self.strength -= CharValues.attackUpIncrease
    
    def removeDebuff(self, name):
        return 0

    def normalAttack(self):
        print(f"{self.name} has {self.mana}")
        if random.randrange(1, 100) <= 5:
            self.attackCrit = True
            return (self.strength + 10) * 2
        else:
            return self.strength + 10
    
    def WarCry(self):
        updatedAttackUp = {"Attack Up": 3}
        self.buffs.update(updatedAttackUp)
        self.strength += CharValues.attackUpIncrease
        self.mana -= CharValues.special1Cost
        return f"{self.name} used War Cry! Attack buffed for 2 turns!"
    
    def WindUpStart(self):
        self.windUp = True
        self.windUpTurns = 1
        self.mana -= CharValues.special2Cost
        return f"{self.name} is focusing!"
    
    def WindUpEnd(self):
        self.windUp = False
        return self.strength + 50
    
    def MagicBurst(self):
        self.mana -= 100
        return self.strength + 80

    def takeDamage(self, damage, isCrit):
        damage = damage - self.defense
        self.health -= damage
        if isCrit:
            return f"Critical Hit! {self.name} took {damage} damage!"
        else:
            return f"{self.name} took {damage} damage!"

