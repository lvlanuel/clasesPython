from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi import status, Depends

class Digimon(BaseModel):
    name: str
    tipo: str
    hp: int
    ataque: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Angel",
                    "tipo": "Aire",
                    "hp": 100,
                    "ataque": 5.5,
                }
            ]
        }
    }

class UpdateDigimon(BaseModel):
    id: int
    name: str
    tipo: str
    hp: int
    ataque: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id":1,
                    "name": "Angel",
                    "tipo": "Aire",
                    "hp": 100,
                    "ataque": 5.5,
                }
            ]
        }
    }

class ListDigimon(BaseModel):
    digimon: List[Digimon]