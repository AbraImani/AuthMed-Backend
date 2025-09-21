from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from .database import Base
import datetime
import enum

class AnalysisStatus(str, enum.Enum):
    # énumération pour le statut du diagnostic
    AUTHENTIQUE = "Authentique"
    SUSPECT = "Suspect"
    CONTREFAIT = "Contrefait"

class Medicament(Base):
    """
    Modèle pour la table de référence des médicaments.
    Contient les informations officielles sur chaque médicament.
    """
    __tablename__ = "medicaments"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True, nullable=False)
    code_barres = Column(String, unique=True, nullable=False)
    # Dans un cas réel, ce serait un chemin vers une image du logo officiel, 
    # ce qui est à implementer dans analysis_module.py
    logo_path = Column(String, nullable=True) 
    # Données attendues dans le QR code (de même)
    qr_code_data = Column(String, unique=True, nullable=True)

class Log(Base):
    """
    Modèle pour la table de journalisation (logs).
    Enregistre chaque tentative de scan pour la traçabilité.
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    image_hash = Column(String, unique=True, nullable=False, index=True)
    result_status = Column(Enum(AnalysisStatus), nullable=False)
    result_message = Column(String, nullable=False)
    # Optionnel: pourrait être enrichi avec des données GPS qui sont des données externes
    location = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Clé étrangère vers le médicament de référence si une correspondance a été trouvée
    matched_medicament_id = Column(Integer, ForeignKey("medicaments.id"), nullable=True)

