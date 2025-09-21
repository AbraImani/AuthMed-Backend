from fastapi import FastAPI
from contextlib import asynccontextmanager
from . import routes, database, crud, schemas
from .database import SessionLocal

def seed_database():
    """
    Initialise la base de données avec des données de référence (mock).
    C'est pour nous permettre  d'éviter d'avoir une base de médicaments vide au démarrage.
    """
    db = SessionLocal()
    try:
        # Vérifier si des médicaments existent déjà
        medicaments = crud.get_all_medicaments(db)
        if not medicaments:
            print("Base de données vide, initialisation avec des données de test...")
            medicaments_to_add = [
                schemas.MedicamentCreate(
                    nom="Paracétamol 500mg",
                    code_barres="8901234123457",
                    qr_code_data="SN:123;EXP:2026-12"
                ),
                schemas.MedicamentCreate(
                    nom="Ibuprofène 200mg",
                    code_barres="9780201379624",
                    qr_code_data="SN:456;EXP:2025-10"
                )
            ]
            for med in medicaments_to_add:
                crud.create_medicament(db, medicament=med)
            print("Données de test ajoutées.")
        else:
            print("La base de données contient déjà des données.")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code à exécuter avant le démarrage de l'application
    database.init_db()
    seed_database()
    yield
    # Code à exécuter après l'arrêt de l'application (pas nécessaire ici maintenant c'est à préserver)

app = FastAPI(
    title="API AuthMed - Détection de Médicaments",
    description="Une API pour analyser des images de médicaments et vérifier leur authenticité.",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API AuthMed. Accédez à /docs pour la documentation."}

