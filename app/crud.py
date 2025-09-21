from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas

# fonctions CRUD pour medicament
def get_medicament_by_code(db: Session, code: str) -> Optional[models.Medicament]:
    return db.query(models.Medicament).filter(
        (models.Medicament.code_barres == code) | (models.Medicament.qr_code_data == code)
    ).first()

def get_all_medicaments(db: Session):
    return db.query(models.Medicament).all()

def create_medicament(db: Session, medicament: schemas.MedicamentCreate) -> models.Medicament:
    db_medicament = models.Medicament(**medicament.dict())
    db.add(db_medicament)
    db.commit()
    db.refresh(db_medicament)
    return db_medicament

# fonctions CRUD pour log
def create_log(db: Session, log: schemas.LogCreate) -> models.Log:
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

