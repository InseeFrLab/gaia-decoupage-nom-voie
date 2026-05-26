from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupage_final_constructors.usecase.dilated_voie_decoupee_use_case import DilatedVoieDecoupeeUseCase


class AssignLibUseCase:
    def __init__(self, dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = DilatedVoieDecoupeeUseCase()):
        self.dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = dilated_voie_decoupee_use_case

    def execute(
        self,
        infovoie: InfoVoie,
    ) -> VoieDecoupee:
        label_assigned = (" ").join(infovoie.label_preproc) if infovoie.label_preproc else ""
        voiedecoupee = VoieDecoupee(label_origin=infovoie.label_origin, type_assigned="", label_assigned=label_assigned, compl_assigned="", compl2=infovoie.complement)
        voiedecoupee = self.dilated_voie_decoupee_use_case.execute(voiedecoupee)

        return voiedecoupee

