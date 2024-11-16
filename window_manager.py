from tkinter import *
import tkinter as tk

def update_window(window, frame, title):
    frame.destroy()
    window.title(title)
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    new_frame = Frame(window, width="1280", height="720")
    new_frame.pack(expand=True, fill="both")
    
    return new_frame

def navigate_to(window, frame, menu_type):
    if menu_type == "main":
        from MainMenu import updateMainMenuWindow
        updateMainMenuWindow(window, frame)
    elif menu_type == "new":
        from NewCharacterMenu import updateWindow
        updateWindow(window, frame)
    elif menu_type == "edit":
        from EditCharacterMenu import updateWindow
        updateWindow(window, frame)
    elif menu_type == "remove":
        from RemoveCharacterMenu import updateWindow
        updateWindow(window, frame)
    elif menu_type == "details":
        from CharacterDetailsMenu import updateWindow
        updateWindow(window, frame) 