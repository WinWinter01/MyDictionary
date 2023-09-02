from tkinter import *
from tkinter import ttk
import pandas as pd

LENGHT_ROW = 49  # 49 symbols
HEIGHT_ROW = 3  # 3 row
DEFAUL_FILL_FILE = {'English': [], 'Translate': [], 'Phrase': []}

class CreateWidgets:
    def __init__(self, window):
        self.window = window
        try:
            self.words = pd.read_csv("data.csv")
        except:
            updated_words = pd.DataFrame(DEFAUL_FILL_FILE)
            updated_words.to_csv("data.csv", index=False)
            self.words = pd.read_csv("data.csv")
        self.words_dict = self.words.to_dict(orient="records")

        self.window.bind("<Tab>", self.select_next_widget)
        self.window.bind("<Return>", self.on_enter)
        self.count_edit_btn = 0  # 1 = you can edit word, 2 = confirm edition

    def create_widgets(self):
        ###################################
        # Create words list
        self.tree = ttk.Treeview()

        # Style
        s = ttk.Style()
        s.configure('Treeview', rowheight=50, font=(None, 10))

        # Define Our Columns
        self.tree['columns'] = ("English", "Translate", "Phrase")

        # Formate Our Columns
        self.tree.column("#0", width=50, anchor=W)
        self.tree.column("English", anchor=CENTER, width=300)
        self.tree.column("Translate", anchor=CENTER, width=300)
        self.tree.column("Phrase", anchor=W, width=330)

        # Create Headings
        self.tree.heading("#0", text="№")
        self.tree.heading("English", text="English", anchor=CENTER)
        self.tree.heading("Translate", text="Translate", anchor=CENTER)
        self.tree.heading("Phrase", text="Phrase", anchor=W)

        # Add Dataa
        self.insert_words_list()
        # Pack to the screen
        self.tree.grid(column=0, row=0, pady=20, stick='', padx=20, columnspan=4)
        ###################################
        # Another widgets

        # index
        self.index_entry = Entry()
        self.index_entry.grid(column=0, row=1, stick='', padx=5, pady=5)
        self.index_entry.insert(0, "number or delete last")
        self.index_entry.bind("<FocusIn>", lambda event: self.focus_on(event, "index_entry"))
        self.index_entry.bind("<FocusOut>", lambda event: self.focus_out(event, "index_entry"))

        # word
        self.word_entry = Entry()
        self.word_entry.grid(column=1, row=1, stick='', padx=5, pady=5)
        self.word_entry.insert(0, "Enter the word")
        self.word_entry.bind("<FocusIn>", lambda event: self.focus_on(event, "word_entry"))
        self.word_entry.bind("<FocusOut>", lambda event: self.focus_out(event, "word_entry"))

        # translate
        self.translate_entry = Entry()
        self.translate_entry.grid(column=2, row=1, stick='', padx=5, pady=5)
        self.translate_entry.insert(0, "Enter the translate")
        self.translate_entry.bind("<FocusIn>", lambda event: self.focus_on(event, "translate_entry"))
        self.translate_entry.bind("<FocusOut>", lambda event: self.focus_out(event, "translate_entry"))

        # phrase
        self.phrase_entry = Entry()
        self.phrase_entry.grid(column=3, row=1, stick='', padx=5, pady=5)
        self.phrase_entry.insert(0, "Enter the phrase")
        self.phrase_entry.bind("<FocusIn>", lambda event: self.focus_on(event, "phrase_entry"))
        self.phrase_entry.bind("<FocusOut>", lambda event: self.focus_out(event, "phrase_entry"))

        # btn add
        self.addWord_btn = Button(text="Add Word", command=self.add_word)
        self.addWord_btn.grid(column=0, row=2, stick='e', padx=50, pady=5, columnspan=2)

        # btn delete
        self.DeleteWord_btn = Button(text="Delete Word", command=self.delete_word)
        self.DeleteWord_btn.grid(column=1, row=2, stick='', padx=5, pady=5, columnspan=2)

        # btn edit
        self.EditWord_btn = Button(text="Edit Word", command=self.edit_word)
        self.EditWord_btn.grid(column=2, row=2, stick='w', padx=50, pady=5, columnspan=2)