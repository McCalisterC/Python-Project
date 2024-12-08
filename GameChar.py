import CharValues
import random

class char:

    #Class init function
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

    #Function that updates the character per turn
    def turnUpdate(self):
        #Regenerate mana up to max amount (100)
        if self.mana + 5 > 100:
            self.mana = 100
        else:
            self.mana += 5

        #Update every buff in the buff dictionary
        for buff, turns in list(self.buffs.items()):
            print(f"{buff} has {turns} left")
            if turns != 0:
                turns -= 1
                self.buffs.update({buff: turns})
                if turns == 0:
                    self.removeBuff(buff)
        #Update every debuff in the debuff dictionary
        for debuff, turns in list(self.debuffs.items()):
            if turns != 0:
                if debuff == "Laceration":
                    self.health -= CharValues.laceration
                turns -= 1
                self.debuffs.update({debuff: turns})
                if turns == 0:
                    self.removeDebuff(debuff)

    #Function to remove buffs and reset values depending on buff
    def removeBuff(self, name):
        del self.buffs[name]
        match name:
            case "Attack Up":
                self.strength -= CharValues.attackUp
    
    #Function to remove debuffs and reset values depeing on debuff
    def removeDebuff(self, name):
        del self.debuffs[name]
        match name:
            case "Attack Down":
                self.strength += CharValues.attackDown
            case "Defense Down":
                self.defense += CharValues.defenseDown

    #Function for normal attacks
    def normalAttack(self):
        if random.randrange(1, 100) <= 5:
            self.attackCrit = True
            return (self.strength + 10) * 2
        else:
            return self.strength + 10
    
    #Function for War Cry special that increases character attack
    def WarCry(self):
        self.spendMana(CharValues.strengthCost[0])
        if "Attack Up" in self.buffs:
            AttackUp = {"Attack Up": self.buffs.get("Attack Up") + CharValues.attackUpTurns}
        else:
            AttackUp = {"Attack Up": CharValues.attackUpTurns}
            self.strength += CharValues.attackUp
        self.buffs.update(AttackUp)
        return f"{self.name} used War Cry! Attack buffed for {CharValues.attackUpTurns - 1} turns!"
    
    #Function for Wind Up special that starts the process
    def WindUpStart(self):
        self.spendMana(CharValues.strengthCost[1])
        self.windUp = True
        self.windUpTurns = 1
        return f"{self.name} is focusing!"
    
    #Function for Wind Up special that ends the process
    def WindUpEnd(self):
        self.windUp = False
        return self.strength + 50
    
    #Function for Magic Burst special that spends a large amount of mana to due a large amount of damage
    def MagicBurst(self):
        self.spendMana(CharValues.strengthCost[2])
        return self.strength + 80
    
    #Function for Leeching Strike special that deals damage and heals the character
    def LeechingStrike(self):
        self.spendMana(CharValues.vitalityCost[0])
        if self.health + CharValues.lifestealAmount >= (100 + (self.vitality * 10)):
            self.health = 100 + (self.vitality * 10)
        else:
            self.health += CharValues.lifestealAmount
        return f"{self.name} healed {CharValues.lifestealAmount}! "
    
    #Function for Cure special that cleanses all debuffs
    def Cure(self):
        self.spendMana(CharValues.vitalityCost[1])
        self.debuffs.clear()
        return f"{self.name} cleansed all debuffs!"
    
    #Function for Full Heal special that heals the character to full health
    def FullHeal(self):
        self.spendMana(CharValues.vitalityCost[2])
        self.health = 100 + (self.vitality * 10)
        return f"{self.name} has fully healed!"
    
    #Function for Shield Bash special that inflicts the opposing character with the defense down debuff
    def ShieldBash(self, char):
        char.spendMana(CharValues.defenseCost[0])
        if "Defense Down" in self.debuffs:
            DefenseDown = {"Defense Down": self.debuffs.get("Defense Down") + CharValues.defenseDownTurns}
        else:
            DefenseDown = {"Defense Down": CharValues.defenseDownTurns}
            self.defense -= CharValues.defenseDown
        self.debuffs.update(DefenseDown)
        return f"{self.name} defense reduced for {CharValues.defenseDownTurns - 1} turns!"

    #Function for Impair special that inflicts the opposing character with the attack down debuff
    def Impair(self, char):
        char.spendMana(CharValues.defenseCost[1])
        if "Attack Down" in self.debuffs:
            AttackDown = {"Attack Down": self.debuffs.get("Attack Down") + CharValues.attackDownTurns}
        else:
            AttackDown = {"Attack Down": CharValues.attackDownTurns}
            self.strength -= CharValues.attackDown
        self.debuffs.update(AttackDown)
        return f"{self.name} attack reduced for {CharValues.attackDownTurns - 1} turns!"
    
    #Function for Impervious that inflicts the opposing character with the stun debuff
    def Impervious(self, char):
        char.spendMana(CharValues.defenseCost[2])
        Stun = {"Stun": CharValues.imperviousStunTurns}
        self.debuffs.update(Stun)
        return f"{self.name} has been stunned for {CharValues.imperviousStunTurns - 1} turns!"
    
    #Function for Laceration that inflicts the opposing character with the Laceration debuff
    def Laceration(self, char):
        char.spendMana(CharValues.dexterityCost[0])
        Laceration = {"Laceration": CharValues.lacerationTurns}
        self.debuffs.update(Laceration)
        return f"{self.name} has been inflicted with bleed for {CharValues.lacerationTurns - 1} turns!"
    
    #Function for Cheap Shot special that deals a certain amount of damage that is increased with the amount of the opposing character's debuffs
    def CheapShot(self, debuffAmount):
        self.spendMana(CharValues.dexterityCost[1])
        return (self.strength + CharValues.cheapShotBaseDamage) * (debuffAmount + 1)
        
    #Function for Double Time special that grants the character the Double Time buff
    def DoubleTime(self):
        self.spendMana(CharValues.dexterityCost[2])
        DoubleTime = {"Double Time": (CharValues.doubleTime * 2) + 1}
        self.buffs.update(DoubleTime)
        return f"{self.name} has sped up and can now take 2 actions per turn!"

    #Function for taking damage
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
        
    #Function for spending mana
    def spendMana(self, mana):
        self.mana -= mana
        return ""

    #Function for initializing the enemy character and figuring out which moves they can use
    def enemyInit(self, player):
        #Initalize variables
        self.possibleMoves = []
        self.player = char

        #If statements to check the enemy's stats and appends functions to the possible moves array if the enemy can use them
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

    #Function for handling the enemy's turn
    def enemyTurn(self, player):
        #Check if enemy is winding up and handle turn depending on which stage of the process the character is at
        if self.windUp == True:
            self.windUpTurns -= 1
            if(self.windUpTurns > 0):
                return f"{self.name} is focusing!"
            else:
                return f"{self.name} has launched a powerful attack! " + player.takeDamage(self.WindUpEnd(), isCrit=self.attackCrit)
        
        #Randomly chooses between performing a normal attack or special attack
        if random.randrange(0, 100) >= 50:
            move = random.randrange(len(self.possibleMoves))
            #Checks if player has the mana to do the move and performs a normal attack instead if not
            if self.possibleMoves[move].get("cost") > self.mana:
                return player.takeDamage(damage=self.normalAttack(), isCrit=self.attackCrit)
            else:
                if self.possibleMoves[move].get("dealsDamage") == False:
                    return self.possibleMoves[move].get("function")()
                else:
                    return self.possibleMoves[move].get("message") + player.takeDamage(damage=self.possibleMoves[move]["function"](), isCrit=self.attackCrit)
        else:
            return player.takeDamage(damage=self.normalAttack(), isCrit=self.attackCrit)