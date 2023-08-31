from tkinter import *
from tkinter import ttk
import pandas as pd
import textwrap
from MainMenu import MainMenu

menu = MainMenu()

# Data
words = pd.read_csv("data.csv")
words_dict = words.to_dict(orient="records")
words_eng = words["English"]
words_rus = words["Translate"]
phrases = words["Phrase"]

def wrap(string, lenght=49):
    return '\n'.join(textwrap.wrap(string, lenght))

def insert_tree():
    count = 0
    for i in words_dict:
        tree.insert(parent='', index='end', iid=count, text=count+1, values=(i["English"], i["Translate"], wrap(i["Phrase"])))
        count += 1

def on_EntryWord_click(event):
    if word_entry.get() == "Enter the word":
        word_entry.delete(0, "end")

def focus_EntryWord_out(event):
    if word_entry.get() == "":
        word_entry.delete(0, "end")
        word_entry.insert(0, "Enter the word")

window = Tk()
window.geometry("1300x700")
window.config(bg="grey")

tree = ttk.Treeview()

# Style
s = ttk.Style()
s.configure('Treeview', rowheight=50, font=(None, 10))

# Define Our Columns
tree['columns'] = ("English", "Translate", "Phrase")

# Formate Our Columns
tree.column("#0", width=50, anchor=W)
tree.column("English", anchor=CENTER, width=330)
tree.column("Translate", anchor=CENTER, width=330)
tree.column("Phrase", anchor=W, width=350)

# Create Headings
tree.heading("#0", text="№")
tree.heading("English", text="English", anchor=CENTER)
tree.heading("Translate", text="Translate", anchor=CENTER)
tree.heading("Phrase", text="Phrase", anchor=W)

# Add Data
insert_tree()

# Pack to the screen
tree.grid(column=0, row=0, pady=20, padx=20)

word_entry = Entry()

word_entry.grid(column=1, row=0)
word_entry.insert(0, "Enter the word")
word_entry.bind("<FocusIn>", on_EntryWord_click)
word_entry.bind("<FocusOut>", focus_EntryWord_out)



window.mainloop()
