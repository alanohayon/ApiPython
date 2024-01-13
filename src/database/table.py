from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String(55), unique=True)

    dictionary = relationship("DictionaryLines", back_populates="dictionaryLines")


class DictionaryLines(Base):
    __tablename__ = 'dictionary_lines'

    id = Column(Integer, primary_key=True)
    dictionary_id = Column(Integer, ForeignKey('dictionary.id'))
    char = Column(String(1))
    value = Column(String(10))

    dictionaryLines = relationship("Dictionary", back_populates="dictionary")

# Traduction d'un mot à partir d'un dictionnaire
# @app.get("/{dict}/{word}")
# def translate_word(dict: str, word: str):
#     # On recupere le mot traduit grace à la fonction qui traduit le mot
#     tradWord = Translate(dict, word)
#     return tradWord.translate_word()