# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import json
import os
import random
from SpritesStore import sprite_paths
from PIL import Image
from ResourceBar import ResourceBar
from GameChar import char

# Main Window Properties
playerChar = char
enemyChar = char

def updateWindow(window, frame, name):
    global playerChar, enemyChar
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

    health_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerChar.health
    )
    health_bar.pack(side=tk.TOP, padx=10)

    mana_bar = ResourceBar(
        master=player_char_frame,
        width=200,
        height=20,
        max_resource=playerChar.mana,
        static=True,
        color="#68C2F5"
    )
    mana_bar.pack(side=tk.TOP, padx=10)

    player_image = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[playerChar.sprite_index]),
        size=(150, 300)
    )

    image_label = customtkinter.CTkLabel(player_char_frame, image=player_image, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    enemy_char_frame = Frame(char_frame, width=450, height=400)
    enemy_char_frame.propagate(0)
    enemy_char_frame.pack(side=tk.LEFT, expand=TRUE)

    health_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=enemyChar.health
    )
    health_bar.pack(side=tk.TOP, padx=10)

    mana_bar = ResourceBar(
        master=enemy_char_frame,
        width=200,
        height=20,
        max_resource=enemyChar.health,
        static=True,
        color="#68C2F5"
    )
    mana_bar.pack(side=tk.TOP, padx=10)

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
            fg_color="#90EE90"
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
        type_level = 0

        if(type == "vitality"):
            names = ["Leeching Strike", "Cure", "Full Heal"]
        elif(type == "strength"):
            names = ["Warcry", "Focus Punch", "Magic Burst"]
        elif(type == "defense"):
            names = ["Shield Bash", "Impair", "Impervious"]
        elif(type == "dexterity"):
            names = ["Laceration", "Cheap Shot", "2Fast 2Furious"]

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
            fg_color="#90EE90"
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
            fg_color="#90EE90"
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
            fg_color="#90EE90"
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