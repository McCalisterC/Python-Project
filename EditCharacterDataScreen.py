# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import json
import os
from tkinter import messagebox
from PIL import Image
from SpritesStore import sprite_paths

skillPoints = 10
characterName = ""
characterVitality = 0
characterStrength = 0
characterDexterity = 0
characterDefense = 0
sprite_index = 0

# Main Window Properties
def updateWindow(window, frame, name):
    global skillPoints, characterVitality, characterStrength, characterDexterity, characterDefense, characterName, sprite_index
    
    # Update window using window_manager
    frame = window_manager.update_window(window, frame, "New Character")

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
            characterName = character.get("name")
            characterVitality = character.get("vitality")
            characterStrength = character.get("strength")
            characterDexterity = character.get("dexterity")
            characterDefense = character.get("defense")
            skillPoints = (9 + character.get("level")) - (characterVitality + characterDefense + characterStrength + characterDexterity)
            sprite_index = character.get("sprite_path")

    # Create title label
    title_label = customtkinter.CTkLabel(
    master=frame,
    text="Edit Your Character",
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
    title_label.pack(side=tk.TOP, expand=True)

    char_edit_frame = Frame(frame, width=1000, height=600)
    char_edit_frame.propagate(0)
    char_edit_frame.pack(side=tk.TOP, expand=TRUE)

    left_frame = Frame(char_edit_frame, width=400, height=600)
    left_frame.propagate(0)
    left_frame.pack(side=tk.LEFT, expand=TRUE)

    # Create skill points label
    skill_points_label = customtkinter.CTkLabel(
        master=left_frame,
        text=f"Skill Points: {skillPoints}",
        font=("Arial", 20),
        text_color="#000000",
        height=30,
        width=200,
        corner_radius=0,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
        compound="center",
        anchor="center"
    )
    skill_points_label.pack(side=tk.TOP, expand=True)

    # Function to handle slider changes
    def handle_stat_change(value, stat_type, label, slider):
        global skillPoints, characterVitality, characterStrength, characterDexterity, characterDefense
        value = round(value)
        
        # Get the current stat value based on stat_type
        current_value = 0
        if stat_type == "vitality":
            current_value = characterVitality
        elif stat_type == "strength":
            current_value = characterStrength
        elif stat_type == "dexterity":
            current_value = characterDexterity
        elif stat_type == "defense":
            current_value = characterDefense

        # Calculate the change
        change = value - current_value

        # Check if we can make the change
        if change > 0 and skillPoints <= 0:
            # Revert the slider if we're out of skill points
            slider.set(current_value)
            return
        
        # Update the appropriate stat
        if stat_type == "vitality":
            characterVitality = value
        elif stat_type == "strength":
            characterStrength = value
        elif stat_type == "dexterity":
            characterDexterity = value
        elif stat_type == "defense":
            characterDefense = value

        # Update skill points
        skillPoints -= change
        
        # Update labels
        skill_points_label.configure(text=f"Skill Points: {skillPoints}")
        label.configure(text=f"{stat_type.capitalize()}: {value}")
        
        # Check if save button is valid now
        update_save_button_state()

    # Add this function after handle_stat_change
    def update_save_button_state():
        global skillPoints, characterName
        # Get the current text from the input box
        characterName = input_id.get("1.0", "end-1c").strip() 
        
        # Enable button only if skillPoints is 0 and name is not empty
        if skillPoints == 0 and characterName != "":
            save_button.configure(state="normal")
        else:
            save_button.configure(state="disabled")

    # Create frame for name input
    name_frame = Frame(left_frame, bg="#FFFFFF")
    name_frame.pack(side=tk.TOP, expand=True)

    # Create name label
    name_label = customtkinter.CTkLabel(
    master=name_frame,
    text=f"Character Name: ",
    font=("Arial", 20),
    text_color="#000000",
    height=30,
    width=200,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    compound="center",
    anchor="center"
    )
    name_label.pack(side=tk.LEFT, expand=True)

    # Create input box
    input_id = customtkinter.CTkTextbox(
        master=name_frame,
        font=("Arial", 20),
        text_color="#000000",
        height=30,
        width=200,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
    )
    input_id.insert("1.0", characterName)
    input_id.pack(side=tk.LEFT, expand=True)

    # Bind the textbox to update save button when text changes
    input_id.bind('<KeyRelease>', lambda e: update_save_button_state())

    # Create a frame for Vitality label/slider
    vitality_frame = Frame(left_frame, bg="#FFFFFF")
    vitality_frame.pack(side=tk.TOP, expand=True)

    # Create Vitality label
    vitality_label = customtkinter.CTkLabel(
        master=vitality_frame,
        text=f"Vitality: {characterVitality}",
        font=("Arial", 20),
        text_color="#000000",
        height=30,
        width=200,
        corner_radius=0,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
        compound="center",
        anchor="center"
    )
    vitality_label.pack(side=tk.TOP, padx=10)

    # Create Vitality slider
    vitality_slider = customtkinter.CTkSlider(
        master=vitality_frame,
        from_=0,
        to=10,
        number_of_steps=10,
        width=200,
        height=20,
        border_width=2,
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        progress_color="#00ff55",
        button_color="#00ff55",
        button_hover_color="#188124",
        command=lambda x: handle_stat_change(x, "vitality", vitality_label, vitality_slider)
    )
    vitality_slider.pack(side=tk.TOP, padx=10)
    vitality_slider.set(characterVitality)  # Set initial value

    # Create a frame for Strength label/slider
    strength_frame = Frame(left_frame, bg="#FFFFFF")
    strength_frame.pack(side=tk.TOP, expand=True)

    # Create strength label
    strength_label = customtkinter.CTkLabel(
    master=strength_frame,
    text=f"Strength: {characterStrength}",
    font=("Arial", 20),
    text_color="#000000",
    height=30,
    width=200,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    compound="center",
    anchor="center"
    )
    strength_label.pack(side=tk.TOP, expand=True)

    # Create strength slider
    strength_slider = customtkinter.CTkSlider(
        master=strength_frame,
        from_=0,
        to=10,
        number_of_steps=10,
        width=200,
        height=20,
        border_width=2,
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        progress_color="#00ff55",
        button_color="#00ff55",
        button_hover_color="#188124",
        command=lambda x: handle_stat_change(x, "strength", strength_label, strength_slider)
    )
    strength_slider.pack(side=tk.TOP, expand=True)
    strength_slider.set(characterStrength) # Set initial value

    # Create a frame for Dexterity label/slider
    dexterity_frame = Frame(left_frame, bg="#FFFFFF")
    dexterity_frame.pack(side=tk.TOP, expand=True)

    # Create Dexterity label
    dexterity_label = customtkinter.CTkLabel(
    master=dexterity_frame,
    text=f"Dexterity: {characterDexterity}",
    font=("Arial", 20),
    text_color="#000000",
    height=30,
    width=200,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    compound="center",
    anchor="center"
    )
    dexterity_label.pack(side=tk.TOP, expand=True)

    # Create Dexterity slider
    dexterity_slider = customtkinter.CTkSlider(
        master=dexterity_frame,
        from_=0,
        to=10,
        number_of_steps=10,
        width=200,
        height=20,
        border_width=2,
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        progress_color="#00ff55",
        button_color="#00ff55",
        button_hover_color="#188124",
        command=lambda x: handle_stat_change(x, "dexterity", dexterity_label, dexterity_slider)
    )
    dexterity_slider.pack(side=tk.TOP, expand=True)
    dexterity_slider.set(characterDexterity) #Set initial value

    # Create a frame for Defense label/slider
    defense_frame = Frame(left_frame, bg="#FFFFFF")
    defense_frame.pack(side=tk.TOP, expand=True)

    # Create defense label
    defense_label = customtkinter.CTkLabel(
    master=defense_frame,
    text=f"Defense: {characterDefense}",
    font=("Arial", 20),
    text_color="#000000",
    height=30,
    width=200,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    compound="center",
    anchor="center"
    )
    defense_label.pack(side=tk.TOP, expand=True)

    # Create defense slider
    defense_slider = customtkinter.CTkSlider(
        master=defense_frame,
        from_=0,
        to=10,
        number_of_steps=10,
        width=200,
        height=20,
        border_width=2,
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        progress_color="#00ff55",
        button_color="#00ff55",
        button_hover_color="#188124",
        command=lambda x: handle_stat_change(x, "defense", defense_label, defense_slider)
    )
    defense_slider.pack(side=tk.TOP, expand=True)
    defense_slider.set(characterDefense)

    right_frame = Frame(char_edit_frame, width=400, height=600)
    right_frame.propagate(0)
    right_frame.pack(side=tk.LEFT, expand=TRUE)

    image_id = customtkinter.CTkImage(
        light_image=Image.open(sprite_paths[sprite_index]),
        size=(250, 500)
    )

    image_label = customtkinter.CTkLabel(right_frame, image=image_id, text="") 
    image_label.pack(side=tk.TOP, expand=TRUE)

    img_button_frame = Frame(right_frame, width=400, height=100)
    img_button_frame.propagate(0)
    img_button_frame.pack(side=tk.BOTTOM, expand=TRUE)

    def handle_sprite_change(img, num):
        global sprite_index, sprite_paths
        
        if sprite_index >= len(sprite_paths) - 1 and num == 1:
            sprite_index = 0
        elif sprite_index == 0 and num == -1:
            sprite_index = len(sprite_paths) - 1
        else:
            sprite_index += num

        img.configure(light_image=Image.open(sprite_paths[sprite_index]))

    back_button = customtkinter.CTkButton(
        master=img_button_frame,
        text="Back",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#188124",
        height=30,
        width=100,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#00ff55",
        command=lambda: handle_sprite_change(image_id, -1)
    )
    back_button.pack(side=tk.LEFT, expand=TRUE)

    next_button = customtkinter.CTkButton(
        master=img_button_frame,
        text="Next",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#188124",
        height=30,
        width=100,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#00ff55",
        command=lambda: handle_sprite_change(image_id, 1)
    )
    next_button.pack(side=tk.LEFT, expand=TRUE)

    # Handle saving the character
    def save_character():
        global characterName, characterVitality, characterStrength, characterDexterity, characterDefense, skillPoints
        
        # Load existing characters or create empty list
        all_characters = []
        if os.path.exists("Characters.json"):
            try:
                with open("Characters.json", "r") as file:
                    all_characters = json.load(file)
            except json.JSONDecodeError:
                # Handle case where file exists but is empty or invalid
                all_characters = []
        
        # Edit character
        for character in all_characters:
            if character.get("name") == name:
                character.update({"name": characterName})
                character.update({"vitality": characterVitality})
                character.update({"strength": characterStrength})
                character.update({"dexterity": characterDexterity})
                character.update({"defense": characterDefense})
                character.update({"sprite_path": sprite_index})
                break
        
        # Save to file
        try:
            with open("Characters.json", "w") as file:
                json.dump(all_characters, file, indent=3)
            messagebox.showinfo("Success", "Character edited successfully!")
            #Reset all variables for next character
            skillPoints = 10
            characterName = ""
            characterVitality = 0
            characterStrength = 0
            characterDexterity = 0
            characterDefense = 0
            # Navigate back to main menu
            window_manager.navigate_to(window, frame, "edit")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit character: {str(e)}")

    # Create save character button
    save_button = customtkinter.CTkButton(
        master=frame,
        text="Edit Character",
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
        state="disabled",
        command=save_character
        )
    save_button.pack(side=tk.TOP, expand=True)

    exit_button = customtkinter.CTkButton(
        master=frame,
        text="Exit",
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
        command=lambda: window_manager.navigate_to(window, frame, "edit")
        )
    exit_button.pack(side=tk.TOP, expand=True)