from typing import Union
from fastapi import FastAPI, File, UploadFile, Form
from fastapi import status, Depends
from app.schemas.digimon import Digimon, UpdateDigimon, ListDigimon
from app.config.database import Session, engine, Base
from app.models.digimon import Digimon as DigimonModel
from app.config.database import Session, engine, Base
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import JSONResponse, RedirectResponse
import base64

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/all_digimon", status_code=status.HTTP_200_OK, response_model=ListDigimon, tags=["Digimon"])
def get_all_Digimons():
    db = Session()
    result = db.query(DigimonModel).all()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontro data"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@app.get("/digimon/{id}", status_code=status.HTTP_200_OK, tags=["Digimon"], response_model=Digimon)
def get_digimon_id(id: int):
    db = Session()
    result = db.query(DigimonModel).filter(DigimonModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontro data"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Este endpoint permite subir un archivo de imagen, convertirlo a base64 y devolver la cadena resultante.
    """
    file_content = await file.read()

    encoded_image = base64.b64encode(file_content).decode('utf-8')
    return JSONResponse(content={"filename": file.filename, "image_base64": encoded_image})


@app.post("/create_digimon", status_code=status.HTTP_200_OK, response_model=Digimon, summary="Create a new Digimon", tags=["Digimon"])
def create_digimon(digimon: Digimon):
    db = Session()
    new_digimon = DigimonModel(name=digimon.name, tipo=digimon.tipo, hp=digimon.hp, ataque=digimon.ataque)
    db.add(new_digimon)
    db.commit()
    db.refresh(new_digimon)
    return new_digimon

@app.post("/create_digimon2", status_code=status.HTTP_200_OK, response_model=Digimon, summary="Create a new Digimon", tags=["Digimon"])
async def create_digimon2(
    file: UploadFile = File(...),  # Recibimos el archivo
    name: str = Form(...),         # Recibimos los datos del "JSON" como campos de formulario
    tipo: str = Form(...),
    hp: int = Form(...),
    ataque: float = Form(...)
):
    file_content = await file.read()
    encoded_image = base64.b64encode(file_content).decode('utf-8')
    db = Session()
    new_digimon = DigimonModel(
        name=name,
        tipo=encoded_image,
        hp=hp,
        ataque=ataque
    )
    db.add(new_digimon)
    db.commit()
    db.refresh(new_digimon)
    return new_digimon

@app.delete("/{id}", status_code=status.HTTP_200_OK, response_model=Digimon, tags=["Digimon"])
def delete_digimon(id: int):
    db = Session()
    result = db.query(DigimonModel).filter(DigimonModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontro data a eliminar"})
    result_return = result
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@app.get("/", status_code=status.HTTP_302_FOUND, include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

