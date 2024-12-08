# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import json
import os
from tkinter import messagebox

skillPoints = 10
characterName = ""
characterVitality = 0
characterStrength = 0
characterDexterity = 0
characterDefense = 0
level = 0
xp = 0
next_level_xp = 0
enemies_defeated = 0
secrets = 0

# Main Window Properties
def updateWindow(window, frame, acc, char):
    global skillPoints, characterVitality, characterStrength, characterDexterity, characterDefense, characterName, level, xp, next_level_xp, enemies_defeated, secrets
    
    # Update window using window_manager
    frame = window_manager.update_window(window, frame, "New Character")

    # Load character passed in
    characterName = char.name
    characterVitality = char.vitality
    characterStrength = char.strength
    characterDexterity = char.dexterity
    characterDefense = char.defense
    skillPoints = (9 + char.level) - (characterVitality + characterDefense + characterStrength + characterDexterity)
    level = char.level
    xp = char.xp
    next_level_xp = level * 40
    enemies_defeated = char.defeated_enemies
    secrets = char.secrets

    # Create title label
    title_label = customtkinter.CTkLabel(
        master=frame,
        text=characterName + " Details",
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

    #Create frame for the details
    detailsFrame = Frame(frame, width=1000, height=600)
    detailsFrame.propagate(0)
    detailsFrame.pack(side=tk.TOP, expand=TRUE)

    #Create the left side of the frame for editable values
    leftFrame = Frame(detailsFrame, width=400, height=600, bg="#FFFFFF")
    leftFrame.propagate(0)
    leftFrame.pack(side=tk.LEFT, expand=TRUE)

    # Create label for left side title
    editedable_stats_label = customtkinter.CTkLabel(
        master=leftFrame,
        text="Editable Details",
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
    editedable_stats_label.pack(side=tk.TOP, expand=True)

    # Create skill points label
    skill_points_label = customtkinter.CTkLabel(
        master=leftFrame,
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

    # Create frame for name input
    name_frame = Frame(leftFrame, bg="#FFFFFF")
    name_frame.pack(side=tk.TOP, expand=True)

    # Create name label
    name_label = customtkinter.CTkLabel(
        master=name_frame,
        text=f"Character Name: {characterName}",
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

    # Create a frame for Vitality label/slider
    vitality_frame = Frame(leftFrame, bg="#FFFFFF")
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

    # Create a frame for Strength label/slider
    strength_frame = Frame(leftFrame, bg="#FFFFFF")
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

    # Create a frame for Dexterity label/slider
    dexterity_frame = Frame(leftFrame, bg="#FFFFFF")
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

    # Create a frame for Defense label/slider
    defense_frame = Frame(leftFrame, bg="#FFFFFF")
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

    #Create right side of frame for lifetime statistics
    rightFrame = Frame(detailsFrame, width=400, height=600, bg="#FFFFFF")
    rightFrame.propagate(0)
    rightFrame.pack(side=tk.LEFT, expand=TRUE)

    # Create right side title label
    lifetime_stats_label = customtkinter.CTkLabel(
        master=rightFrame,
        text="Lifetime Statistics",
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
    lifetime_stats_label.pack(side=tk.TOP, expand=True)

    # Create level label
    level_label = customtkinter.CTkLabel(
        master=rightFrame,
        text=f"Level: {level}",
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
    level_label.pack(side=tk.TOP, expand=True)

    #Create xp label
    xp_label = customtkinter.CTkLabel(
        master=rightFrame,
        text=f"XP: {xp}",
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
    xp_label.pack(side=tk.TOP, expand=True)

    #Create xp to next level label
    xp_to_next_label = customtkinter.CTkLabel(
        master=rightFrame,
        text=f"XP Until Next Level: {next_level_xp}",
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
    xp_to_next_label.pack(side=tk.TOP, expand=True)

    #Create enemies defeated label
    enemies_defeated_label = customtkinter.CTkLabel(
        master=rightFrame,
        text=f"Enemies Defeated: {enemies_defeated}",
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
    enemies_defeated_label.pack(side=tk.TOP, expand=True)

    #Create secrets found label
    secrets_label = customtkinter.CTkLabel(
        master=rightFrame,
        text=f"Secrets Found: {secrets}",
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
    secrets_label.pack(side=tk.TOP, expand=True)

    #Create the exit button
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
        command=lambda: window_manager.navigate_to(window, frame, acc, "details")
        )
    exit_button.pack(side=tk.BOTTOM, expand=True)