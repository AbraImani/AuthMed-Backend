from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from . import crud, models, schemas

def mock_analyze_image(image_path: str, db: Session) -> Dict[str, Any]:
    extracted_code = "8901234123457" # Code-barres pour "Paracétamol 500mg"
    print(f"Code extrait (simulé) de l'image : {extracted_code}")

    # Recherche du médicament correspondant dans notre base de référence
    medicament_ref = crud.get_medicament_by_code(db, code=extracted_code)

    if medicament_ref:
        # Si une correspondance est trouvée, le médicament est considéré authentique
        return {
            "status": models.AnalysisStatus.AUTHENTIQUE,
            "message": f"Médicament identifié comme '{medicament_ref.nom}'. Correspondance trouvée dans la base de référence.",
            "matched_medicament": medicament_ref
        }
    else:
        # Si aucune correspondance n'est trouvée, le médicament est suspect
        return {
            "status": models.AnalysisStatus.SUSPECT,
            "message": f"Le code '{extracted_code}' ne correspond à aucun médicament connu dans notre base. La prudence est recommandée.",
            "matched_medicament": None
        }

    # On pourrait ajouter une logique pour le statut "CONTREFAIT" si un modèle
    # détectait des anomalies visuelles spécifiques (ex: police, couleur, etc.)
