from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
import logging
from typing import List, Dict
from decoupage_libelles.config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.preprocessing.pipeline.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from decoupage_libelles.preprocessing.text_normalization.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.information_generators.libelle.usecase.apply_postagging_use_case import ApplyPostaggingUseCase


class VoiesData(BaseModel):
    list_labels_voies: List[str] = Field(
        ...,
        example=[
            "Hoche rue",
            "Residence Soleil Rue des cerisiers",
        ],
    )


class VoieData(BaseModel):
    label_voie: str = Field(
        ...,
        example="rue hoche"
    )


def process(voies_data, launcher: TypeVoieDecoupageLauncher) -> List[Dict[str, Dict[str, str]]]:
    list_labels_voies = list(set(voies_data.list_labels_voies))
    voies_processed = launcher.execute(voies_data=list_labels_voies)
    return [
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


def process_preproc(voies_data) -> List[Dict[str, Dict[str, str]]]:
    ponctuation_preprocessor_use_case = PonctuationPreprocessorUseCase()
    list_labels_voies = list(set(voies_data.list_labels_voies))
    voies_preproc = []
    for libelle in list_labels_voies:
        lib_without_preprocessed_ponctuation = InfoVoie(label_origin=libelle)
        lib_with_preprocessed_ponctuation = ponctuation_preprocessor_use_case.execute(lib_without_preprocessed_ponctuation)
        libelle_preproc = " ".join(lib_with_preprocessed_ponctuation.label_preproc).lower()
        if lib_with_preprocessed_ponctuation.complement:
            libelle_preproc += " " + lib_with_preprocessed_ponctuation.complement.lower()
        voies_preproc.append({libelle: libelle_preproc})
    return voies_preproc


def process_detect_types_voies(voie_data) -> Dict[str, str]:
    voie_lib_preprocessor_use_case = VoieLibPreprocessorUseCase()

    infovoie = InfoVoie(label_origin=voie_data)
    r = voie_lib_preprocessor_use_case.execute([infovoie])

    return {voie_data: r[0].types_and_positions}


def process_postag(voie_data) -> Dict[str, str]:
    voie_lib_preprocessor_use_case = VoieLibPreprocessorUseCase()

    infovoie = InfoVoie(label_origin=voie_data)
    voie_preprocessed = voie_lib_preprocessor_use_case.execute([infovoie])[0]

    apply_postagging_use_case: ApplyPostaggingUseCase = ApplyPostaggingUseCase()

    r = apply_postagging_use_case.execute(voie_preprocessed)

    return {voie_data: r.label_postag}


app = FastAPI()
launcher = TypeVoieDecoupageLauncher()

logging.info("Démarrage de l'API")
logging.info("API de découpage des libellés de voies")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.post(
    "/analyse-libelles-voies",
    summary="Découper les libellés de voies",
    description="Cette route permet de découper les libellés de voies pour en extraire des types",
)
async def analyse_libelles_voies(voies_data: VoiesData):
    return {"reponse": process(voies_data, launcher)}


@app.post(
    "/ponctuation-preprocessing-adresse",
    summary="Nettoye la ponctuation au sein des adresses",
    description="Cette route permet de nettoyer la ponctuation au sein des adresses",
)
async def preproc_libelles_voies(voies_data: VoiesData):
    return {"reponse": process_preproc(voies_data)}


@app.post(
    "/detect-types-voies",
    summary="Détection des types de voie au sein du libellé de voie",
    description="Cette route permet de détecter les types de voie potentiels au sein du libellé de voie",
)
async def detect_types_voies(voie_data: VoieData):
    return {"reponse": process_detect_types_voies(voie_data)}


@app.post(
    "/postag",
    summary="Applique le modèle NLP sur le libellé de voie",
    description="Cette route retourne les étiquetages synthaxiques générés par le modèle NLP sur le libellé de voie",
)
async def postag(voie_data: VoieData):
    return {"reponse": process_postag(voie_data)}
