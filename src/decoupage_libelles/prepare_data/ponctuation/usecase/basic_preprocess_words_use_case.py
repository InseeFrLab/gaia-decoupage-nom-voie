from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from unidecode import unidecode
import re


class BasicPreprocessWordsUseCase:
    EXTRA_SYNONYMS = {
        'st': 'saint',
        'ste': 'sainte',
        'sts': 'saints',
        'stes': 'saintes',
        'gd': 'grand',
        'gde': 'grande',
        'gds': 'grands',
        'gdes': 'grandes',
        'pt': 'petit',
        'pte': 'petite',
        'pts': 'petits',
        'ptes': 'petites',
        'gen': 'general',
        'gal': 'general',
        'mal': 'marechal',
        'lt': 'lieutenant',
        'cdt': 'commandant',
        'dr': 'docteur',
        'ht': 'haut',
        'hte': 'haute',
        'hts': 'hauts',
        'htes': 'hautes',
        'pdt': 'president',
        'sgt': 'sergent',
        'pr': 'professeur'
        }

    def execute(self, voie: InfoVoie) -> InfoVoie:
        voie_ascii_folded = unidecode(voie.label_raw)
        voie_number_letter_separeted = re.sub(r"(\d+)([a-zA-Z]+)", r"\1 \2", voie_ascii_folded)
        voie_without_extra_spaces = re.sub(r"\s+", " ", voie_number_letter_separeted).strip() 
        voie_upper = voie_without_extra_spaces.upper()
        for acronym, full_form in BasicPreprocessWordsUseCase.EXTRA_SYNONYMS.items():
            voie_upper = re.sub(rf'\b{acronym}\b', f'{acronym} {full_form}', voie_upper, flags=re.IGNORECASE)        

        voie.label_raw = voie_upper

        return voie