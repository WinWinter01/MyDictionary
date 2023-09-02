import textwrap
import pandas as pd
from tkinter import messagebox
from CreateWidgets import CreateWidgets
from CreateWidgets import LENGHT_ROW
class EditWords(CreateWidgets):
    def insert_words_list(self):
        count = 0
        for i in self.words_dict:
            self.tree.insert(parent='', index='end', iid=str(count), text=str(count+1), values=(str(i["English"]), str(i["Translate"]), self.wrap(str(i["Phrase"]))))
            count += 1

    def wrap(self, string):
        return '\n'.join(textwrap.wrap(string, LENGHT_ROW))

    def select_next_widget(self, event):
        current_focus = self.window.focus_get()
        next_focus = current_focus.tk_focusNext()
        next_focus.focus_set()

    def on_enter(self, evnet):
        try:
            self.window.focus_get().invoke()
        except:
            pass

    def focus_on(self, event, widget):
        if widget == "word_entry" and self.word_entry.get() == "Enter the word":
            self.word_entry.delete(0, "end")
        elif widget == "translate_entry" and self.translate_entry.get() == "Enter the translate":
            self.translate_entry.delete(0, "end")
        elif widget == "phrase_entry" and self.phrase_entry.get() == "Enter the phrase":
            self.phrase_entry.delete(0, "end")
        elif widget == "index_entry" and self.index_entry.get() == "number or delete last":
            self.index_entry.delete(0, "end")

    def focus_out(self, event, widget):
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
            if index == "number or delete last" or index == "":
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
            try:
                self.index = int(self.index_entry.get())-1
                word = self.words_dict[self.index]["English"]
                translate = self.words_dict[self.index]["Translate"]
                phrase = self.words_dict[self.index]["Phrase"]
            except:
                self.count_edit_btn -= 1
                messagebox.showerror(title="field error", message="Error: empty field")
            else:
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
