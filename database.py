from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost/Gestion-Embarazadas"

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