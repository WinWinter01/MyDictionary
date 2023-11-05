import pandas as pd
import random
from tkinter import *

class CheckWords:
    def init_dict(self):
        words = pd.read_csv("data.csv")
        self.words_dict = words.to_dict(orient="records")
        return len(self.words_dict)

    def make_word(self):
        try:
            whole_word = random.choice(self.words_dict)
        except:
            return False
        
        self.click = 0

        self.word = whole_word["Word"]
        self.translate = whole_word["Translate"]
        self.phrase = whole_word["Phrase"]


        self.words_dict.remove(whole_word)

        return self.word

    def check_word(self, entry_widget):
        self.click += 1
        text = entry_widget.get().lower()
        if self.phrase.lower() == text and self.click == 1 or self.translate.lower() == text and self.click == 2:
            return self.click
        else:
            return False