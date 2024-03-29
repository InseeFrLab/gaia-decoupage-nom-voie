from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import logging


class LibelleVoie(BaseModel):
    libelle: str


app = FastAPI()


def initialize_api():
    """_summary_
    Code exécuté au démarrage de l'API
    """
    logging.info("Démarrage de l'API")
    logging.info("API de découpage des libellés de voies")


def process(libelle: str) -> str:
    return libelle


initialize_api()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.post(
    "/analyse-libelles-voies",
    summary="Découper les libellés de voies",
    description="Cette route permet de découper les libellés de voies pour en extraire des types",
)
async def analyse_libelles_voies(libelle: LibelleVoie):
    return {"reponse": process(libelle)}
