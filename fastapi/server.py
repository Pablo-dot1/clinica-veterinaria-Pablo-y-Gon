import shutil
import io
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List
from pydantic import BaseModel as PydanticBaseModel, Field
from routes import router  # Asegúrate de que 'routes.py' está en la misma carpeta

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Contrato(BaseModel):
    fecha: str
    centro_seccion: str
    nreg: str
    nexp: str
    objeto: str
    tipo: str
    procedimiento: str
    numlicit: str
    numinvitcurs: str
    proc_adjud: str
    presupuesto_con_iva: str
    valor_estimado: str
    importe_adj_con_iva: str
    adjuducatario: str
    fecha_formalizacion: str
    I_G: str

class ListadoContratos(BaseModel):
    contratos: List[Contrato] = Field(default_factory=list)

app = FastAPI(
    title="Servidor de datos",
    description="""Servimos datos de contratos, clientes, mascotas, citas y tratamientos.""",
    version="0.1.0",
)

@app.get("/retrieve_data/")
def retrieve_data():
    todosmisdatos = pd.read_csv('./contratos_inscritos_simplificado_2023.csv', sep=';')
    todosmisdatos = todosmisdatos.fillna(0)
    todosmisdatosdict = todosmisdatos.to_dict(orient='records')
    listado = ListadoContratos()
    listado.contratos = todosmisdatosdict
    return listado

class FormData(BaseModel):
    date: str
    description: str
    option: str
    amount: float

@app.post("/envio/")
async def submit_form(data: FormData):
    return {"message": "Formulario recibido", "data": data}

# Incluir las rutas de clientes, mascotas, citas y tratamientos
app.include_router(router)
