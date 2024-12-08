
# libraries Import
from tkinter import *
import tkinter as tk
import customtkinter
import window_manager
import account
from tkinter import messagebox
import hashlib, re

def updateWindow(window, frame):
    #Update window title
    frame = window_manager.update_window(window, frame, "Login")

    #Create a title label
    title_label = customtkinter.CTkLabel(
        master=frame,
        text="Login",
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

    #Create a description label
    description_label = customtkinter.CTkLabel(
        master=frame,
        text="Enter Your Account Details and Press The Login Button to Login.\n\nIf You Do Not Have An Account, Enter Your Desired Account Details and Press Register.",
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
    description_label.pack(side=tk.TOP, expand=True)

    # Create frame for username input
    username_frame = Frame(frame, bg="#FFFFFF")
    username_frame.pack(side=tk.TOP, expand=True)

    # Create username label
    username_label = customtkinter.CTkLabel(
        master=username_frame,
        text=f"User Name: ",
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
    username_label.pack(side=tk.LEFT, expand=True)

    # Create input box
    username_input = customtkinter.CTkTextbox(
        master=username_frame,
        font=("Arial", 20),
        text_color="#000000",
        height=30,
        width=200,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
    )
    username_input.bind("<Tab>", focus_next_window)
    username_input.bind("<Return>", lambda event: enter_submit(window, frame, username_input.get("1.0", "end-1c").strip(), password_input.get("1.0", "end-1c").strip()))
    username_input.pack(side=tk.LEFT, expand=True)

    # Create frame for password input
    password_frame = Frame(frame, bg="#FFFFFF")
    password_frame.pack(side=tk.TOP, expand=True)

    # Create username label
    password_label = customtkinter.CTkLabel(
        master=password_frame,
        text=f"Password: ",
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
    password_label.pack(side=tk.LEFT, expand=True)

    # Create input box
    password_input = customtkinter.CTkTextbox(
        master=password_frame,
        font=("Arial", 20),
        text_color="#000000",
        height=30,
        width=200,
        bg_color="#FFFFFF",
        fg_color="#FFFFFF",
    )
    password_input.bind("<Tab>", focus_next_window)
    password_input.bind("<Return>", lambda event: enter_submit(window, frame, username_input.get("1.0", "end-1c").strip(), password_input.get("1.0", "end-1c").strip()))
    password_input.pack(side=tk.LEFT, expand=True)

    # Create password requirements label
    password_requirements_label = customtkinter.CTkLabel(
        master=frame,
        text="Password must start with one of the following special characters !@#$%^&, contain at least one digit, \none lowercase letter and one uppercase letter and must be between 6 and 12 characters long.",
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
    password_requirements_label.pack(side=tk.TOP, expand=True)

    #Create a frame for the buttons
    button_frame = customtkinter.CTkFrame(
        master=frame,
        width=500,
        height=50
    )
    button_frame.propagate(0)
    button_frame.pack(side=tk.TOP, expand=True)

    #Create a button to login
    login_button = customtkinter.CTkButton(
        master=button_frame,
        text="Login",
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
        command=lambda: handleLogin(window, frame, username_input.get("1.0", "end-1c").strip(), password_input.get("1.0", "end-1c").strip())
    )
    login_button.pack(side=tk.LEFT, expand=True)

    #Create a button to register
    register_button = customtkinter.CTkButton(
        master=button_frame,
        text="Register",
        font=("undefined", 16),
        text_color="#000000",
        hover=True,
        hover_color="#0F52BA",
        height=30,
        width=150,
        border_width=2,
        corner_radius=6,
        border_color="#000000",
        bg_color="#FFFFFF",
        fg_color="#68C2F5",
        command=lambda: handleRegister(username_input.get("1.0", "end-1c").strip(), password_input.get("1.0", "end-1c").strip())
    )
    register_button.pack(side=tk.LEFT, expand=True)

    #Create a button to exit the application
    exit_button = customtkinter.CTkButton(
        master=button_frame,
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
    exit_button.pack(side=tk.LEFT, expand=True)

#Function for handling registering
def handleRegister(username, password):
    #Check if username and password is empty and display an error if so
    if not username or not password:
        messagebox.showerror("Error", "Username or password cannot be empty!")
        return
    
    #Create a match for the account password requirement and passed in password
    match = re.match(account.regex, password)

    #Check if match is valid and display appropriate error message if not
    if not match:
        messagebox.showerror("Error", "Password does not meet requirements!")
        return
    #If password is valid create new variable with the password encoded
    else:
        passwordEncoded = hashlib.md5(password.encode()).hexdigest()

    #Open the SessionFacotry from the account module as a session
    with account.SessionFactory() as session:
        try:
            #Create a new account object
            new_account = account.Account(username=username, password=passwordEncoded, level=1, xp=0)

            #Add and commit the new account
            session.add(new_account)
            session.commit()
            #Display success message
            messagebox.showinfo("Success", f"Account '{username}' successfully registered!")
        except Exception as e:
            #Display error message
            messagebox.showerror("Error", f"Error registering account: {e}")
            #Rollback the session
            session.rollback()

#Function for handling login
def handleLogin(window, frame, username, password):
    #Check if username and password is empty and display an error if so
    if not username or not password:
        messagebox.showerror("Error", "Username or password cannot be empty!")
        return

    #Open the SessionFacotry from the account module as a session
    with account.SessionFactory() as session:
        #Create acc variable and assign by filtering through the database for an accout with ther passed in username
        acc = session.query(account.Account).filter_by(username=username).first()

        #Check if the account exist and display an error if not
        if acc:
            #Check if the password is correct and display an error if not
            if acc.password == hashlib.md5(password.encode()).hexdigest():
                window_manager.navigate_to(window, frame, acc, "main")
            else:
                messagebox.showerror("Error", "Password is incorrect!")
        else:
            messagebox.showerror("Error", "Account does not exist!")
        
#Function to shift focus to next input field
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

#Function to handle logining when pressing the enter key (Must be done this way to prevent enter key from creating a new line in the text field)
def enter_submit(window, frame, username, password):
    handleLogin(window, frame, username, password)
    return("break")