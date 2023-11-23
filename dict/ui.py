import pandas as pd
import textwrap
import os
from tkinter import *
from tkinter import ttk, font

class Interface:
    def __init__(self, edits, test):
        self.edits = edits
        self.test = test

        self.count_test = 0
        self.FOLDER_PASS = "dictionaries"
        self.CURRENT_DICT_PATH = None
        self.type_dict = None

        self.window = Tk()
        self.window.geometry("1300x700")
        self.window.wm_geometry(f"{1020}x{700}+{0}+{0}")
        self.window.config(bg="grey")

        self.ui_dicts()

        self.window.mainloop()

    def ui_dicts(self):
        
        font_list_dicts = font.Font(size=30)
        self.count_add_dict = 0
        self.count_test = 0
        self.dicts_list = Listbox(font=font_list_dicts, width=30, height=10)

        files = os.listdir(self.FOLDER_PASS)
        count = 0
        # Output list of files
        for file in files:
            count+=1
            self.dicts_list.insert(count, file)


        self.AddDict_btn = Button(text="Add Dict", command=self.add_dict)
        
        self.selected_option_var = StringVar()
        self.selected_option_var.set(None)
        self.type_check_1 = Radiobutton(text="WORD/TRANSLATE", variable=self.selected_option_var, value=0)
        self.type_check_2 = Radiobutton(text="WORD/TRANSLATE/PHRASE", variable=self.selected_option_var, value=1)

        self.dicts_list.pack()
        self.AddDict_btn.pack()
        self.type_check_1.pack()
        self.type_check_2.pack()

        self.dicts_list.bind('<ButtonRelease-1>', self.on_listbox_select)

    def on_listbox_select(self, event):
        # loading chosen file
        selected_index = self.dicts_list.curselection()
        if selected_index:
            selected_item = self.dicts_list.get(selected_index)
            
            self.CURRENT_DICT_PATH = f"{self.FOLDER_PASS}/{selected_item}"
            words = pd.read_csv(self.CURRENT_DICT_PATH)
            words_dict = words.to_dict(orient="records")

            if len(words_dict[0]) == 2:
                self.type_dict = 0
            elif len(words_dict[0]) == 3:
                self.type_dict = 1

            self.clear_widgets()
            self.display_widgets()
    
    def add_dict(self):
        self.count_add_dict+=1
        if self.count_add_dict == 1:
            self.dict_entry = Entry()
            self.dict_entry.pack()
        elif self.count_add_dict == 2:
            name = self.dict_entry.get().lower()
            self.type_dict = int(self.selected_option_var.get())

            with open(f"{self.FOLDER_PASS}/{name}.csv", 'w') as handle:
                if self.type_dict == 0:
                    dict_sample = {"Word":["apple"],"Translate":["яблоко"]}
                elif self.type_dict == 1:
                    dict_sample = {"Word":["apple"],"Translate":["яблоко"],"Phrase":["I like apples"]}
                
                df = pd.DataFrame(dict_sample)
                df.to_csv(f"{self.FOLDER_PASS}/{name}.csv", index=False)
                
            self.count_add_dict == 0
            self.clear_widgets()
            self.ui_dicts()
                
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
        if self.type_dict == 1:
            self.tree.heading("Phrase", text="Phrase", anchor=W)

        self.count_words_main = self.insert_treeview()
        self.tree.grid(column=0, row=0, pady=20, stick='', padx=20, columnspan=4)
         
        # btn add
        self.addWord_btn = Button(text="Add Word", command=self.add_pressed)
        self.addWord_btn.grid(column=0, row=1, stick='e', padx=50, pady=5, columnspan=2)
        #self.add_clicks = 0
        self.window.bind('<Return>', self.add_pressed)

        # btn delete
        self.DeleteWord_btn = Button(text="Delete Word", command=self.delete_pressed)
        self.DeleteWord_btn.grid(column=1, row=1, stick='', padx=5, pady=5, columnspan=2)

        # btn edit
        self.EditWord_btn = Button(text="Edit Word", command=self.edit_pressed)
        self.EditWord_btn.grid(column=2, row=1, stick='w', padx=50, pady=5, columnspan=2)
        self.clicks = 0

        # btn menu
        self.Menu_btn = Button(text="Menu", command=self.return_to_menu)
        self.Menu_btn.grid(column=3, row=1, stick='w', padx=50, pady=5, columnspan=2)

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
        if self.type_dict == 1:
            self.phrase_entry = Entry()
            self.phrase_entry.grid(column=3, row=2, stick='', padx=5, pady=5)
            self.phrase_entry.insert(0, "Enter the phrase")
            self.phrase_entry.bind("<FocusIn>", lambda event: self.focus_on(self.phrase_entry, "Enter the phrase"))
            self.phrase_entry.bind("<FocusOut>", lambda event: self.focus_out(self.phrase_entry, "Enter the phrase"))
        elif self.type_dict == 0:
            self.phrase_entry = None

        # test btn
        self.DeleteWord_btn = Button(text="Test", command=self.test_pressed)
        self.DeleteWord_btn.grid(column=0, row=3, stick='', padx=5, pady=5, columnspan=2)
        
        self.selected_option_var_test = StringVar()
        self.selected_option_var_test.set(None)
        self.typeTest_check_1 = Radiobutton(text="WORD -> TRANSLATE / PHRASE", variable=self.selected_option_var_test, value=0)
        self.typeTest_check_2 = Radiobutton(text="TRANSLATE - > WORD / PHRASE", variable=self.selected_option_var_test, value=1)
        self.typeTest_check_1.grid(column=0, row=4, stick='', padx=5, pady=5, columnspan=2)
        self.typeTest_check_2.grid(column=1, row=4, stick='', padx=5, pady=5, columnspan=2)

        self.count_widget_main = Label()
        self.count_widget_main.grid(column=1, row=3, stick='', padx=5, pady=5, columnspan=2)
        self.count_widget_main.config(text=f"{self.count_test}/{self.count_words_main}")

    def insert_treeview(self):
        words = pd.read_csv(self.CURRENT_DICT_PATH)
        words_dict = words.to_dict(orient="records")
        count = 0
        for i in words_dict:
            if self.type_dict == 0:
                self.tree.insert(parent='', index='end', iid=str(count), text=str(count + 1),
                            values=(str(i["Word"]), str(i["Translate"])))
            elif self.type_dict == 1:
                self.tree.insert(parent='', index='end', iid=str(count), text=str(count + 1),
                            values=(str(i["Word"]), str(i["Translate"]), '\n'.join(textwrap.wrap(str(i["Phrase"]), 49))))
        
            count += 1
        return count

    def add_pressed(self, event=None):
        word_inf = self.edits.add_word(self.CURRENT_DICT_PATH, self.word_entry, self.translate_entry, self.phrase_entry)
        if word_inf:
            self.clear_widgets()
            self.display_widgets()

    def delete_pressed(self):
        selected_item = self.tree.selection()
        Specific_word = self.edits.delete_word(self.CURRENT_DICT_PATH, selected_item)
        self.clear_widgets()
        if Specific_word == True:
            self.display_widgets()
        else:
            self.ui_dicts()

    def edit_pressed(self):
        selected_item = self.tree.selection()
    
        if self.clicks == 0:
            word = self.edits.edit_word(selected_item, self.CURRENT_DICT_PATH, self.clicks)
            self.word_entry.delete(0, "end")
            self.word_entry.insert(0, word["Word"]) 
            self.translate_entry.delete(0, "end")
            self.translate_entry.insert(0, word["Translate"])
            if self.type_dict == 1: 
                self.phrase_entry.delete(0, "end")
                self.phrase_entry.insert(0, word["Phrase"]) 
            self.clicks += 1
        elif self.clicks == 1:
            word = self.edits.edit_word(selected_item, self.CURRENT_DICT_PATH, self.clicks, self.word_entry, self.translate_entry, self.phrase_entry)
            #self.tree.item(selected_item, values=word)
            self.clicks = 0
            self.clear_widgets()
            self.display_widgets()

    def return_to_menu(self):
        self.clear_widgets()
        self.ui_dicts()



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
        self.clear_widgets()
        self.window.bind('<Return>', self.test_check_word)
        self.type_test = int(self.selected_option_var_test.get())

        self.count_test = 0
        self.clicks_type2_test = 0

        self.label_widget = Label(width=40, height=10)
        self.label_widget.pack(padx=10, pady=10)

        self.entry_widget = Entry()
        self.entry_widget.pack(padx=10, pady=10)
        
        self.button_widget = Button(text="push", command=self.test_check_word)
        self.button_widget.pack()

        self.count_words = self.test.init_dict(self.CURRENT_DICT_PATH, self.type_dict, self.type_test)
        self.count_widget = Label(width=40, height=10)
        self.count_widget.pack(padx=10, pady=10)

        
        self.count_widget.config(text=f"{self.count_test}/{self.count_words}")
        self.count_widget.pack()
        
        self.test_new_word()

    def test_new_word(self):
        text = self.test.make_word()
        
        if text == False:
            self.clear_widgets()
            self.display_widgets()
        else:
            self.word_to_check = text["Word"]
            self.translate_to_check = text["Translate"]
            if self.type_dict == 1:
                self.phrase_to_check = text["Phrase"]
            else:
                self.phrase_to_check = None

            if self.type_test == 0:
                self.label_widget.config(text=text["Word"])
            elif self.type_test == 1:
                self.label_widget.config(text=text["Translate"])

    def test_check_word(self, event=None):
        answer = self.test.check_word(self.entry_widget, self.word_to_check, self.translate_to_check, self.phrase_to_check)
        self.clicks_type2_test+=1
        self.entry_widget.delete(0, END)
        try:
            self.Tru_answer_widget.destroy()
        except:
            None
        if self.type_dict == 0:
            if answer == True:
                self.count_test += 1
                self.count_widget.config(text=f"{self.count_test}/{self.count_words}")
                self.window.configure(bg="#32CD32")
                self.window.after(500, self.back_color) 
                self.test_new_word()
            else:
                self.Tru_answer_widget = Label(width=40, height=10)
                self.Tru_answer_widget.pack(padx=10, pady=10)
                self.Tru_answer_widget.config(text=f"{self.word_to_check} - {self.translate_to_check}") 
                self.window.configure(bg="#FF0000")
                self.window.after(500, self.back_color)
                self.test_new_word()

        elif self.type_dict == 1:
            if answer == True and self.clicks_type2_test == 1:
                self.window.configure(bg="#32CD32")
                self.window.after(500, self.back_color) 
            elif answer == True and self.clicks_type2_test == 2:
                self.count_test += 1
                self.clicks_type2_test = 0
                self.count_widget.config(text=f"{self.count_test}/{self.count_words}")
                self.window.configure(bg="#32CD32")
                self.window.after(500, self.back_color)
                self.test_new_word()
            elif answer == False:
                self.Tru_answer_widget = Label(width=40, height=10)
                self.Tru_answer_widget.pack(padx=10, pady=10)
                self.Tru_answer_widget.config(text=f"{self.phrase_to_check} - {self.word_to_check} - {self.translate_to_check}") 
                self.clicks_type2_test = 0
                self.window.configure(bg="#FF0000")
                self.window.after(500, self.back_color)	
                self.test_new_word()

    def clear_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def back_color(self):
        self.window.config(bg="grey")
