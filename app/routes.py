from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db
from .image_processor import calculate_hash, preprocess_image
from .analysis_module import mock_analyze_image

router = APIRouter()

@router.post("/scan", response_model=schemas.AnalysisResponse)
async def scan_medicament_image(db: Session = Depends(get_db), file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier fourni n'est pas une image.")

    image_bytes = await file.read()
    
    # 1. Calculer le hash de l'image
    image_hash = calculate_hash(image_bytes)

    try:
        # 2. Prétraiter l'image
        processed_image_path = preprocess_image(image_bytes, image_hash)
        
        # 3. Analyser l'image (mock) et comparer avec la BDD
        analysis_result = mock_analyze_image(processed_image_path, db)
        
        # 4. Créer l'entrée pour le log
        log_entry = schemas.LogCreate(
            image_hash=image_hash,
            result_status=analysis_result["status"],
            result_message=analysis_result["message"],
            matched_medicament_id=analysis_result["matched_medicament"].id if analysis_result["matched_medicament"] else None
        )
        created_log = crud.create_log(db, log=log_entry)

        # 5. Préparer et retourner la réponse finale
        return schemas.AnalysisResponse(
            status=analysis_result["status"],
            message=analysis_result["message"],
            log_id=created_log.id,
            matched_medicament=analysis_result["matched_medicament"]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Gérer les erreurs inattendues
        raise HTTPException(status_code=500, detail=f"Une erreur interne est survenue: {e}")

