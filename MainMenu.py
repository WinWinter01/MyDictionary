from tkinter import *
from tkinter import ttk
import textwrap
import pandas as pd
from tkinter import messagebox

LENGHT_ROW = 49  # 49 symbols
HEIGHT_ROW = 3  # 3 row
DEFAUL_FILL_FILE = {'English': [], 'Translate': [], 'Phrase': []}


class MainMenu:
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

        self.create_widgets()

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
        self.index_entry.bind("<FocusIn>", lambda event: self.on_EntryWord_click(event, "index_entry"))
        self.index_entry.bind("<FocusOut>", lambda event: self.focus_EntryWord_out(event, "index_entry"))

        # word
        self.word_entry = Entry()
        self.word_entry.grid(column=1, row=1, stick='', padx=5, pady=5)
        self.word_entry.insert(0, "Enter the word")
        self.word_entry.bind("<FocusIn>", lambda event: self.on_EntryWord_click(event, "word_entry"))
        self.word_entry.bind("<FocusOut>", lambda event: self.focus_EntryWord_out(event, "word_entry"))

        # translate
        self.translate_entry = Entry()
        self.translate_entry.grid(column=2, row=1, stick='', padx=5, pady=5)
        self.translate_entry.insert(0, "Enter the translate")
        self.translate_entry.bind("<FocusIn>", lambda event: self.on_EntryWord_click(event, "translate_entry"))
        self.translate_entry.bind("<FocusOut>", lambda event: self.focus_EntryWord_out(event, "translate_entry"))

        # phrase
        self.phrase_entry = Entry()
        self.phrase_entry.grid(column=3, row=1, stick='', padx=5, pady=5)
        self.phrase_entry.insert(0, "Enter the phrase")
        self.phrase_entry.bind("<FocusIn>", lambda event: self.on_EntryWord_click(event, "phrase_entry"))
        self.phrase_entry.bind("<FocusOut>", lambda event: self.focus_EntryWord_out(event, "phrase_entry"))

        # btn add
        self.addWord_btn = Button(text="Add Word", command=self.add_word)
        self.addWord_btn.grid(column=0, row=2, stick='e', padx=50, pady=5, columnspan=2)

        # btn delete
        self.DeleteWord_btn = Button(text="Delete Word", command=self.delete_word)
        self.DeleteWord_btn.grid(column=1, row=2, stick='', padx=5, pady=5, columnspan=2)

        # btn edit
        self.EditWord_btn = Button(text="Edit Word", command=self.edit_word)
        self.EditWord_btn.grid(column=2, row=2, stick='w', padx=50, pady=5, columnspan=2)

    def select_next_widget(self, event):
        current_focus = self.window.focus_get()
        next_focus = current_focus.tk_focusNext()
        next_focus.focus_set()

    def on_enter(self, evnet):
        try:
            self.window.focus_get().invoke()
        except:
            pass

    def wrap(self, string):
        return '\n'.join(textwrap.wrap(string, LENGHT_ROW))

    def insert_words_list(self):
        count = 0
        for i in self.words_dict:
            self.tree.insert(parent='', index='end', iid=str(count), text=str(count+1), values=(str(i["English"]), str(i["Translate"]), self.wrap(str(i["Phrase"]))))
            count += 1

    def on_EntryWord_click(self, event, widget):
        if widget == "word_entry" and self.word_entry.get() == "Enter the word":
            self.word_entry.delete(0, "end")
        elif widget == "translate_entry" and self.translate_entry.get() == "Enter the translate":
            self.translate_entry.delete(0, "end")
        elif widget == "phrase_entry" and self.phrase_entry.get() == "Enter the phrase":
            self.phrase_entry.delete(0, "end")
        elif widget == "index_entry" and self.index_entry.get() == "number or delete last":
            self.index_entry.delete(0, "end")

    def focus_EntryWord_out(self, event, widget):
        if widget == "word_entry" and self.word_entry.get() == "":
            self.word_entry.delete(0, "end")
            self.word_entry.insert(0, "Enter the word")
        elif widget == "translate_entry" and self.translate_entry.get() == "":
            self.translate_entry.delete(0, "end")
            self.translate_entry.insert(0, "Enter the translate")
        elif widget == "phrase_entry" and self.phrase_entry.get() == "":
            self.phrase_entry.delete(0, "end")
            self.phrase_entry.insert(0, "Enter the phrase")
        elif widget == "index_entry" and self.index_entry.get() == "":
            self.index_entry.delete(0, "end")
            self.index_entry.insert(0, "number or delete last")

    def add_word(self):
        word = self.word_entry.get().lower()
        translate = self.translate_entry.get().lower()
        phrase = self.phrase_entry.get().lower()

        if word != "" and word != "enter the word" and translate != "" and translate != "enter the translate" and phrase != "" and phrase != "enter the phrase":
            new_word = {'English': word, 'Translate': translate, 'Phrase': phrase}
            self.words_dict.append(new_word)
            updated_all_words = pd.DataFrame(self.words_dict)
            updated_all_words.to_csv("data.csv", index=False)
            self.remove_widgets()
            self.create_widgets()
        else:
            messagebox.showerror(title="empty field", message="Error: empty field")

    def delete_word(self):
        try:
            index = self.index_entry.get()
            if index == "number or delete last":
                last_index = len(self.words_dict)-1
                self.words_dict.pop(last_index)
            else:
                self.words_dict.pop(int(index)-1)

            updated_words = pd.DataFrame(self.words_dict)
            updated_words.to_csv("data.csv", index=False)
            self.remove_widgets()
            self.create_widgets()
        except:
            messagebox.showerror(title="field error", message="Error: write number or no such word")

    def edit_word(self):
        self.count_edit_btn += 1
        if self.count_edit_btn == 1:
            self.index = int(self.index_entry.get())-1
            word = self.words_dict[self.index]["English"]
            translate = self.words_dict[self.index]["Translate"]
            phrase = self.words_dict[self.index]["Phrase"]

            self.word_entry.delete(0, "end")
            self.translate_entry.delete(0, "end")
            self.phrase_entry.delete(0, "end")

            self.word_entry.insert(0, word)
            self.translate_entry.insert(0, translate)
            self.phrase_entry.insert(0, phrase)

        elif self.count_edit_btn == 2:
            word = self.word_entry.get().lower()
            translate = self.translate_entry.get().lower()
            phrase = self.phrase_entry.get().lower()
            if word != "" and translate != "" and phrase != "":
                self.words_dict[self.index]["English"] = word
                self.words_dict[self.index]["Translate"] = translate
                self.words_dict[self.index]["Phrase"] = phrase
                updated_words = pd.DataFrame(self.words_dict)
                updated_words.to_csv("data.csv", index=False)
            else:
                messagebox.showerror(title="field error", message="Error: empty field")
            self.count_edit_btn = 0
            self.remove_widgets()
            self.create_widgets()
    def remove_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()
