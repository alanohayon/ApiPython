from ..crud.CrudDictionary import CrudDictionary
class Translate:
    def __init__(self, dict, word):
        self.dict = dict
        self.word = word

    def translate_word(self):
        word = self.word
        dict = self.dict
        # On recupere les lignes du dictionnaire
        dict_lines = CrudDictionary().get_dict_lines(dict)

        trad = ""
        # On parcours le mot par caractere
        for char in word:
            for line in dict_lines:
                # si le caractere est le meme que la cle de la ligne en bdd
                if char == line.char:
                    trad += line.value
        return trad


