from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db
from .image_processor import calculate_hash, preprocess_image
# Mise à jour pour utiliser la nouvelle fonction d'analyse
from .analysis_module import analyze_image_with_model

router = APIRouter()

@router.post("/scan", response_model=schemas.AnalysisResponse)
async def scan_medicament_image(db: Session = Depends(get_db), file: UploadFile = File(...)):
    """
    Endpoint principal pour l'analyse d'une image de médicament.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier fourni n'est pas une image.")

    image_bytes = await file.read()
    
    image_hash = calculate_hash(image_bytes)

    try:
        processed_image_path = preprocess_image(image_bytes, image_hash)
        
        # Appel à la nouvelle fonction qui utilise le modèle ML
        analysis_result = analyze_image_with_model(processed_image_path, db)
        
        log_entry = schemas.LogCreate(
            image_hash=image_hash,
            result_status=analysis_result["status"],
            result_message=analysis_result["message"],
            matched_medicament_id=None # La classification ne renvoie pas d'ID de médicament
        )
        created_log = crud.create_log(db, log=log_entry)

        return schemas.AnalysisResponse(
            status=analysis_result["status"],
            message=analysis_result["message"],
            log_id=created_log.id,
            matched_medicament=None
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur interne est survenue: {e}")

