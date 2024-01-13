from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from .crud.CrudDictionary import CrudDictionary
from .models.Translate import Translate
from .schemas.DictEntry import DictEntry, Lines
from .database.database import engine
from .database.table import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


# page par defaut
@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.post("/dict/create_dict")
def add_dict(dict_entry: DictEntry):
    # on ajoute un dictionnaire
    crud_dict = CrudDictionary()
    try:
        new_dict = crud_dict.create_dict(dict_entry)
        return f"Le dictionnaire {new_dict.name} a été créé avec succès !"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/trad/{dict}/{word}")
def translate_word(dict: str, word: str):
    # on traduit un mot
    try:
        trad = Translate(dict, word)
        trad_word = trad.translate_word()
        return {word + " = " + trad_word}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/dict/all_dict")
def get_all_dict():
    # on recupere tous les dictionnaires
    crud_dict = CrudDictionary()
    try:
        all_dict = crud_dict.get_all_dict()
        return all_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/line/dict_lines/{dict_name}")
def get_dict_lines(dict_name: str):
    # on recupere les lignes d'un dictionnaire
    crud_dict = CrudDictionary()
    try:
        dict_lines = crud_dict.get_dict_lines(dict_name)
        return dict_lines
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/dict/delete_dict/{dict_name}")
def delete_dict(dict_name: str):
    # on supprime un dictionnaire
    crud_dict = CrudDictionary()
    try:
        crud_dict.delete_dict(dict_name)
        return f"Le dictionnaire {dict_name} a été supprimé avec succès !"
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/dict/update_name_dict/{change_name}")
def update_name_dict(change_name: str, dict_name: str):
    # on modifie le nom d'un dictionnaire
    crud_dict = CrudDictionary()
    try:
        new_name = crud_dict.update_name_dict(change_name, dict_name)
        return f"Le dictionnaire {new_name} a été modifié avec succès !"
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/update_lines/{dict_name}")
def update_lines_dict(dict_name: str, dict_lines: List[Lines]):
    # on modifie un dictionnaire
    crud_dict = CrudDictionary()
    try:
        crud_dict.update_lines_dict(dict_name, dict_lines)
        return f"Les lignes {str(dict_lines)} du dictionnaire {dict_name} ont été modifié avec succès !"
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/delete_lines/{dict_name}")
def delete_lines_dict(dict_name: str, dict_lines: List[Lines]):
    # on supprime une ligne d'un dictionnaire
    crud_dict = CrudDictionary()
    try:
        crud_dict.delete_lines_dict(dict_name, dict_lines)
        return f"Les lignes {str(dict_lines)} ont été supprimé avec succès !"
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
