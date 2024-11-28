import CharValues

class char:

    def __init__(self, vitality, strength, defense, dexterity, name, sprite_index):
        self.health = 100 + (vitality * 10)
        self.strength = strength
        self.defense = defense
        self.dexterity = dexterity
        self.name = name
        self.sprite_index = sprite_index
        self.mana = 100
        self.buffs = {}
        self.debuffs = {}

    def turnUpdate(self):
        if self.mana + 5 > 100:
            self.mana = 100
        else:
            self.mana += 5

        for buff, turns in self.buffs.items:
            if turns != 0:
                turns -= 1
                if turns == 0:
                    self.removeBuff(buff)
        for debuff, turns in self.debuffs.items:
            if turns != 0:
                turns -= 1
                if turns == 0:
                    self.removeBuff(debuff)

    def removeBuff(self, name):
        self.buffs.pop(name)
        match name:
            case "Attack Up":
                self.strength -= CharValues.attackUpIncrease
    
    def removeDebuff(self, name):
        return 0

    def normalAttack(self):
        return self.strength + 10
    
    def WarCry(self):
        updatedAttackUp = {"Attack Up": self.buffs.get("Attack Up") + 2}
        self.buffs.update(updatedAttackUp)
        self.strength += CharValues.attackUpIncrease
        self.mana -= CharValues.warCryCost

    def takeDamage(self, damage):
        self.health -= (damage - self.defense)

