import pandas as pd
import random
from tkinter import *

class CheckWords:
    def init_dict(self, current_dict, type_dict, type_test):
        words = pd.read_csv(current_dict)
        self.words_dict = words.to_dict(orient="records")
        self.type_dict = type_dict
        self.type_test = type_test
        return len(self.words_dict)

    def make_word(self):
        try:
            whole_word = random.choice(self.words_dict)
        except:
            return False
        self.click = 0
        #print(whole_word)
        self.words_dict.remove(whole_word)

        return whole_word

    def check_word(self, entry_widget, word, translate, phrase):
        self.click += 1
        text = entry_widget.get().lower()

        #first type dict
        if self.type_dict == 0:
            # word - > translate
            if self.type_test == 0 and text == translate:
                return True
            # traslate - > word
            elif self.type_test == 1 and text == word:
                return True
            else:
                return False
        
        #second type dict
        elif self.type_dict == 1:
                # for first and second type we ask "phrase" at first
                if self.type_test == 0 and text == phrase and self.click == 1 or self.type_test == 1 and text == phrase and self.click == 1:
                    return True
                # first type 2 stage
                elif self.type_test == 0 and text == translate and self.click == 2:
                    return True
                # second type 2 stage
                elif self.type_test == 1 and text == word and self.click == 2:
                    return True
                else:
                    return False
                

