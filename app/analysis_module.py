from sqlalchemy.orm import Session
from typing import Dict, Any
import cv2
import numpy as np
import tensorflow as tf

from . import models
from .model_loader import classification_model

CLASS_NAMES = ["Counterfeit", "Authentic"] 
# La taille d'image attendue par MobileNet (généralement 224x224)
MODEL_INPUT_SIZE = (224, 224) 

def prepare_image_for_mobilenet(image_path: str) -> np.ndarray:
    """
    Charge, redimensionne et pré-traite de l'image pour qu'elle corresponde
    au format d'entrée spécifique du modèle MobileNet.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Impossible de lire l'image depuis le chemin fourni.")

    # Convertir l'ordre des couleurs de BGR (OpenCV) à RGB (TensorFlow)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Redimensionner à la taille exacte attendue par le modèle
    img_resized = cv2.resize(img_rgb, MODEL_INPUT_SIZE)

    # La forme passe de (224, 224, 3) à (1, 224, 224, 3)
    img_expanded = np.expand_dims(img_resized, axis=0)

    # Cette fonction normalise les pixels dans la plage [-1, 1]
    return tf.keras.applications.mobilenet.preprocess_input(img_expanded)


def analyze_image_with_model(image_path: str, db: Session) -> Dict[str, Any]:
    """
    Effectue une analyse d'image en utilisant le modèle TensorFlow (MobileNet) chargé.
    """
    if classification_model is None:
        return {
            "status": models.AnalysisStatus.SUSPECT,
            "message": "Erreur : Le modèle de classification n'est pas disponible.",
            "matched_medicament": None
        }

    # Préparer l'image
    prepared_image = prepare_image_for_mobilenet(image_path)
    
    # Faire la prédiction
    predictions = classification_model.predict(prepared_image)
    probabilities = predictions[0] # Extraire les probabilités pour notre unique image

    # Interpréter le résultat
    confidence = np.max(probabilities)
    prediction_index = np.argmax(probabilities)
    prediction_label = CLASS_NAMES[prediction_index]

    CONFIDENCE_THRESHOLD = 0.75 # Seuil de confiance minimal

    if confidence < CONFIDENCE_THRESHOLD:
        status = models.AnalysisStatus.SUSPECT
        message = (f"Le modèle n'est pas certain du résultat (Confiance: {confidence:.2%}). "
                   f"Classification la plus probable : {prediction_label}. La prudence est recommandée.")
    elif prediction_label == "Authentique":
        status = models.AnalysisStatus.AUTHENTIQUE
        message = f"Le modèle a classifié l'image comme 'Authentique' avec une confiance de {confidence:.2%}."
    else: # Contrefait
        status = models.AnalysisStatus.CONTREFAIT
        message = f"Alerte : Le modèle a classifié l'image comme 'Contrefait' avec une confiance de {confidence:.2%}."

    return {
        "status": status,
        "message": message,
        "matched_medicament": None
    }

