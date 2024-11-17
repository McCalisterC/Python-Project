
# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager

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
    