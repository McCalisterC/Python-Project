
# libraries Import
from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter
import window_manager
import json
import os

# Main Window Properties

def updateWindow(window, frame):
    frame = window_manager.update_window(window, frame, "Remove Character")

    Label_id2 = customtkinter.CTkLabel(
    master=frame,
    text="Remove Character",
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
    Label_id2.pack(side=tk.TOP, expand=True)

    # Scrollable frame for any amount of characters
    scrollFrame = customtkinter.CTkScrollableFrame(frame, width=1000, height=500)
    scrollFrame.pack(side=tk.TOP, expand=TRUE)

    all_characters = []
    if os.path.exists("Characters.json"):
        try:
            with open("Characters.json", "r") as file:
                all_characters = json.load(file)
        except json.JSONDecodeError:
            # Handle case where file exists but is empty or invalid
            all_characters = []


    if all_characters != []:
        flipColor = False

        for character in all_characters:
            color = "#FFFFFF"

            if(flipColor):
                color = "#D3D3D3"

            charFrame = Frame(scrollFrame, width=950, height=100)
            charFrame.pack_propagate(0)
            charFrame.pack(side=tk.TOP, expand=TRUE)

            charLabel = customtkinter.CTkButton(
                master=charFrame,
                text=str(character.get("name")),
                font=("undefined", 50),
                text_color="#000000",
                hover=True,
                hover_color="#90EE90",
                height=30,
                width=150,
                border_width=2,
                corner_radius=6,
                border_color="#000000",
                bg_color=color,
                fg_color=color,
                command=lambda char=character: confirmDelete(window, frame, all_characters, char)
            )
                
            charLabel.pack(fill="both", expand=TRUE)

            flipColor = not(flipColor)
    else:
        charFrame = Frame(scrollFrame, width=950, height=100)
        charFrame.pack_propagate(0)
        charFrame.pack(side=tk.TOP, expand=TRUE)
        
        errorLabel = customtkinter.CTkLabel(
            master=charFrame,
            text="No characters found",
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
        errorLabel.pack(side=tk.TOP, expand=TRUE)

    Button_id7 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "main")
        )
    Button_id7.pack(side=tk.TOP, expand=True)
    
def confirmDelete(window, frame, allChars, char):
    result = messagebox.askyesno(title="Confirmation", message="Are you sure you want to proceed?")
    if result:
        allChars.remove(char)
        with open("Characters.json", "w") as file:
                json.dump(allChars, file, indent=3)
        updateWindow(window, frame)
        return
    else:
        return