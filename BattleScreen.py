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

# Main Window Properties
playerChar = char
enemyChar = char
player_health_bar = ResourceBar
player_mana_bar = ResourceBar
enemy_health_bar = ResourceBar
enemy_mana_bar = ResourceBar
message_label = customtkinter.CTkLabel
message_frame = customtkinter.CTkFrame

def updateWindow(window, frame, name):
    global playerChar, enemyChar, player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar
    frame = window_manager.update_window(window, frame, "Battle")

    #Load character passed in
    all_characters = []
    if os.path.exists("Characters.json"):
        try:
            with open("Characters.json", "r") as file:
                all_characters = json.load(file)
        except json.JSONDecodeError:
            # Handle case where file exists but is empty or invalid
            all_characters = []

    for character in all_characters:
        if character.get("name") == name:
            playerChar = char(
                character.get("vitality"),
                character.get("strength"),
                character.get("defense"),
                character.get("dexterity"),
                character.get("name"),
                character.get("sprite_path")
                )
            
            enemySkillPoints = character.get("level") + 9

            enemyVitality = random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyVitality

            enemyStrength = random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyStrength

            enemyDefense = random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyDefense

            enemyDexterity = random.randrange(0, enemySkillPoints)
            enemySkillPoints -= enemyDexterity

            enemyChar = char(
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
        max_resource=playerChar.health
    )
    player_health_bar.pack(side=tk.TOP, padx=10)

    player_mana_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerChar.mana,
        static=True,
        color="#68C2F5"
    )
    player_mana_bar.pack(side=tk.TOP, padx=10)

    player_image = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[playerChar.sprite_index]),
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
        max_resource=enemyChar.health
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
        light_image=Image.open(sprite_paths[enemyChar.sprite_index]).transpose(Image.FLIP_LEFT_RIGHT),
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
            command=lambda: turnChange_thread(frame, controls_frame, enemyChar.takeDamage(damage=playerChar.normalAttack(), isCrit=playerChar.attackCrit), 
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
        functions = {}
        type_level = 0

        if(type == "vitality"):
            names = ["Leeching Strike", "Cure", "Full Heal"]
            functions = {'special1': playerChar.WarCry, 'special2': playerChar.WarCry, 'special3': playerChar.WarCry}
            type_level = playerChar.vitality
        elif(type == "strength"):
            names = ["War Cry", "Focus Punch", "Magic Burst"]
            functions = {'special1': playerChar.WarCry, 'special2': playerChar.WindUpStart, 'special3': lambda: enemyChar.takeDamage(damage=playerChar.MagicBurst(), isCrit=False)}
            type_level = playerChar.strength
        elif(type == "defense"):
            names = ["Shield Bash", "Impair", "Impervious"]
            functions = {'special1': playerChar.WarCry, 'special2': playerChar.WarCry, 'special3': playerChar.WarCry}
            type_level = playerChar.defense
        elif(type == "dexterity"):
            names = ["Laceration", "Cheap Shot", "2Fast 2Furious"]
            functions = {'special1': playerChar.WarCry, 'special2': playerChar.WarCry, 'special3': playerChar.WarCry}
            type_level = playerChar.dexterity

        button_valid = []

        if type_level < 3:
            button_valid = ["disabled", "disabled", "disabled"]
        elif type_level < 6:
            button_valid = ["normal", "disabled", "disabled"]
        elif type_level < 10:
            button_valid = ["normal", "normal", "disabled"]
        else:
            button_valid = ["normal", "normal", "normal"]

        if playerChar.mana < CharValues.special1Cost:
            button_valid = ["disabled", "disabled", "disabled"]
        elif playerChar.mana < CharValues.special2Cost:
            button_valid = ["normal", "disabled", "disabled"]
        elif playerChar.mana < CharValues.special3Cost:
            button_valid = ["normal", "normal", "disabled"]
        elif playerChar.mana >= CharValues.special3Cost:
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

        player_health.set_resource(playerChar.health)
        player_mana.set_resource(playerChar.mana)
        enemy_health.set_resource(enemyChar.health)
        enemy_mana.set_resource(enemyChar.mana)

    def turnChange_thread(frame, frame_to_destroy, message, player_health, player_mana, enemy_health, enemy_mana, queue):
        global message_label, message_frame
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

        threading.Thread(target=turnChange, args=(frame, player_health, player_mana, enemy_health, enemy_mana, queue)).start()

    def turnChange(frame, player_health, player_mana, enemy_health, enemy_mana, queue):
        global playerChar, enemyChar

        updateValues(player_health, player_mana, enemy_health, enemy_mana)

        playerChar.turnUpdate()

        time.sleep(2)

        if enemyChar.health <= 0:
            queue.put("You win!")

            time.sleep(2)

            window_manager.navigate_to(window, frame, "main")

        else:
            queue.put(playerChar.takeDamage(damage=enemyChar.normalAttack(), isCrit=enemyChar.attackCrit))

            updateValues(player_health, player_mana, enemy_health, enemy_mana)

            enemyChar.turnUpdate()

            time.sleep(2)

            if playerChar.health <= 0:
                queue.put("You lose!")

                time.sleep(2)

                window_manager.navigate_to(window, frame, "main")

            else:
                playerChar.attackCrit = False
                enemyChar.attackCrit = False

                if(playerChar.windUp == True):
                    playerChar.windUpTurns -= 1
                    if(playerChar.windUpTurns > 0):
                        queue.put("focus continue")
                        return
                    else:
                        queue.put("focus end")
                        return
                queue.put("end turn")
    
    queue = Queue()

    def processQueue():
        global message_label, message_frame
        while not queue.empty():
            message = queue.get_nowait()
            match message:
                case "focus continue":
                    turnChange_thread(frame, message_frame, f"{name} is focusing!", 
                                        player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
                case "focus end":
                    turnChange_thread(frame, message_frame, enemyChar.takeDamage(damage=playerChar.WindUpEnd(), isCrit=False), 
                                        player_health_bar, player_mana_bar, enemy_health_bar, enemy_mana_bar, queue)
                case "end turn":
                    normal_controls(frame, message_frame)
                case _:
                    message_label.configure(text=message)
        window.after(100, processQueue)

    processQueue()