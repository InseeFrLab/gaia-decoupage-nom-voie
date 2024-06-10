from typing import List, Dict
import re
from unidecode import unidecode


PONCTUATIONS = ["-", ".", ",", ";", ":", "!", "?", "(", ")", "[", "]", "{", "}", "'", '"', "«", "»", "*", "/"]


def separate_words_with_apostrophe_and_supress_ponctuation_use_case(label_raw: str, ponctuations: List[str]) -> List[str]:
    voie = label_raw
    # séparer le libellé en liste de mots
    voie_separated = voie.split(" ")
    # séparer en deux les mots avec apostrophe
    voie_separated_apostrophe = [mot.split("'") for mot in voie_separated]
    voie_separated_without_apostrophe = [mot for item in voie_separated_apostrophe for mot in item]
    voie_separated_without_apostrophe = [segment for mot in voie_separated_without_apostrophe for segment in re.split(r"(\d+)", mot) if segment]
    # retirer les ponctuations seules et les espaces en trop
    voie_treated = [item for item in voie_separated_without_apostrophe if (item not in ponctuations and item != "")]
    return voie_treated


def suppress_ponctuation_in_words_use_case(chaine_traitee: List[str], ponctuations: List[str]) -> List[str]:
    # retirer la ponctuation contenue dans un mot
    new_label_preproc = []
    for mot in chaine_traitee:
        mot_sep = re.split(r"([-.,;:!?(){}*/])", mot)
        mot_sep = [ss for ss in mot_sep if ss.strip()]
        new_mot = [ss for ss in mot_sep if ss not in ponctuations]
        for sous_mot in new_mot:
            new_label_preproc.append(sous_mot)
    return new_label_preproc


def preprocess_ponctuation_in_list_lib(list_queries: List[str]) -> List[Dict[str, Dict[str, str]]]:
    queries_raw_preproc = []
    for query_lib in list_queries:
        voie_ascii_folded = unidecode(query_lib)
        voie_upper = voie_ascii_folded
        chaine_decoupee = separate_words_with_apostrophe_and_supress_ponctuation_use_case(voie_upper, PONCTUATIONS)
        new_label_preproc = suppress_ponctuation_in_words_use_case(chaine_decoupee, PONCTUATIONS)
        libelle_preproc = (" ").join(new_label_preproc)
        queries_raw_preproc.append({query_lib: libelle_preproc.lower()})

    return queries_raw_preproc


#########
# Exemple
#########
preprocess_ponctuation_in_list_lib(["rue d'acueil"])
