from tkinter import *
import window_manager

#Initalizes the window and then navigates to the login page
def main():
    window = Tk()
    window.title("Login")
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    frame = Frame(window, width="1280", height="720")
    frame.pack(expand=True, fill="both")

    window_manager.navigate_to_login(window, frame)
    window.mainloop()

main()