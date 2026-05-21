from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from unidecode import unidecode
import re


class BasicPreprocessWordsUseCase:
    def execute(self, voie: InfoVoie) -> InfoVoie:
        voie_without_degree = re.sub(r"[°]", " ", voie.label_raw)
        voie_ascii_folded = unidecode(voie_without_degree)
        voie_number_letter_separeted = re.sub(r"(\d+)([a-zA-Z]+)", r"\1 \2", voie_ascii_folded)
        voie_letter_number_separated = re.sub(r"([a-zA-Z]+)(\d+)", r"\1 \2", voie_number_letter_separeted)
        voie_without_extra_spaces = re.sub(r"\s+", " ", voie_letter_number_separated).strip()
        voie_upper = voie_without_extra_spaces.upper()
        voie.label_raw = voie_upper

        return voie
