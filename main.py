from tkinter import *
from MainMenu import MainMenu


# Create Window
window = Tk()
window.geometry("1300x700")
#window.resizable(width=False, height=False)
window.wm_geometry(f"{1020}x{700}+{0}+{0}")
window.config(bg="grey")

# Create widgets

menu = MainMenu(window)


window.mainloop()
