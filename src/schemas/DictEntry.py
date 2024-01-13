from typing import List
from pydantic import BaseModel


# Créer une class Lines qui represente le type des lignes d'un dictionnaire
class Lines(BaseModel):
    key: str
    value: str


# Dictionnaire qui contient la saisie du POST
class DictEntry(BaseModel):
    name: str
    lines: List[Lines]

