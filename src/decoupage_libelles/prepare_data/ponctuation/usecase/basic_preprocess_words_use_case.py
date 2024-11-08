from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from unidecode import unidecode
import re


class BasicPreprocessWordsUseCase:
    def execute(self, voie: InfoVoie) -> InfoVoie:
        voie_ascii_folded = unidecode(voie.label_raw)
        voie_number_letter_separeted = re.sub(r"(\d+)([a-zA-Z]+)", r"\1 \2", voie_ascii_folded)
        voie_without_extra_spaces = re.sub(r"\s+", " ", voie_number_letter_separeted).strip() 
        voie_upper = voie_without_extra_spaces.upper()
        voie.label_raw = voie_upper

        return voie
