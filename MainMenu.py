
# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager

def updateMainMenuWindow(window, frame):
    frame = window_manager.update_window(window, frame, "Main Menu")

    Label_id2 = customtkinter.CTkLabel(
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
    Label_id2.pack(side=tk.TOP, expand=True)
    Button_id4 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "play")
        )
    Button_id4.pack(side=tk.TOP, expand=True)
    Button_id1 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "new")
        )
    Button_id1.pack(side=tk.TOP, expand=True)
    Button_id3 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "edit")
        )
    Button_id3.pack(side=tk.TOP, expand=True)
    Button_id5 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "remove")
        )
    Button_id5.pack(side=tk.TOP, expand=True)
    Button_id6 = customtkinter.CTkButton(
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
        command=lambda: window_manager.navigate_to(window, frame, "details")
        )
    Button_id6.pack(side=tk.TOP, expand=True)
    Button_id7 = customtkinter.CTkButton(
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
    Button_id7.pack(side=tk.TOP, expand=True)
