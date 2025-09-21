from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import AnalysisStatus

# Schémas pour Medicament
class MedicamentBase(BaseModel):
    nom: str
    code_barres: str
    logo_path: Optional[str] = None
    qr_code_data: Optional[str] = None

class MedicamentCreate(MedicamentBase):
    pass

class Medicament(MedicamentBase):
    id: int

    class Config:
        from_attributes = True

# Schémas pour Log
class LogBase(BaseModel):
    image_hash: str
    result_status: AnalysisStatus
    result_message: str
    location: Optional[str] = None
    matched_medicament_id: Optional[int] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


#Schémas pour la Réponse de l'API
class AnalysisResponse(BaseModel):

    status: AnalysisStatus
    message: str
    log_id: int
    # Inclut les détails du médicament trouvé s'il y en a un
    matched_medicament: Optional[Medicament] = None

