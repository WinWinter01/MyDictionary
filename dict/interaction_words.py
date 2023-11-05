import pandas as pd

class EditWords():

    def add_word(self, word_entry, translate_entry, phrase_entry):
        words = pd.read_csv("data.csv")
        words_dict = words.to_dict(orient="records")

        word = word_entry.get().lower()
        translate = translate_entry.get().lower()
        phrase = phrase_entry.get().lower()

        if word != "" and word != "enter the word" and translate != "" and translate != "enter the translate" and phrase != "" and phrase != "enter the phrase":
            new_word = {'Word': word, 'Translate': translate, 'Phrase': phrase}
            words_dict.append(new_word)
            updated_words = pd.DataFrame(words_dict)
            updated_words.to_csv("data.csv", index=False)
            return [(len(words_dict)), word, translate, phrase]
        else:
            return False     
                            
    def delete_word(self, selected_item):
        words = pd.read_csv("data.csv")
        words_dict = words.to_dict(orient="records")
        if selected_item:
            words_dict.pop(int(selected_item[0]))
            Specific_word = "Specific_word"
        else:
            index = len(words_dict)-1
            words_dict.pop(index)
            Specific_word = index
        
        
        updated_words = pd.DataFrame(words_dict)
        updated_words.to_csv("data.csv", index=False)

        return Specific_word
    
    def edit_word(self, selected_item, clicks=None, word_entry=None, translate_entry=None, phrase_entry=None):
        words = pd.read_csv("data.csv")
        words_dict = words.to_dict(orient="records")
        index_word = int(selected_item[0])
        word = words_dict[index_word]

        if clicks == 0:
            return word
        elif clicks == 1:
            word = word_entry.get().lower()
            translate = translate_entry.get().lower()
            phrase = phrase_entry.get().lower()
            changed_word = {'Word': word, 'Translate': translate, 'Phrase': phrase}
            if word != "" and word != "enter the word" and translate != "" and translate != "enter the translate" and phrase != "" and phrase != "enter the phrase":
                words_dict[index_word] = changed_word
            return (word, translate, phrase)
