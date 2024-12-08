
# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager

def updateMainMenuWindow(window, frame, acc):
    #Update window title
    frame = window_manager.update_window(window, frame, "Main Menu")

    #Create a title label
    title_label = customtkinter.CTkLabel(
        master=frame,
        text="Main Menu",
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

    #Create the play game button
    play_game_button = customtkinter.CTkButton(
        master=frame,
        text="Play Game",
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
        command=lambda: window_manager.navigate_to(window, frame, acc, "play")
        )
    play_game_button.pack(side=tk.TOP, expand=True)

    #Create the new character button
    new_char_button = customtkinter.CTkButton(
        master=frame,
        text="New Character",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=150,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=lambda: window_manager.navigate_to(window, frame, acc, "new")
        )
    new_char_button.pack(side=tk.TOP, expand=True)

    #Create the edit character button
    edit_char_button = customtkinter.CTkButton(
        master=frame,
        text="Edit Character",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=150,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=lambda: window_manager.navigate_to(window, frame, acc, "edit")
        )
    edit_char_button.pack(side=tk.TOP, expand=True)

    #Create the remove character button
    remove_char_button = customtkinter.CTkButton(
        master=frame,
        text="Remove Character",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=150,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=lambda: window_manager.navigate_to(window, frame, acc, "remove")
        )
    remove_char_button.pack(side=tk.TOP, expand=True)

    #Create the character details button
    char_details_button = customtkinter.CTkButton(
        master=frame,
        text="Character Details",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#949494",
        height=30,
        width=150,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#F0F0F0",
        command=lambda: window_manager.navigate_to(window, frame, acc, "details")
        )
    char_details_button.pack(side=tk.TOP, expand=True)

    #Create the exit game button
    exit_game_button = customtkinter.CTkButton(
        master=frame,
        text="Exit Game",
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
        command=lambda: window_manager.quit(window)
        )
    exit_game_button.pack(side=tk.TOP, expand=True)
