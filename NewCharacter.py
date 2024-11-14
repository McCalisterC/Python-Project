
# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter

# Main Window Properties

def updateWindow(window, frame):
    
    frame.destroy()
    window.title("New Character")
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    frame = Frame(window, width="1280", height="720")
    frame.pack(expand=True, fill="both")


    Label_id2 = customtkinter.CTkLabel(
    master=frame,
    text="New Character",
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
    