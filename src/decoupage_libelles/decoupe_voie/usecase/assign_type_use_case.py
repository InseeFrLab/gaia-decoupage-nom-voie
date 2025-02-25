from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.dilated_voie_decoupee_use_case import DilatedVoieDecoupeeUseCase


class AssignTypeUseCase:
    def __init__(self, dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = DilatedVoieDecoupeeUseCase()):
        self.dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = dilated_voie_decoupee_use_case

    def execute(self, infovoie: InfoVoie, type_principal: InformationOnTypeOrdered) -> VoieDecoupee:
        voiedecoupee = VoieDecoupee(label_origin=infovoie.label_origin, type_assigned=type_principal.type_name, label_assigned="", compl_assigned="", compl2=infovoie.complement)

        try:
            voiedecoupee = self.dilated_voie_decoupee_use_case.execute(voiedecoupee)
        except:
            voiedecoupee = voiedecoupee

        return voiedecoupee
