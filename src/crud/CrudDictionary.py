from typing import List

from ..database.database import SessionLocal
from ..database.table import Dictionary, DictionaryLines
from ..schemas.DictEntry import DictEntry, Lines


class CrudDictionary:

    def __init__(self):
        self.db = SessionLocal()

    def create_dict(self, dict_entry: DictEntry):
        try:
            # On ajoute le dictionnaire
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == dict_entry.name).first()
            if dictionary:
                raise Exception("Dictionnaire existe déja")

            new_dictionary = Dictionary(name=dict_entry.name)
            self.db.add(new_dictionary)
            self.db.commit()
            self.db.refresh(new_dictionary)

            # On ajoute les lines du dictionnaire
            for line in dict_entry.lines:
                new_line = DictionaryLines(dictionary_id=new_dictionary.id, char=line.key, value=line.value)
                self.db.add(new_line)

            # On envoie les changements
            self.db.commit()
            # On rafraichit la base de données pour avoir les données du dictionnaire (pour le return)
            self.db.refresh(new_dictionary)

            return new_dictionary

        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def get_all_dict(self):
        try:
            # On recupere tous les dictionnaires
            all_dict = self.db.query(Dictionary.name).all()
            all_names = [name[0] for name in all_dict]
            return all_names

        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def get_dict_lines(self, dict_name: str):
        try:
            # On recupere le dictionnaire et les lines
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == dict_name).first()
            if not dictionary:
                raise Exception("Dictionnaire non trouvé")

            dict_lines = self.db.query(DictionaryLines).filter(DictionaryLines.dictionary_id == dictionary.id).all()
            return dict_lines
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def delete_dict(self, dict_name: str):
        try:
            # On supprime le dictionnaire
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == dict_name).first()
            if not dictionary:
                raise Exception("Dictionnaire non trouvé")

            self.db.delete(dictionary)

            dict_lines = self.db.query(DictionaryLines).filter(DictionaryLines.dictionary_id == dictionary.id).all()
            for line in dict_lines:
                self.db.delete(line)

            self.db.commit()

        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def update_name_dict(self, change_name: str, dict_name: str):
        try:
            # On modifie le dictionnaire
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == change_name).first()
            if not dictionary:
                raise Exception("Dictionnaire non trouvé")

            dictionary.name = dict_name
            self.db.commit()
            self.db.refresh(dictionary)
            return dict_name

        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def update_lines_dict(self, dict_name: str, dict_lines: List[Lines]):
        try:
            # On modifie les lignes du dictionnaire
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == dict_name).first()
            if not dictionary:
                raise Exception("Dictionnaire non trouvé")

            for line in dict_lines:
                dict_line = self.db.query(DictionaryLines).filter(
                    DictionaryLines.dictionary_id == dictionary.id,
                    DictionaryLines.char == line.key
                ).first()

                if dict_line:
                    dict_line.value = line.value
                else:
                    new_line = DictionaryLines(dictionary_id=dictionary.id, char=line.key, value=line.value)
                    self.db.add(new_line)

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def delete_lines_dict(self, dict_name: str, dict_lines: List[Lines]):
        try:
            # On supprime les lignes du dictionnaire
            dictionary = self.db.query(Dictionary).filter(Dictionary.name == dict_name).first()
            if not dictionary:
                raise Exception("Dictionnaire non trouvé")

            for line in dict_lines:
                dict_line = self.db.query(DictionaryLines).filter(
                    DictionaryLines.char == line.key,
                    DictionaryLines.value == line.value
                ).first()

                if not dict_line:
                    raise Exception("Ligne non trouvée")
                else:
                    self.db.delete(dict_line)

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise
        finally:
            self.db.close()

