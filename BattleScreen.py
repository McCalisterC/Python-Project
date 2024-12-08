# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import account
import random
import threading
import time
from SpritesStore import sprite_paths
from SpritesStore import enemy_sprite_path
from PIL import Image
from pygame import mixer
from ResourceBar import ResourceBar
from GameChar import char
import CharValues
from queue import Queue

message_label = customtkinter.CTkLabel
message_frame = customtkinter.CTkFrame

def updateWindow(window, frame, acc, playerCharacter):
    #Initializing variables
    playerGameChar = char
    enemyGameChar = char
    player_health_bar = ResourceBar
    player_mana_bar = ResourceBar
    enemy_health_bar = ResourceBar
    enemy_mana_bar = ResourceBar
    
    #Updating window title
    frame = window_manager.update_window(window, frame, "Battle")

    #Load character passed in
    playerGameChar = char(
        playerCharacter.vitality, 
        playerCharacter.strength, 
        playerCharacter.defense, 
        playerCharacter.dexterity, 
        playerCharacter.name, 
        playerCharacter.sprite_path, 
    )

    #Generate an enemy with stats equal to player level
    enemySkillPoints = playerCharacter.level + 9

    enemyVitality = random.randrange(0, enemySkillPoints)
    enemySkillPoints -= enemyVitality

    enemyStrength = random.randrange(0, enemySkillPoints)
    enemySkillPoints -= enemyStrength

    enemyDefense = random.randrange(0, enemySkillPoints)
    enemySkillPoints -= enemyDefense

    enemyDexterity = enemySkillPoints

    enemyGameChar = char(
        enemyVitality,
        enemyStrength,
        enemyDefense,
        enemyDexterity,
        "Enemy",
        0
    )

    #Create frame for each characters details and sprites
    char_frame = Frame(frame, width=1280, height=450)
    char_frame.propagate(0)
    char_frame.pack(side=tk.TOP, expand=TRUE)

    #Create player characters frame
    player_char_frame = Frame(char_frame, width=600, height=400)
    player_char_frame.propagate(0)
    player_char_frame.pack(side=tk.LEFT, expand=TRUE)

    #Create player characters health bar and pack into player character frame
    player_health_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerGameChar.health
    )
    player_health_bar.pack(side=tk.TOP, padx=10)

    #Create player characters mana bar and pack into player character frame
    player_mana_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerGameChar.mana,
        static=True,
        color="#68C2F5"
    )
    player_mana_bar.pack(side=tk.TOP, padx=10)

    #Create a CTK Image and use player's image path for sprite
    player_image = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[playerGameChar.sprite_index]),
        size=(150, 300)
    )

    #Place image in label to pack into player character frame
    image_label = customtkinter.CTkLabel(player_char_frame, image=player_image, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    #Create enemy characters frame
    enemy_char_frame = Frame(char_frame, width=450, height=400)
    enemy_char_frame.propagate(0)
    enemy_char_frame.pack(side=tk.LEFT, expand=TRUE)

    #Create enemy characters health bar and pack into player character frame
    enemy_health_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=enemyGameChar.health
    )
    enemy_health_bar.pack(side=tk.TOP, padx=10)

    #Create enemy characters mana bar and pack into player character frame
    enemy_mana_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=100,
        static=True,
        color="#68C2F5"
    )
    enemy_mana_bar.pack(side=tk.TOP, padx=10)

    #Create a CTK Image and use enemy's image path for sprite
    enemy_image = customtkinter.CTkImage(
        light_image=Image.open(enemy_sprite_path),
        size=(150, 300)
    )

    #Place image in label to pack into enemy character frame
    image_label = customtkinter.CTkLabel(enemy_char_frame, image=enemy_image, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    #Function that updates the controls frame to normal controls
    def normal_controls(frame, frame_to_destroy):
        #Destroy passed in frame
        frame_to_destroy.destroy()

        #Replace with blank frame
        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

        #Create button for normal attack
        normal_attack_button = customtkinter.CTkButton(
            master=controls_frame,
            text="Normal Attack",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=150,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            command=lambda: turnChange_thread(frame, controls_frame, enemyGameChar.takeDamage(damage=playerGameChar.normalAttack(), isCrit=playerGameChar.attackCrit), 
                                       player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
        )
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        #Create button for special attack
        speical_attack_button = customtkinter.CTkButton(
            master=controls_frame,
            text="Special Attacks",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#0F52BA",
            height=150,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#68C2F5",
            command=lambda: special_attacks_select_controls(frame, controls_frame)
        )
        speical_attack_button.pack(side=tk.LEFT, expand=TRUE)

    #Call normal controls function with blank frame to destroy
    normal_controls(frame, Frame(frame))

    #Function that updates control frame with special attack selects
    def special_attacks_select_controls(frame, frame_to_destroy):
        #Destory passed in frame
        frame_to_destroy.destroy()

        #Replace with blank frame
        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

        #Create frame for top row of buttons
        top_row_frame = Frame(controls_frame, width=1280, height=100)
        top_row_frame.propagate(0)
        top_row_frame.pack(side=tk.TOP, expand=TRUE)

        #Create vitality attack select button
        vitality_attack_button = customtkinter.CTkButton(
            master=top_row_frame,
            text="Vitality Moves",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            command=lambda: special_attacks_controls(frame, controls_frame, "vitality")
        )
        vitality_attack_button.pack(side=tk.LEFT, expand=TRUE)

        #Create strength attack select button
        strength_attack_button = customtkinter.CTkButton(
            master=top_row_frame,
            text="Strength Moves",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            command=lambda: special_attacks_controls(frame, controls_frame, "strength")
        )
        strength_attack_button.pack(side=tk.LEFT, expand=TRUE)

        #Create frame for buttom row buttons
        bottom_row_frame = Frame(controls_frame, width=1280, height=100)
        bottom_row_frame.propagate(0)
        bottom_row_frame.pack(side=tk.TOP, expand=TRUE)

        #Create defense attack select button
        defense_attack_button = customtkinter.CTkButton(
            master=bottom_row_frame,
            text="Defense Moves",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            command=lambda: special_attacks_controls(frame, controls_frame, "defense")
        )
        defense_attack_button.pack(side=tk.LEFT, expand=TRUE)

        #Create dexterity attack select button
        dexterity_attack_button = customtkinter.CTkButton(
            master=bottom_row_frame,
            text="Dexterity Moves",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            command=lambda: special_attacks_controls(frame, controls_frame, "dexterity")
        )
        dexterity_attack_button.pack(side=tk.LEFT, expand=TRUE)

        #Create frame for back button row
        back_button_row_frame = Frame(controls_frame, width=1280, height=30)
        back_button_row_frame.propagate(0)
        back_button_row_frame.pack(side=tk.TOP, expand=TRUE)

        #Create back button to return to normal controls
        back_button = customtkinter.CTkButton(
            master=back_button_row_frame,
            text="Back",
            font=("undefined", 20, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#9a1d1d",
            height=20,
            width=100,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#FF0000",
            command=lambda: normal_controls(frame, controls_frame)
        )
        back_button.pack(side=tk.RIGHT, expand=TRUE)

    #Function that updates control frame with special attacks depending on attack type selected
    def special_attacks_controls(frame, frame_to_destroy, type):
        #Initialize variables
        names = []
        cost = []
        functions = {}
        type_level = 0

        #Check which type of attack was passed in and set the previous variables values depending on type
        if(type == "vitality"):
            names = ["Leeching Strike", "Cure", "Full Heal"]
            cost = CharValues.vitalityCost
            functions = {'special1':lambda: playerGameChar.LeechingStrike() + enemyGameChar.takeDamage(damage=playerGameChar.normalAttack(), isCrit=playerGameChar.attackCrit), 'special2': playerGameChar.Cure, 'special3': playerGameChar.FullHeal}
            type_level = playerGameChar.vitality
        elif(type == "strength"):
            names = ["War Cry", "Focus Punch", "Magic Burst"]
            cost = CharValues.strengthCost
            functions = {'special1': playerGameChar.WarCry, 'special2': playerGameChar.WindUpStart, 'special3': lambda: f"{playerGameChar.name} has expended all there magic! " + enemyGameChar.takeDamage(damage=playerGameChar.MagicBurst(), isCrit=False)}
            type_level = playerGameChar.strength
        elif(type == "defense"):
            names = ["Shield Bash", "Impair", "Impervious"]
            cost = CharValues.defenseCost
            functions = {'special1':lambda: enemyGameChar.ShieldBash(char=playerGameChar), 'special2':lambda: enemyGameChar.Impair(char=playerGameChar), 'special3':lambda: enemyGameChar.Impervious(char=playerGameChar)}
            type_level = playerGameChar.defense
        elif(type == "dexterity"):
            names = ["Laceration", "Cheap Shot", "2Fast 2Furious"]
            cost = CharValues.dexterityCost
            functions = {'special1':lambda: enemyGameChar.Laceration(char=playerGameChar), 'special2':lambda: f"{playerGameChar.name} uses {enemyGameChar.name}'s weaknesses against them! " + enemyGameChar.takeDamage(damage=playerGameChar.CheapShot(debuffAmount=len(enemyGameChar.debuffs)), isCrit=False), 'special3': playerGameChar.DoubleTime}
            type_level = playerGameChar.dexterity

        #Initialize which buttons are valid to an empty array
        button_valid = []

        #Check player's type level and current mana to determine which attacks are valid
        if type_level < 3:
            button_valid = ["disabled", "disabled", "disabled"]
        elif type_level < 6:
            if playerGameChar.mana < cost[0]:
                button_valid = ["disabled", "disabled", "disabled"]
            else:
                button_valid = ["normal", "disabled", "disabled"]
        elif type_level < 10:
            if playerGameChar.mana < cost[0]:
                button_valid = ["disabled", "disabled", "disabled"]
            elif playerGameChar.mana < cost[1]:
                button_valid = ["normal", "disabled", "disabled"]
            else:
                button_valid = ["normal", "normal", "disabled"]
        else:
            if playerGameChar.mana < cost[0]:
                button_valid = ["disabled", "disabled", "disabled"]
            elif playerGameChar.mana < cost[1]:
                button_valid = ["normal", "disabled", "disabled"]
            elif playerGameChar.mana < cost[2]:
                button_valid = ["normal", "normal", "disabled"]
            else:
                button_valid = ["normal", "normal", "normal"]

        #Destroy passed in frame
        frame_to_destroy.destroy()

        #Replace with blank frame
        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

        #Create frame for the top row of buttons
        top_row_frame = Frame(controls_frame, width=1280, height=100)
        top_row_frame.propagate(0)
        top_row_frame.pack(side=tk.TOP, expand=TRUE)

        #Create button for first special
        special1_button = customtkinter.CTkButton(
            master=top_row_frame,
            text=names[0],
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            state=button_valid[0],
            command=lambda: turnChange_thread(frame, controls_frame, functions["special1"](), 
                                       player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
        )
        special1_button.pack(side=tk.LEFT, expand=TRUE)

        #Create button for second special
        special2_button = customtkinter.CTkButton(
            master=top_row_frame,
            text=names[1],
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            state=button_valid[1],
            command=lambda: turnChange_thread(frame, controls_frame, functions["special2"](), 
                                       player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
        )
        special2_button.pack(side=tk.LEFT, expand=TRUE)

        #Create frame for the bottom row of buttons
        bottom_row_frame = Frame(controls_frame, width=1280, height=100)
        bottom_row_frame.propagate(0)
        bottom_row_frame.pack(side=tk.TOP, expand=TRUE)

        #Create button for third special
        special3_button = customtkinter.CTkButton(
            master=bottom_row_frame,
            text=names[2],
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#32CD32",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#90EE90",
            state=button_valid[2],
            command=lambda: turnChange_thread(frame, controls_frame, functions["special3"](), 
                                       player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
        )
        special3_button.pack(side=tk.LEFT, expand=TRUE)

        #Create button to return to special attack select controls
        back_button = customtkinter.CTkButton(
            master=bottom_row_frame,
            text="Back",
            font=("undefined", 40, 'bold'),
            text_color="#FFFFFF",
            hover=True,
            hover_color="#9a1d1d",
            height=75,
            width=400,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#FF0000",
            command=lambda: special_attacks_select_controls(frame, controls_frame)
        )
        back_button.pack(side=tk.LEFT, expand=TRUE)

    #Function that updates the values of the resource bars for each character
    def updateValues(player_health, player_mana, enemy_health, enemy_mana):
        player_health.set_resource(playerGameChar.health)
        player_mana.set_resource(playerGameChar.mana)
        enemy_health.set_resource(enemyGameChar.health)
        enemy_mana.set_resource(enemyGameChar.mana)

    #Function that starts a thread for turn changing
    def turnChange_thread(frame, frame_to_destroy, message, player_health, player_mana, enemy_health, enemy_mana, queue):
        #Get message frame and label
        global message_frame, message_label

        #Destroy passed in frame
        frame_to_destroy.destroy()

        #Replace with blank frame
        message_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        message_frame.propagate(0)
        message_frame.pack(side=tk.TOP, expand=TRUE)

        #Set message to new label with passed in message
        message_label = customtkinter.CTkLabel(
            master=message_frame,
            text=message,
            font=("Arial", 40),
            text_color="#000000",
            compound="center",
            anchor="center"
        )
        message_label.pack(side=tk.TOP, expand=TRUE)

        #Create a thread for the rest of the turnChange and start it
        threading.Thread(target=turnChange, args=(player_health, player_mana, enemy_health, enemy_mana, queue)).start()

    #Function to handle turn change using threading
    def turnChange(player_health, player_mana, enemy_health, enemy_mana, queue):
        updateValues(player_health, player_mana, enemy_health, enemy_mana)

        #Sleep to give player time to read message
        time.sleep(2)

        #Check if the enmey has been defeated and trigger player win event if true
        if enemyGameChar.health <= 0:
            queue.put("Player Wins")

        #Else initiate the enemy's turn
        else:
            #Update char using turnUpdate
            enemyGameChar.turnUpdate()

            #Check if the player has the "Double Time" buff and give them another turn if true and they haven't already taken a second turn
            if "Double Time" in playerGameChar.buffs:
                if playerGameChar.buffs.get("Double Time") % 2 == 0:
                    turns = playerGameChar.buffs.get("Double Time") - 1
                    playerGameChar.buffs.update({"Double Time": turns})
                    queue.put("end turn")
                    return
            
            #Check if the enemy has the "Stun" debuff and skip their turn if true
            if "Stun" in enemyGameChar.debuffs:
                queue.put(f"{enemyGameChar.name} is stunned!")
            #Check if the enemy has the "Laceration" debuff and trigger the bleed message if true before starting turn
            elif "Laceration" in enemyGameChar.debuffs:
                updateValues(player_health, player_mana, enemy_health, enemy_mana)

                queue.put(f"{enemyGameChar.name} takes {CharValues.laceration} bleed damage!")

                #Sleep to give player time to read message
                time.sleep(2)

                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))

                #Check if the enemy has the "Double Time" buff and give them another turn if true and they haven't already taken a second turn
                if "Double Time" in enemyGameChar.buffs:
                    if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                        #Sleep to give player time to read message
                        time.sleep(2)

                        turns = enemyGameChar.buffs.get("Double Time") - 1
                        enemyGameChar.buffs.update({"Double Time": turns})
                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
            #Else start enemy turn
            else:
                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))

                #Check if the enemy has the "Double Time" buff and give them another turn if true and they haven't already taken a second turn
                if "Double Time" in enemyGameChar.buffs:
                    if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                        #Sleep to give player time to read message
                        time.sleep(2)

                        turns = enemyGameChar.buffs.get("Double Time") - 1
                        enemyGameChar.buffs.update({"Double Time": turns})
                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))

            updateValues(player_health, player_mana, enemy_health, enemy_mana)

            #Sleep to give player time to read message
            time.sleep(2)

            #Check if player has been defeated and trigger player lost event if true
            if playerGameChar.health <= 0:
                queue.put("Player Lost")

            #Else reset each character and trigger start of next turn effects if needed before changing turns
            else:
                playerGameChar.attackCrit = False
                enemyGameChar.attackCrit = False
                playerGameChar.turnUpdate()

                #Check if player is winding up and trigger an event depending on which phase of wind up they are at
                if(playerGameChar.windUp == True):
                    playerGameChar.windUpTurns -= 1
                    if(playerGameChar.windUpTurns > 0):
                        queue.put("focus continue")
                        return
                    else:
                        queue.put("focus end")
                        return
                    
                #Check if the player is stunned and start the enemy's turn if true
                if "Stun" in playerGameChar.debuffs:
                    while "Stun" in playerGameChar.debuffs:
                        queue.put(f"{playerGameChar.name} is stunned!")
                        playerGameChar.turnUpdate()

                        #Sleep to give player time to read message
                        time.sleep(2)

                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))

                        #Check if the enemy has the "Double Time" buff and give them another turn if true and they haven't already taken a second turn
                        if "Double Time" in enemyGameChar.buffs:
                            if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                                #Sleep to give player time to read message
                                time.sleep(2)

                                turns = enemyGameChar.buffs.get("Double Time") - 1
                                enemyGameChar.buffs.update({"Double Time": turns})
                                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
                                enemyGameChar.turnUpdate()

                        updateValues(player_health, player_mana, enemy_health, enemy_mana)

                        #Sleep to give player time to read message
                        time.sleep(2)

                        #Check if player has been defeated and trigger player lost event if true
                        if playerGameChar.health <= 0:
                            queue.put("Player Lost")
                            return
                
                #Check if player has the "Laceration" debuff and trigger bleed message if true
                elif "Laceration" in playerGameChar.debuffs:
                    updateValues(player_health, player_mana, enemy_health, enemy_mana)

                    queue.put(f"{playerGameChar.name} takes {CharValues.laceration} bleed damage!")

                    #Sleep to give player time to read message
                    time.sleep(2)

                #Trigger end turn event
                queue.put("end turn")
                return
    
    #Create queue for processing events
    queue = Queue()

    #Function that recursively checks the queue every 0.1 seconds and triggers events that are in the queue
    def processQueue():
        #Get message frame and label
        global message_frame, message_label

        #While the queue is not empty, trigger events in the queue
        while not queue.empty():
            #Get message from queue
            message = queue.get_nowait()

            #Check if message matches event trigger
            match message:
                case "focus continue":
                    turnChange_thread(frame, message_frame, f"{playerGameChar.name} is focusing!", 
                                        player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
                case "focus end":
                    turnChange_thread(frame, message_frame, f"{playerGameChar.name} has launched a powerful attack! " + enemyGameChar.takeDamage(damage=playerGameChar.WindUpEnd(), isCrit=False), 
                                        player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
                case "end turn":
                    normal_controls(frame, message_frame)
                case "Player Wins":
                    handleWin()
                    EndGameScreen(window, f"You Win!", True)
                case "Player Lost":
                    EndGameScreen(window, f"You Lost!", False)
                case _:
                    message_label.configure(text=message)
        
        #Call process after 100 miliseconds
        window.after(100, processQueue)

    #Function to handle the player win event
    def handleWin():
        with account.SessionFactory() as session:
            character = session.query(account.Character).filter_by(id=playerCharacter.id).first()
            if character:
                character.xp += 10
                character.defeated_enemies += 1
                if (character.xp >= character.level * 40):
                    character.level += 1
                session.commit()

    #Function that shows the end game screen with messages depending on if the player won or not
    def EndGameScreen(window, message, playerWin):
        #Stop music
        mixer.music.stop()

        updatedCharacter = None
        
        #Pull character from database for most up to date data
        with account.SessionFactory() as session:
            character = session.query(account.Character).filter_by(id=playerCharacter.id).first()
            if character:
                updatedCharacter = character

        #Create new frame to place in middle of window
        end_game_frame = customtkinter.CTkFrame(
            master=window,
            width=1000,
            height=600
        )
        end_game_frame.propagate(0)
        end_game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        #Create label for the message
        end_game_message = customtkinter.CTkLabel(
            master=end_game_frame,
            text=message,
            font=("Arial", 30),
            text_color="#000000",
            height=30,
            width=200,
            corner_radius=0,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF",
            compound="center",
            anchor="center"
        )
        end_game_message.pack(side=tk.TOP, expand=True)

        #If the player wins, create and place necessary updated values
        if playerWin:
            xp_obtained_label = customtkinter.CTkLabel(
                master=end_game_frame,
                text="Gained XP: 10",
                font=("Arial", 30),
                text_color="#000000",
                height=30,
                width=200,
                corner_radius=0,
                bg_color="#FFFFFF",
                fg_color="#FFFFFF",
                compound="center",
                anchor="center"
            )
            xp_obtained_label.pack(side=tk.TOP, expand=True)

            current_xp_label = customtkinter.CTkLabel(
                master=end_game_frame,
                text=f"Current XP: {updatedCharacter.xp}",
                font=("Arial", 30),
                text_color="#000000",
                height=30,
                width=200,
                corner_radius=0,
                bg_color="#FFFFFF",
                fg_color="#FFFFFF",
                compound="center",
                anchor="center"
            )
            current_xp_label.pack(side=tk.TOP, expand=True)

            xp_progression_frame = customtkinter.CTkFrame(
                master=end_game_frame,
                width=500,
                height=100
            )
            xp_progression_frame.pack(side=tk.TOP, expand=True)

            xp_progression_label = customtkinter.CTkLabel(
                master=xp_progression_frame,
                text="XP Progression To Next Level: ",
                font=("Arial", 30),
                text_color="#000000",
                height=50,
                width=200,
                corner_radius=0,
                bg_color="#FFFFFF",
                fg_color="#FFFFFF",
                compound="center",
                anchor="center"
            )
            xp_progression_label.pack(side=tk.LEFT, expand=True)

            xp_progression_bar = ResourceBar(
                master=xp_progression_frame,
                width=200,
                height=50,
                max_resource=40,
                current_resource=updatedCharacter.xp - ((updatedCharacter.level - 1) * 40),
                static=True,
                color="#68C2F5"
            )
            xp_progression_bar.pack(side=tk.TOP, padx=10)

        #Create a frame for the buttons
        button_frame = customtkinter.CTkFrame(
            master=end_game_frame,
            width=500,
            height=50
        )
        button_frame.propagate(0)
        button_frame.pack(side=tk.TOP, expand=True)

        #Create a button to play again
        play_again_button = customtkinter.CTkButton(
            master=button_frame,
            text="Play Again",
            font=("undefined", 16),
            text_color="#000000",
            hover=True,
            hover_color="#188124",
            height=30,
            width=150,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#00ff55",
            command=lambda: window_manager.navigate_to_battle(window, frame, acc, updatedCharacter)
        )
        play_again_button.pack(side=tk.LEFT, expand=True)

        #Create a button to edit the character
        edit_char_button = customtkinter.CTkButton(
            master=button_frame,
            text="Edit Character",
            font=("undefined", 16),
            text_color="#000000",
            hover=True,
            hover_color="#0F52BA",
            height=30,
            width=150,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#68C2F5",
            command=lambda: window_manager.navigate_to_character_edit(window, frame, acc, updatedCharacter)
        )
        edit_char_button.pack(side=tk.LEFT, expand=True)

        #Create a button to exit back to main menu
        exit_button = customtkinter.CTkButton(
            master=button_frame,
            text="Return to Main Menu",
            font=("undefined", 16),
            text_color="#000000",
            hover=True,
            hover_color="#9a1d1d",
            height=30,
            width=150,
            border_width=2,
            corner_radius=6,
            border_color="#000000",
            bg_color="#FFFFFF",
            fg_color="#ff0000",
            command=lambda: window_manager.navigate_to(window, frame, acc, "main")
            )
        exit_button.pack(side=tk.LEFT, expand=True)

    #Call processQueue function and initalize the enemy character
    processQueue()
    enemyGameChar.enemyInit(player=playerGameChar)

    #Start battle music
    mixer.init()
    mixer.music.load("assets/sounds/Pythonbattle.wav")
    mixer.music.play(loops=-1)