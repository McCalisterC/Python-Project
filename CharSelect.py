
# libraries Import
from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter
import window_manager
import account

def updateWindow(window, frame, acc, title, type):
    #Update window title
    frame = window_manager.update_window(window, frame, title)

    #Create a label for title of window
    title_label = customtkinter.CTkLabel(
        master=frame,
        text=title,
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

    #Scrollable frame for any amount of characters
    scrollFrame = customtkinter.CTkScrollableFrame(frame, width=1000, height=500)
    scrollFrame.pack(side=tk.TOP, expand=TRUE)

    #Load in characters
    all_characters = []
    with account.SessionFactory() as session:
        characters = session.query(account.Character).filter_by(account_id=acc.id).all()
        for character in characters:
            all_characters.append(character)

    #If all_character has values, create characters
    if all_characters != []:
        flipColor = False

        function = None

        #For each character in all_characters, create a clickable entry
        for character in all_characters:
            match type:
                case "edit":
                    function = window_manager.navigate_to_character_edit
                case "details":
                    function = window_manager.navigate_to_character_detail
                case "battle":
                    function = window_manager.navigate_to_battle
                case "remove":
                    function = confirmDelete

            color = "#FFFFFF"

            #Check flipColor to determine what color the background should be
            if(flipColor):
                color = "#D3D3D3"

            #Create frame for new char entry
            charFrame = Frame(scrollFrame, width=950, height=100, background=color)
            charFrame.pack_propagate(0)
            charFrame.pack(side=tk.TOP, expand=TRUE)

            #Create label for character's name to be placed in charFrame
            charLabel = customtkinter.CTkButton(
                master=charFrame,
                text=str(character.name),
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
                command=lambda char=character: function(window, frame, acc, char)
            )
            charLabel.pack(fill="both", expand=TRUE)

            #flip color
            flipColor = not(flipColor)

    #Else tell user that no characters have been found
    else:
        #Create frame for error
        errorFrame = Frame(scrollFrame, width=950, height=100)
        errorFrame.pack_propagate(0)
        errorFrame.pack(side=tk.TOP, expand=TRUE)
        
        #Create error label
        errorLabel = customtkinter.CTkLabel(
            master=errorFrame,
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

    #Create exit button
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
        command=lambda: window_manager.navigate_to(window, frame, acc, "main")
        )
    exit_button.pack(side=tk.TOP, expand=True)
    
#Function to create a confirmation box for deletion
def confirmDelete(window, frame, acc, char):
    result = messagebox.askyesno(title="Confirmation", message="Are you sure you want to proceed?")
    if result:
        with account.SessionFactory() as session:
            character = session.query(account.Character).filter_by(id=char.id).first()
            if character:
                session.delete(character)
                session.commit()
                updateWindow(window, frame, acc, "Remove Character", "remove")
        return
    else:
        return