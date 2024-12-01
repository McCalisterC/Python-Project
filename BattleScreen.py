# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import json
import os
import random
import threading
import time
from SpritesStore import sprite_paths
from PIL import Image
from ResourceBar import ResourceBar
from GameChar import char
import CharValues
from queue import Queue

message_label = customtkinter.CTkLabel
message_frame = customtkinter.CTkFrame

def updateWindow(window, frame, name):
    playerGameChar = char
    enemyGameChar = char
    player_health_bar = ResourceBar
    player_mana_bar = ResourceBar
    enemy_health_bar = ResourceBar
    enemy_mana_bar = ResourceBar

    playerChar = {}
    all_characters = []

    frame = window_manager.update_window(window, frame, "Battle")

    #Load character passed in
    if os.path.exists("Characters.json"):
        try:
            with open("Characters.json", "r") as file:
                all_characters = json.load(file)
        except json.JSONDecodeError:
            # Handle case where file exists but is empty or invalid
            all_characters = []

    for character in all_characters:
        if character.get("name") == name:
            playerChar = character

            playerGameChar = char(
                character.get("vitality"),
                character.get("strength"),
                character.get("defense"),
                character.get("dexterity"),
                character.get("name"),
                character.get("sprite_path")
                )
            
            enemySkillPoints = character.get("level") + 9

            enemyVitality =  0 #random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyVitality

            enemyStrength = 0 #random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyStrength

            enemyDefense = 0 #random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyDefense

            enemyDexterity = 10 #enemySkillPoints

            enemyGameChar = char(
                enemyVitality,
                enemyStrength,
                enemyDefense,
                enemyDexterity,
                "Monster",
                random.randrange(0, len(sprite_paths) - 1)
            )

    char_frame = Frame(frame, width=1280, height=450)
    char_frame.propagate(0)
    char_frame.pack(side=tk.TOP, expand=TRUE)

    player_char_frame = Frame(char_frame, width=600, height=400)
    player_char_frame.propagate(0)
    player_char_frame.pack(side=tk.LEFT, expand=TRUE)

    player_health_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerGameChar.health
    )
    player_health_bar.pack(side=tk.TOP, padx=10)

    player_mana_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerGameChar.mana,
        static=True,
        color="#68C2F5"
    )
    player_mana_bar.pack(side=tk.TOP, padx=10)

    player_image = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[playerGameChar.sprite_index]),
        size=(150, 300)
    )

    image_label = customtkinter.CTkLabel(player_char_frame, image=player_image, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    enemy_char_frame = Frame(char_frame, width=450, height=400)
    enemy_char_frame.propagate(0)
    enemy_char_frame.pack(side=tk.LEFT, expand=TRUE)

    enemy_health_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=enemyGameChar.health
    )
    enemy_health_bar.pack(side=tk.TOP, padx=10)

    enemy_mana_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=100,
        static=True,
        color="#68C2F5"
    )
    enemy_mana_bar.pack(side=tk.TOP, padx=10)

    enemy_image = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[enemyGameChar.sprite_index]).transpose(Image.FLIP_LEFT_RIGHT),
        size=(150, 300)
    )

    image_label = customtkinter.CTkLabel(enemy_char_frame, image=enemy_image, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    def normal_controls(frame, frame_to_destroy):
        frame_to_destroy.destroy()

        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

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

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

    normal_controls(frame, Frame(frame))

    def special_attacks_select_controls(frame, frame_to_destroy):
        frame_to_destroy.destroy()

        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

        top_row_frame = Frame(controls_frame, width=1280, height=100)
        top_row_frame.propagate(0)
        top_row_frame.pack(side=tk.TOP, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        bottom_row_frame = Frame(controls_frame, width=1280, height=100)
        bottom_row_frame.propagate(0)
        bottom_row_frame.pack(side=tk.TOP, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        back_button_row_frame = Frame(controls_frame, width=1280, height=30)
        back_button_row_frame.propagate(0)
        back_button_row_frame.pack(side=tk.TOP, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.RIGHT, expand=TRUE)

    def special_attacks_controls(frame, frame_to_destroy, type):
        names = []
        cost = []
        functions = {}
        type_level = 0

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

        button_valid = []

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

        frame_to_destroy.destroy()

        controls_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        controls_frame.propagate(0)
        controls_frame.pack(side=tk.TOP, expand=TRUE)

        top_row_frame = Frame(controls_frame, width=1280, height=100)
        top_row_frame.propagate(0)
        top_row_frame.pack(side=tk.TOP, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        bottom_row_frame = Frame(controls_frame, width=1280, height=100)
        bottom_row_frame.propagate(0)
        bottom_row_frame.pack(side=tk.TOP, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

        normal_attack_button = customtkinter.CTkButton(
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
        normal_attack_button.pack(side=tk.LEFT, expand=TRUE)

    def updateValues(player_health, player_mana, enemy_health, enemy_mana):

        player_health.set_resource(playerGameChar.health)
        player_mana.set_resource(playerGameChar.mana)
        enemy_health.set_resource(enemyGameChar.health)
        enemy_mana.set_resource(enemyGameChar.mana)

    def turnChange_thread(frame, frame_to_destroy, message, player_health, player_mana, enemy_health, enemy_mana, queue):
        global message_frame, message_label
        frame_to_destroy.destroy()

        message_frame = Frame(frame, width=1280, height=300, background="#FFFFFF")
        message_frame.propagate(0)
        message_frame.pack(side=tk.TOP, expand=TRUE)

        message_label = customtkinter.CTkLabel(
            master=message_frame,
            text=message,
            font=("Arial", 40),
            text_color="#000000",
            compound="center",
            anchor="center"
        )
        message_label.pack(side=tk.TOP, expand=TRUE)

        threading.Thread(target=turnChange, args=(player_health, player_mana, enemy_health, enemy_mana, queue)).start()

    def turnChange(player_health, player_mana, enemy_health, enemy_mana, queue):
        updateValues(player_health, player_mana, enemy_health, enemy_mana)

        time.sleep(2)

        if enemyGameChar.health <= 0:
            queue.put("Player Wins")

        else:
            enemyGameChar.turnUpdate()

            if "Double Time" in playerGameChar.buffs:
                if playerGameChar.buffs.get("Double Time") % 2 == 0:
                    turns = playerGameChar.buffs.get("Double Time") - 1
                    playerGameChar.buffs.update({"Double Time": turns})
                    queue.put("end turn")
                    return
            
            if "Stun" in enemyGameChar.debuffs:
                queue.put(f"{enemyGameChar.name} is stunned!")
            elif "Laceration" in enemyGameChar.debuffs:
                updateValues(player_health, player_mana, enemy_health, enemy_mana)

                queue.put(f"{enemyGameChar.name} takes {CharValues.laceration} bleed damage!")
                time.sleep(2)
                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
                if "Double Time" in enemyGameChar.buffs:
                    if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                        time.sleep(2)
                        turns = enemyGameChar.buffs.get("Double Time") - 1
                        enemyGameChar.buffs.update({"Double Time": turns})
                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
            else:
                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
                if "Double Time" in enemyGameChar.buffs:
                    if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                        time.sleep(2)
                        turns = enemyGameChar.buffs.get("Double Time") - 1
                        enemyGameChar.buffs.update({"Double Time": turns})
                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))

            updateValues(player_health, player_mana, enemy_health, enemy_mana)

            time.sleep(2)

            if playerGameChar.health <= 0:
                queue.put("Player Lost")

            else:
                playerGameChar.attackCrit = False
                enemyGameChar.attackCrit = False
                playerGameChar.turnUpdate()

                if(playerGameChar.windUp == True):
                    playerGameChar.windUpTurns -= 1
                    if(playerGameChar.windUpTurns > 0):
                        queue.put("focus continue")
                        return
                    else:
                        queue.put("focus end")
                        return
                if "Stun" in playerGameChar.debuffs:
                    while "Stun" in playerGameChar.debuffs:
                        queue.put(f"{playerGameChar.name} is stunned!")
                        playerGameChar.turnUpdate()
                        time.sleep(2)
                        queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
                        if "Double Time" in enemyGameChar.buffs:
                            if enemyGameChar.buffs.get("Double Time") % 2 == 0:
                                time.sleep(2)
                                turns = enemyGameChar.buffs.get("Double Time") - 1
                                enemyGameChar.buffs.update({"Double Time": turns})
                                queue.put(enemyGameChar.enemyTurn(player=playerGameChar))
                                enemyGameChar.turnUpdate()
                        updateValues(player_health, player_mana, enemy_health, enemy_mana)
                        time.sleep(2)

                        if playerGameChar.health <= 0:
                            queue.put("Player Lost")
                            return
                elif "Laceration" in playerGameChar.debuffs:
                    updateValues(player_health, player_mana, enemy_health, enemy_mana)

                    queue.put(f"{playerGameChar.name} takes {CharValues.laceration} bleed damage!")
                    time.sleep(2)
                queue.put("end turn")
                return
    
    queue = Queue()

    def processQueue():
        global message_frame, message_label
        while not queue.empty():
            message = queue.get_nowait()
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
                    handleWin(playerChar, all_characters)
                    EndGameScreen(window, f"You Win!", playerChar, True)
                case "Player Lost":
                    EndGameScreen(window, f"You Lost!", playerChar, False)
                case _:
                    message_label.configure(text=message)
        window.after(100, processQueue)

    def handleWin(character, all_characters):
        for character in all_characters:
            if character.get("name") == name:
                character.update({"xp": character.get("xp") + 10})
                if character.get("xp") >= character.get("level") * 40:
                    character.update({"level": character.get("level") + 1})
                character.update({"defeated_enemies": character.get("defeated_enemies") + 1})
                break
        try:
            with open("Characters.json", "w") as file:
                json.dump(all_characters, file, indent=3)
        except Exception as e:
            return

    def EndGameScreen(window, message, character, playerWin):
        end_game_frame = customtkinter.CTkFrame(
            master=window,
            width=1000,
            height=600
        )
        end_game_frame.propagate(0)
        end_game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
                text=f"Current XP: {character.get('xp')}",
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
                current_resource=character.get("xp") - ((character.get("level") - 1) * 40),
                static=True,
                color="#68C2F5"
            )
            xp_progression_bar.pack(side=tk.TOP, padx=10)

        button_frame = customtkinter.CTkFrame(
            master=end_game_frame,
            width=500,
            height=50
        )
        button_frame.propagate(0)
        button_frame.pack(side=tk.TOP, expand=True)

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
            command=lambda: window_manager.navigate_to_battle(window, frame, name)
        )
        play_again_button.pack(side=tk.LEFT, expand=True)

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
            command=lambda: window_manager.navigate_to_character_edit(window, frame, name)
        )
        edit_char_button.pack(side=tk.LEFT, expand=True)

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
            command=lambda: window_manager.navigate_to(window, frame, "main")
            )
        exit_button.pack(side=tk.LEFT, expand=True)

    processQueue()
    enemyGameChar.enemyInit(player=playerGameChar)