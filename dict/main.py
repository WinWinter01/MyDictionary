from ui import Interface
from interaction_words import EditWords
from test import CheckWords

test = CheckWords()
edits = EditWords()
dictionary = Interface(edits, test)