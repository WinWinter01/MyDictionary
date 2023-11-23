import pandas as pd
import os

class EditWords():

    def add_word(self, path_dict, word_entry, translate_entry, phrase_entry=None):
        words = pd.read_csv(path_dict)
        words_dict = words.to_dict(orient="records")

        word = word_entry.get().lower()
        translate = translate_entry.get().lower()
        if phrase_entry != None:
            phrase = phrase_entry.get().lower()
        else:
            phrase = None
        if word != "" and word != "enter the word" and translate != "" and translate != "enter the translate":
            if phrase != "" and phrase != "enter the phrase" and phrase != None:
                new_word = {'Word': word, 'Translate': translate, 'Phrase': phrase}
            else:
                new_word = {'Word': word, 'Translate': translate}
            words_dict.append(new_word)
            updated_words = pd.DataFrame(words_dict)
            updated_words.to_csv(path_dict, index=False)
            return True
        else:
            return False     
                            
    def delete_word(self, path_dict, selected_item):
        words = pd.read_csv(path_dict)
        words_dict = words.to_dict(orient="records")
        if selected_item:
            words_dict.pop(int(selected_item[0]))
        else:
            index = len(words_dict)-1
            words_dict.pop(index)
        
        if len(words_dict) == 0:
            os.remove(path_dict)
            return False
        else:
            updated_words = pd.DataFrame(words_dict)
            updated_words.to_csv(path_dict, index=False)
            return True
    
    def edit_word(self, selected_item, path, clicks=None, word_entry=None, translate_entry=None, phrase_entry=None):
        words = pd.read_csv(path)
        words_dict = words.to_dict(orient="records")
        index_word = int(selected_item[0])
        word = words_dict[index_word]
        
        if clicks == 0:
            return word
        elif clicks == 1:
            word = word_entry.get().lower()
            translate = translate_entry.get().lower()
            if phrase_entry != None:
                phrase = phrase_entry.get().lower()
            else:
                phrase = None

            if word != "" and word != "enter the word" and translate != "" and translate != "enter the translate":
                if phrase != None and phrase != "" and phrase != "enter the phrase":
                    changed_word = {'Word': word, 'Translate': translate, 'Phrase': phrase}
                    
                elif phrase == None:
                    changed_word = {'Word': word, 'Translate': translate}
            
            words_dict[index_word] = changed_word
            updated_words = pd.DataFrame(words_dict)
            updated_words.to_csv(path, index=False)
            return (word, translate, phrase)

