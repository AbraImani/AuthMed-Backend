"""
Je utiliser ceci pour faire un petit test coté model mais c'est pas vraiment 
utile dans ce cadre car je veux implementer deux fichier celui de analysis_module.py et
image_processor.py
"""

import random

class DummyModel:
    def __init__(self):
        self.labels = ["Authentique", "Contrefait"]
        print("Modèle factice initialisé.")
    def predict(self, data: str):
        """
        Simule une prédiction.
        
        Args:
            data (str): Les données d'entrée (ignorées dans ce modèle factice).
            
        Returns:
            dict: Un dictionnaire contenant le label et le score de la prédiction.
        """
        # Choisit un label au hasard
        predicted_label = random.choice(self.labels)
        
        # Génère un score de confiance aléatoire
        prediction_score = random.uniform(0.5, 1.0)
        
        print(f"Prédiction factice générée: {predicted_label} (Score: {prediction_score:.2f})")
        
        return {
            "label": predicted_label,
            "score": round(prediction_score, 4)
        }

# Instanciation unique du modèle au chargement du module.
# L'application utilisera cette instance unique pour toutes les prédictions.
dummy_model = DummyModel()
