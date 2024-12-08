from tkinter import *
import tkinter as tk

#Function to update the window with a new blank frame
def update_window(window, frame, title):
    frame.destroy()
    window.title(title)
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    new_frame = Frame(window, width="1280", height="720")
    new_frame.pack(expand=True, fill="both")
    
    return new_frame

#Function that navigates to a different menu/window depending on menu type
def navigate_to(window, frame, acc, menu_type):
    if menu_type == "main":
        from MainMenu import updateMainMenuWindow
        updateMainMenuWindow(window, frame, acc)
    elif menu_type == "new":
        from CharacterCreationScreen import updateWindow
        updateWindow(window, frame, acc,"New Character", -1)
    elif menu_type == "edit":
        from CharSelect import updateWindow
        updateWindow(window, frame, acc, "Edit Character", "edit")
    elif menu_type == "remove":
        from CharSelect import updateWindow
        updateWindow(window, frame, acc, "Remove Character", "remove")
    elif menu_type == "details":
        from CharSelect import updateWindow
        updateWindow(window, frame, acc, "Character Details", "details") 
    elif menu_type == "play":
        from CharSelect import updateWindow
        updateWindow(window, frame, acc, "Select Character", "battle")

#Function that navigates to the login screen
def navigate_to_login(window, frame):
    from LoginScreen import updateWindow
    updateWindow(window, frame)

#Function that navigates to the character edit screen
def navigate_to_character_edit(window, frame, acc, char):
    from CharacterCreationScreen import updateWindow
    updateWindow(window, frame, acc, "Edit Character", char)

#Function that navigates to the character detail screen
def navigate_to_character_detail(window, frame, acc, char):
    from CharDetailScreen import updateWindow
    updateWindow(window, frame, acc, char)

#Function that navigates to the battle screen
def navigate_to_battle(window, frame, acc, char):
    from BattleScreen import updateWindow
    updateWindow(window, frame, acc, char)

#Function that quits the application
def quit(window):
    window.destroy()