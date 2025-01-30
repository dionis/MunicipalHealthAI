from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from datetime import datetime, timedelta
import psycopg2
from typing import List
import pandas as pd

app = FastAPI()

# Conexión a la base de datos PostgreSQL
def conectar_db():
    return psycopg2.connect(
        dbname="Gestion-Embarazadas",
        user="admin",
        password="admin",
        host="localhost"
    )

# Modelo de datos para predicción
class PrediccionInput(BaseModel):
    fecha_ultima_menstruacion: str
    duracion_periodo: int
    talla: float
    peso: float
    edad_gestacional: int
    presiones: List[float]
    antecedentes: str

# Funciones IA 
def calcular_fecha_parto(fecha_ultima_menstruacion, duracion_periodo):
    fecha_ultima_menstruacion = datetime.strptime(fecha_ultima_menstruacion, '%Y-%m-%d')
    fecha_parto = fecha_ultima_menstruacion + timedelta(days=(280 - duracion_periodo))
    return fecha_parto.strftime('%Y-%m-%d')

def evaluar_riesgos(presiones, antecedentes):
    riesgo = 'bajo'
    for presion in presiones:
        if presion > 140:
            riesgo = 'alto'
            break
    if 'diabetes' en antecedentes.lower():
        riesgo = 'alto'
    return riesgo

def evaluar_peso(talla, peso, edad_gestacional):
    peso_ideal = 50 + 0.9 * (talla - 150)
    diferencia_peso = peso - peso_ideal
    if diferencia_peso > 5:
        return "Sobrepeso"
    elif diferencia_peso < -5:
        return "Bajo peso"
    else:
        return "Peso normal"

@app.post("/prediccion/")
async def prediccion(input: PrediccionInput):
    try:
        fecha_parto = calcular_fecha_parto(input.fecha_ultima_menstruacion, input.duracion_periodo)
        riesgo = evaluar_riesgos(input.presiones, input.antecedentes)
        peso_evaluacion = evaluar_peso(input.talla, input.peso, input.edad_gestacional)

        # Conexión a la base de datos para guardar información
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predicciones (fecha_entrada, usuario, fecha_parto, riesgo, peso_evaluacion)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), 'usuario', fecha_parto, riesgo, peso_evaluacion))
        conn.commit()
        conn.close()

        return {
            "fecha_parto": fecha_parto,
            "riesgo": riesgo,
            "peso_evaluacion": peso_evaluacion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Crear tabla 
def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predicciones (
            id SERIAL PRIMARY KEY,
            fecha_entrada TIMESTAMP,
            usuario VARCHAR(100),
            fecha_parto DATE,
            riesgo VARCHAR(50),
            peso_evaluacion VARCHAR(50)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_tablas()

# Servicio para procesamiento de Excel
@app.post