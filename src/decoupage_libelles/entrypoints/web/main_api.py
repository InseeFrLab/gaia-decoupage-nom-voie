from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
import logging
from typing import List, Dict
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
from dataclasses import dataclass


@dataclass
class VoiesData(BaseModel):
    list_labels_voies: List[str] = Field(..., example=["rue Hoche", "Residence Soleil Rue des cerisiers"])


def process(voies_data) -> List[Dict[str, Dict[str, str]]]:
    list_labels_voies = list(set(voies_data.list_labels_voies))

    voies_processed = TypeVoieDecoupageLauncher().execute(voies_data=list_labels_voies)

    voies_processed_dict = [
        {
            voie.label_origin.lower() if voie.label_origin else "": {
                "numero": voie.num_assigned if voie.num_assigned is not None else "",
                "indice_rep": voie.indice_rep.lower() if voie.indice_rep else "",
                "typeVoie": voie.type_assigned.lower() if voie.type_assigned else "",
                "libelleVoie": voie.label_assigned.lower() if voie.label_assigned else "",
                "complementAdresse": voie.compl_assigned.lower() if voie.compl_assigned else "",
                "complementAdresse2": voie.compl2.lower() if voie.compl2 else "",
            }
        }
        for voie in voies_processed
    ]
    return voies_processed_dict


app = FastAPI()


def initialize_api():
    """_summary_
    Code exécuté au démarrage de l'API
    """
    logging.info("Démarrage de l'API")
    logging.info("API de découpage des libellés de voies")


initialize_api()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.post(
    "/analyse-libelles-voies",
    summary="Découper les libellés de voies",
    description="Cette route permet de découper les libellés de voies pour en extraire des types",
)
async def analyse_libelles_voies(voies_data: VoiesData):
    return {"reponse": process(voies_data)}
