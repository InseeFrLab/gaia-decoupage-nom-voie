from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
import logging
from typing import List, Dict
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase


class VoiesData(BaseModel):
    list_labels_voies: List[str] = Field(
        ...,
        example=[
            "Hoche rue",
            "Residence Soleil Rue des cerisiers",
        ],
    )


def process(voies_data) -> List[Dict[str, Dict[str, str]]]:
    list_labels_voies = list(set(voies_data.list_labels_voies))
    voies_processed = TypeVoieDecoupageLauncher().execute(voies_data=list_labels_voies)
    voies_processed_dict = [
        {
            voie.label_origin if voie.label_origin else "": {
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


def process_preproc(voies_data) -> List[Dict[str, Dict[str, str]]]:
    ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = PonctuationPreprocessorUseCase()
    list_labels_voies = list(set(voies_data.list_labels_voies))
    voies_preproc = []
    for libelle in list_labels_voies:
        lib_without_preprocessed_ponctuation = InfoVoie(label_origin=libelle)
        lib_with_preprocessed_ponctuation = ponctuation_preprocessor_use_case.execute(lib_without_preprocessed_ponctuation)
        libelle_preproc = (" ").join(lib_with_preprocessed_ponctuation.label_preproc)
        libelle_preproc = libelle_preproc.lower()
        if lib_with_preprocessed_ponctuation.complement:
            libelle_preproc += (" ") + lib_with_preprocessed_ponctuation.complement.lower()
        voies_preproc.append({libelle: libelle_preproc})
    return voies_preproc


app = FastAPI()


def initialize_api():
    logging.info("Démarrage de l'API")
    logging.info("API de découpage des libellés de voies")


initialize_api()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/clear-cache")
async def clear_cache():
    global type_voie_decoupage_launcher
    type_voie_decoupage_launcher = TypeVoieDecoupageLauncher()  # Réinstanciation
    return {"message": "Cache vidé"}

@app.post(
    "/analyse-libelles-voies",
    summary="Découper les libellés de voies",
    description="Cette route permet de découper les libellés de voies pour en extraire des types",
)
async def analyse_libelles_voies(voies_data: VoiesData):
    return {"reponse": process(voies_data)}


@app.post(
    "/ponctuation-preprocessing-adresse",
    summary="Nettoye la ponctuation au sein des adresses",
    description="Cette route permet de nettoyer la ponctuation au sein des adresses",
)
async def preproc_libelles_voies(voies_data: VoiesData):
    return {"reponse": process_preproc(voies_data)}
