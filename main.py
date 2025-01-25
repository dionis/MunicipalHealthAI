from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


SQLALCHEMY_DATABASE_URL = "postgresql://admin:cadmin@localhost/Gestion-Embarazadas"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


Base = declarative_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Prediccion(Base):
    __tablename__ = 'predicciones'
    
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    last_menstrual_date = Column(Date)
    cycle_length = Column(Integer)
    estimated_due_date = Column(Date)

Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Predicción de Embarazo</title>
        <style>
            body {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            h1 {
                color: #1e6a5a;
            }
            input[type="text"], input[type="date"] {
                padding: 10px;
                font-size: 16px;
                margin: 10px;
                width: 80%;
                max-width: 300px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>Predicción de Embarazo</h1>
        <form action="/predict/" method="post">
            <label for="age">Edad:</label>
            <input type="text" id="age" name="age" required><br>
            <label for="last_menstrual_date">Última Fecha Menstrual:</label>
            <input type="date" id="last_menstrual_date" name="last_menstrual_date" required><br>
            <label for="cycle_length">Duración del Ciclo Menstrual (en días):</label>
            <input type="text" id="cycle_length" name="cycle_length" required><br>
            <button type="submit">Predecir</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/predict/")
async def predict(age: str = Form(...), last_menstrual_date: str = Form(...), cycle_length: str = Form(...), db: Session = Depends(get_db)):
    try:
       
        age = int(age)
        cycle_length = int(cycle_length)
        last_menstrual_date = datetime.strptime(last_menstrual_date, "%Y-%m-%d")

       
        estimated_due_date = last_menstrual_date + timedelta(weeks=40)

        
        prediccion = Prediccion(
            age=age,
            last_menstrual_date=last_menstrual_date,
            cycle_length=cycle_length,
            estimated_due_date=estimated_due_date
        )
        db.add(prediccion)
        db.commit()
        db.refresh(prediccion)

        return JSONResponse(content={
            "message": "Predicción guardada en la base de datos",
            "estimated_due_date": estimated_due_date.strftime("%Y-%m-%d"),
            "age": age,
            "cycle_length": cycle_length,
            "last_menstrual_date": last_menstrual_date.strftime("%Y-%m-%d")
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
