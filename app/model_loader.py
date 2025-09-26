import os
import tensorflow as tf

# Le répertoire où votre modèle est stocké
MODEL_DIR = "./model"
# Le nom de votre fichier de modèle.
MODEL_PATH = os.path.join(MODEL_DIR, "model.tflite")

def load_tf_model():
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Le fichier du modèle n'a pas été trouvé à l'emplacement : {MODEL_PATH}. "
                f"Assurez-vous de placer votre fichier 'model.h5' dans le dossier 'model'."
            )
        
        # Charger le modèle avec Keras
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Modèle MobileNet chargé avec succès.")
        return model
    except Exception as e:
        print(f"Erreur critique lors du chargement du modèle TensorFlow : {e}")
        return None

classification_model = load_tf_model()
