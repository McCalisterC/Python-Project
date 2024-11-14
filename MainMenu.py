
# libraries Import
from tkinter import *
import customtkinter

# Main Window Properties

window = Tk()
window.title("Tkinter")
window.geometry("1280x720")
window.configure(bg="#FFFFFF")


Button_id4 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id4.place(x=600, y=200)
Button_id1 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id1.place(x=600, y=250)
Button_id3 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id3.place(x=600, y=300)
Button_id5 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id5.place(x=600, y=350)
Button_id7 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id7.place(x=600, y=450)
Label_id2 = customtkinter.CTkLabel(
    master=window,
    text="Main Menu",
    font=("Arial", 30),
    text_color="#000000",
    height=30,
    width=200,
    corner_radius=0,
    bg_color="#FFFFFF",
    fg_color="#FFFFFF",
    )
Label_id2.place(x=580, y=150)
Button_id6 = customtkinter.CTkButton(
    master=window,
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
    )
Button_id6.place(x=600, y=400)



#run the main loop
window.mainloop()