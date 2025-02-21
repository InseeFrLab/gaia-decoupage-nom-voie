from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
import re


class DilatedVoieDecoupeeUseCase:
    DILATATION_TYPE_VOIE = {
        "IM": "IMMEUBLE",
        "PAV":"PAVILLON",
        "IMM":"IMMEUBLE",
        "BAT":"BATIMENT",
        "APRT":"APPARTEMENT",
        "APT":"APPARTEMENT",
        "APPRT":"APPARTEMENT",
        "APPT":"APPARTEMENT",
        "LGT":"LOGEMENT",
        "LOG":"LOGEMENT",
        "ENT":"ENTREE"
    }

    DILATATION_NOM_VOIE = {
        "GAL": "GENERAL",
        "PR": "PROFESSEUR",
        "PT": "PETIT",
        "PTE": "PETITE",
    }

    DILATATION_COMPLEMENT = DILATATION_TYPE_VOIE | DILATATION_NOM_VOIE

    def execute(self, voiedecoupee: VoieDecoupee) -> VoieDecoupee:
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_TYPE_VOIE.items():
            voiedecoupee.type_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.type_assigned, flags=re.IGNORECASE)  
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_NOM_VOIE.items():
            voiedecoupee.label_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.label_assigned, flags=re.IGNORECASE)  
        for acronym, full_form in DilatedVoieDecoupeeUseCase.DILATATION_COMPLEMENT.items():
            voiedecoupee.compl_assigned = re.sub(rf'\b{acronym}\b', full_form, voiedecoupee.compl_assigned, flags=re.IGNORECASE)  
        return voiedecoupee
