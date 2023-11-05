import pandas as pd
import textwrap
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self, edits, test):
        self.edits = edits
        self.test = test

        self.count_test = 0

        self.window = Tk()
        self.window.geometry("1300x700")
        self.window.wm_geometry(f"{1020}x{700}+{0}+{0}")
        self.window.config(bg="grey")

        self.display_widgets()

        self.window.mainloop()

    def display_widgets(self):
        self.window.bind("<Tab>", self.select_next_widget)
        self.window.bind("<Return>", self.on_enter)
    
        self.tree = ttk.Treeview()

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

        self.count_words_main = self.insert_treeview()
        self.tree.grid(column=0, row=0, pady=20, stick='', padx=20, columnspan=4)
        
        # btn add
        self.addWord_btn = Button(text="Add Word", command=self.add_pressed)
        self.addWord_btn.grid(column=0, row=1, stick='e', padx=50, pady=5, columnspan=2)
        self.add_clicks = 0

        # btn delete
        self.DeleteWord_btn = Button(text="Delete Word", command=self.delete_pressed)
        self.DeleteWord_btn.grid(column=1, row=1, stick='', padx=5, pady=5, columnspan=2)

        # btn edit
        self.EditWord_btn = Button(text="Edit Word", command=self.edit_pressed)
        self.EditWord_btn.grid(column=2, row=1, stick='w', padx=50, pady=5, columnspan=2)
        self.clicks = 0

        # word entry
        self.word_entry = Entry()
        self.word_entry.grid(column=1, row=2, stick='', padx=5, pady=5)
        self.word_entry.insert(0, "Enter the word")
        self.word_entry.bind("<FocusIn>", lambda event: self.focus_on(self.word_entry, "Enter the word"))
        self.word_entry.bind("<FocusOut>", lambda event: self.focus_out(self.word_entry, "Enter the word"))

        # translate entry
        self.translate_entry = Entry()
        self.translate_entry.grid(column=2, row=2, stick='', padx=5, pady=5)
        self.translate_entry.insert(0, "Enter the translate")
        self.translate_entry.bind("<FocusIn>", lambda event: self.focus_on(self.translate_entry, "Enter the translate"))
        self.translate_entry.bind("<FocusOut>", lambda event: self.focus_out(self.translate_entry, "Enter the translate"))

        # phrase entry
        self.phrase_entry = Entry()
        self.phrase_entry.grid(column=3, row=2, stick='', padx=5, pady=5)
        self.phrase_entry.insert(0, "Enter the phrase")
        self.phrase_entry.bind("<FocusIn>", lambda event: self.focus_on(self.phrase_entry, "Enter the phrase"))
        self.phrase_entry.bind("<FocusOut>", lambda event: self.focus_out(self.phrase_entry, "Enter the phrase"))

        # test btn
        self.DeleteWord_btn = Button(text="Test", command=self.test_pressed)
        self.DeleteWord_btn.grid(column=0, row=3, stick='', padx=5, pady=5, columnspan=2)
        
        self.count_widget_main = Label()
        self.count_widget_main.grid(column=1, row=3, stick='', padx=5, pady=5, columnspan=2)
        self.count_widget_main.config(text=f"{self.count_test}/{self.count_words_main}")

    def insert_treeview(self):
        words = pd.read_csv("data.csv")
        words_dict = words.to_dict(orient="records")
        count = 0
        for i in words_dict:
            self.tree.insert(parent='', index='end', iid=str(count), text=str(count + 1),
                        values=(str(i["Word"]), str(i["Translate"]), '\n'.join(textwrap.wrap(str(i["Phrase"]), 49))))
            count += 1
        return count

    def add_pressed(self):
        self.add_clicks = 0
        word_inf = self.edits.add_word(self.word_entry, self.translate_entry, self.phrase_entry)
        if word_inf:
            self.clear_entryes_field()
            self.tree.insert(parent='', index='end', iid=str(word_inf[0]-1), text=str(word_inf[0]),
                        values=(str(word_inf[1]), str(word_inf[2]), '\n'.join(textwrap.wrap(str(word_inf[3]), 49))))

    def delete_pressed(self):
        selected_item = self.tree.selection()
        Specific_word = self.edits.delete_word(selected_item)

        if Specific_word == "Specific_word":
            self.tree.delete(selected_item)
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.insert_treeview()

    def edit_pressed(self):
        selected_item = self.tree.selection()
    
        if self.clicks == 0:
            word = self.edits.edit_word(selected_item, self.clicks)
            self.word_entry.delete(0, "end")
            self.word_entry.insert(0, word["Word"]) 
            self.translate_entry.delete(0, "end")
            self.translate_entry.insert(0, word["Translate"]) 
            self.phrase_entry.delete(0, "end")
            self.phrase_entry.insert(0, word["Phrase"]) 
            self.clicks += 1
        elif self.clicks == 1:
            word = self.edits.edit_word(selected_item, self.clicks, self.word_entry, self.translate_entry, self.phrase_entry)
            self.tree.item(selected_item, values=word)
            self.clicks = 0
            self.word_entry.delete(0, "end")
            self.translate_entry.delete(0, "end")
            self.phrase_entry.delete(0, "end")

    def clear_entryes_field(self):
        self.word_entry.delete(0, END)
        self.translate_entry.delete(0, END)
        self.phrase_entry.delete(0, END)
        self.word_entry.insert(0, "Enter the word")
        self.translate_entry.insert(0, "Enter the translate")
        self.phrase_entry.insert(0, "Enter the phrase")

    def focus_on(self, widget, text):
        if widget.get() == text:
            widget.delete(0, "end")
    
    def focus_out(self, widget, text, clear=False):
        if widget.get() == text or widget.get() == "" or clear == True:
            widget.delete(0, "end")
            widget.insert(0, text)

    def select_next_widget(self, event):
        current_focus = self.window.focus_get()
        next_focus = current_focus.tk_focusNext()
        next_focus.focus_set()

    def on_enter(self, event):
        try:
            self.window.focus_get().invoke()
        except:
            pass

    def test_pressed(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.label_widget = Label(width=40, height=10)
        self.label_widget.pack(padx=10, pady=10)

        self.entry_widget = Entry()
        self.entry_widget.pack(padx=10, pady=10)
        
        self.button_widget = Button(text="push", command=self.test_check_word)
        self.button_widget.pack()

        self.count_words = self.test.init_dict()

        self.count_widget = Label(width=40, height=10)
        self.count_widget.pack(padx=10, pady=10)
        self.count_test = 0
        self.count_widget.config(text=f"{self.count_test}/{self.count_words}")
        self.count_widget.pack()

        self.test_new_word()

    def test_new_word(self):
        text = self.test.make_word()
        if text == False:
            self.clear_test()
            self.display_widgets()
        else:
            self.label_widget.config(text=text)

    def test_check_word(self):
        answer = self.test.check_word(self.entry_widget)
        self.entry_widget.delete(0, END)
        if answer == 1:
            self.window.configure(bg="#32CD32")
            self.window.after(500, self.back_color)
        elif answer == 2:
            self.count_test += 1
            self.count_widget.config(text=f"{self.count_test}/{self.count_words}")
            self.window.configure(bg="#00FF00")
            self.window.after(500, self.back_color)
            self.test_new_word()
        elif answer == False:
            self.window.configure(bg="#FF0000")
            self.window.after(500, self.back_color)	
            self.test_new_word()

    def clear_test(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def back_color(self):
        self.window.config(bg="grey")
