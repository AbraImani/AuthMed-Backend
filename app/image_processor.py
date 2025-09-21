import hashlib
from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy as np
import os
from typing import Tuple

# Répertoire pour stocker temporairement les images traités
PROCESSED_IMAGES_DIR = "./processed_images"
if not os.path.exists(PROCESSED_IMAGES_DIR):
    os.makedirs(PROCESSED_IMAGES_DIR)

def calculate_hash(image_bytes: bytes) -> str:
    # calcule le hash SHA256 d'une image pour en avoir une empreinte unique.
    sha256_hash = hashlib.sha256()
    sha256_hash.update(image_bytes)
    return sha256_hash.hexdigest()

def preprocess_image(image_bytes: bytes, image_hash: str) -> str:
    """
    Appliquons une pipeline de prétraitement à une image et la sauvegarde.
    
    Args:
        image_bytes: L'image sous forme de bytes.
        image_hash: Le hash de l'image, utilisé pour le nom du fichier.

    Returns:
        Le chemin vers l'image sauvegardée.
    """
    try:
        # 1. Charger l'image avec opencv
        image_np = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # 2. Conversion en niveaux de gris (standard pour OCR et analyse)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Redimensionnement
        #  A completer après, pour ce MVP, nous gardons la taille mais 
        # on pourrait la fixer, ex: (1024, 768)
        
        # 4. Amélioration du contraste (CLAHE est efficace pour les images non uniformes)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_img = clahe.apply(gray_img)

        # 5. Sauvegarde de l'image traitée
        output_filename = f"{image_hash}.png"
        output_path = os.path.join(PROCESSED_IMAGES_DIR, output_filename)
        cv2.imwrite(output_path, enhanced_img)
        
        return output_path
    
    except Exception as e:
        # gérer les erreurs si l'image est corrompue ou le format non supporté
        print(f"Erreur de prétraitement de l'image: {e}")
        raise ValueError("Le fichier image est invalide ou corrompu.")
