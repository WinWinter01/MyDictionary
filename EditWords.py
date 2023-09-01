from tkinter import messagebox
from MainMenu import MainMenu
import pandas as pd

class EditWords(MainMenu):
    def __init__(self, window):
        self.window = window
    def add_word(self):
        print(1)
        super().__init__(self.window)
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

