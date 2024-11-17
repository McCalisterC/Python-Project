from tkinter import *
import tkinter as tk
import window_manager

def main():
    window = Tk()
    window.title("Main Menu")
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    frame = Frame(window, width="1280", height="720")
    frame.pack(expand=True, fill="both")

    window_manager.navigate_to(window, frame, "main")
    window.mainloop()

main()