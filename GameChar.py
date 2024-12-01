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
                if debuff == "Laceration":
                    self.health -= CharValues.laceration
                turns -= 1
                self.debuffs.update({debuff: turns})
                if turns == 0:
                    self.removeDebuff(debuff)

    def removeBuff(self, name):
        del self.buffs[name]
        match name:
            case "Attack Up":
                self.strength -= CharValues.attackUp
    
    def removeDebuff(self, name):
        del self.debuffs[name]
        match name:
            case "Attack Down":
                self.strength += CharValues.attackDown
            case "Defense Down":
                self.defense += CharValues.defenseDown

    def normalAttack(self):
        if random.randrange(1, 100) <= 5:
            self.attackCrit = True
            return (self.strength + 10) * 2
        else:
            return self.strength + 10
    
    def WarCry(self):
        self.spendMana(CharValues.strengthCost[0])
        if "Attack Up" in self.buffs:
            AttackUp = {"Attack Up": self.buffs.get("Attack Up") + CharValues.attackUpTurns}
        else:
            AttackUp = {"Attack Up": CharValues.attackUpTurns}
            self.strength += CharValues.attackUp
        self.buffs.update(AttackUp)
        return f"{self.name} used War Cry! Attack buffed for {CharValues.attackUpTurns - 1} turns!"
    
    def WindUpStart(self):
        self.spendMana(CharValues.strengthCost[1])
        self.windUp = True
        self.windUpTurns = 1
        return f"{self.name} is focusing!"
    
    def WindUpEnd(self):
        self.windUp = False
        return self.strength + 50
    
    def MagicBurst(self):
        self.spendMana(CharValues.strengthCost[2])
        return self.strength + 80
    
    def LeechingStrike(self):
        self.spendMana(CharValues.vitalityCost[0])
        if self.health + CharValues.lifestealAmount >= (100 + (self.vitality * 10)):
            self.health = 100 + (self.vitality * 10)
        else:
            self.health += CharValues.lifestealAmount
        return f"{self.name} healed {CharValues.lifestealAmount}! "
    
    def Cure(self):
        self.spendMana(CharValues.vitalityCost[1])
        self.debuffs.clear()
        return f"{self.name} cleansed all debuffs!"
    
    def FullHeal(self):
        self.spendMana(CharValues.vitalityCost[2])
        self.health = 100 + (self.vitality * 10)
        return f"{self.name} has fully healed!"
    
    def ShieldBash(self, char):
        char.spendMana(CharValues.defenseCost[0])
        if "Defense Down" in self.debuffs:
            DefenseDown = {"Defense Down": self.debuffs.get("Defense Down") + CharValues.defenseDownTurns}
        else:
            DefenseDown = {"Defense Down": CharValues.defenseDownTurns}
            self.defense -= CharValues.defenseDown
        self.debuffs.update(DefenseDown)
        return f"{self.name} defense reduced for {CharValues.defenseDownTurns - 1} turns!"

    def Impair(self, char):
        char.spendMana(CharValues.defenseCost[1])
        if "Attack Down" in self.debuffs:
            AttackDown = {"Attack Down": self.debuffs.get("Attack Down") + CharValues.attackDownTurns}
        else:
            AttackDown = {"Attack Down": CharValues.attackDownTurns}
            self.strength -= CharValues.attackDown
        self.debuffs.update(AttackDown)
        return f"{self.name} attack reduced for {CharValues.attackDownTurns - 1} turns!"
    
    def Impervious(self, char):
        char.spendMana(CharValues.defenseCost[2])
        Stun = {"Stun": CharValues.imperviousStunTurns}
        self.debuffs.update(Stun)
        return f"{self.name} has been stunned for {CharValues.imperviousStunTurns - 1} turns!"
    
    def Laceration(self, char):
        char.spendMana(CharValues.dexterityCost[0])
        Laceration = {"Laceration": CharValues.lacerationTurns}
        self.debuffs.update(Laceration)
        return f"{self.name} has been inflicted with bleed for {CharValues.lacerationTurns - 1} turns!"
    
    def CheapShot(self, debuffAmount):
        self.spendMana(CharValues.dexterityCost[1])
        return (self.strength + CharValues.cheapShotBaseDamage) * (debuffAmount + 1)
        
    def DoubleTime(self):
        self.spendMana(CharValues.dexterityCost[2])
        DoubleTime = {"Double Time": (CharValues.doubleTime * 2) + 1}
        self.buffs.update(DoubleTime)
        return f"{self.name} has sped up and can now take 2 actions per turn!"

    def takeDamage(self, damage, isCrit):
        if damage - self.defense < 0:
            damage = 0
        else:
            damage = damage - self.defense
        self.health -= damage
        if isCrit:
            return f"Critical Hit! {self.name} took {damage} damage!"
        else:
            return f"{self.name} took {damage} damage!"
        
    def spendMana(self, mana):
        self.mana -= mana
        return ""

    def enemyInit(self, player):
        self.possibleMoves = []
        self.player = char

        if self.vitality >= 3:
            self.possibleMoves.append({"function":lambda: self.LeechingStrike() + player.takeDamage(damage=self.normalAttack(), isCrit=self.attackCrit),
                                       "cost": CharValues.vitalityCost[0],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.vitality >= 6:
            self.possibleMoves.append({"function": self.Cure,
                                       "cost": CharValues.vitalityCost[1],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.vitality >= 10:
            self.possibleMoves.append({"function": self.FullHeal,
                                       "cost": CharValues.vitalityCost[2],
                                       "dealsDamage": False,
                                       "message": ""})
            
        if self.strength >= 3:
            self.possibleMoves.append({"function": self.WarCry,
                                       "cost": CharValues.strengthCost[0],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.strength >= 6:
            self.possibleMoves.append({"function": self.WindUpStart,
                                       "cost": CharValues.strengthCost[1],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.strength >= 10:
            self.possibleMoves.append({"function": self.MagicBurst,
                                       "cost": CharValues.strengthCost[2],
                                       "dealsDamage": True,
                                       "message": f"{self.name} has expended all there magic! "})
            
        if self.defense >= 3:
            self.possibleMoves.append({"function":lambda: player.ShieldBash(char=self),
                                       "cost": CharValues.defenseCost[0],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.defense >= 6:
            self.possibleMoves.append({"function":lambda: player.Impair(char=self),
                                       "cost": CharValues.defenseCost[1],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.defense >= 10:
            self.possibleMoves.append({"function":lambda: player.Impervious(char=self),
                                       "cost": CharValues.defenseCost[2],
                                       "dealsDamage": False,
                                       "message": ""})
            
        if self.dexterity >= 3:
            self.possibleMoves.append({"function":lambda: player.Laceration(char=self),
                                       "cost": CharValues.dexterityCost[0],
                                       "dealsDamage": False,
                                       "message": ""})
        if self.dexterity >= 6:
            self.possibleMoves.append({"function":lambda: self.CheapShot(debuffAmount=len(player.debuffs)),
                                       "cost": CharValues.dexterityCost[1],
                                       "dealsDamage": True,
                                       "message": f"{self.name} uses {player.name}'s weaknesses against them! "})
        if self.dexterity >= 10:
            self.possibleMoves.append({"function": self.DoubleTime,
                                       "cost": CharValues.dexterityCost[2],
                                       "dealsDamage": False,
                                       "message": ""})

    def enemyTurn(self, player):
        if self.windUp == True:
            self.windUpTurns -= 1
            if(self.windUpTurns > 0):
                return f"{self.name} is focusing!"
            else:
                return f"{self.name} has launched a powerful attack! " + player.takeDamage(self.WindUpEnd(), isCrit=self.attackCrit)
        
        if random.randrange(0, 100) >= 50:
            move = random.randrange(len(self.possibleMoves))
            if self.possibleMoves[move].get("cost") > self.mana:
                return player.takeDamage(damage=self.normalAttack(), isCrit=self.attackCrit)
            else:
                if self.possibleMoves[move].get("dealsDamage") == False:
                    return self.possibleMoves[move].get("function")()
                else:
                    return self.possibleMoves[move].get("message") + player.takeDamage(damage=self.possibleMoves[move]["function"](), isCrit=self.attackCrit)
        else:
            return player.takeDamage(damage=self.normalAttack(), isCrit=self.attackCrit)