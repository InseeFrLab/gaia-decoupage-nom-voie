from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee


class AssignLibUseCase:
    def execute(
        self,
        infovoie: InfoVoie,
    ) -> VoieDecoupee:
        label_assigned = (" ").join(infovoie.label_preproc)
        return VoieDecoupee(label_origin=infovoie.label_origin, type_assigned=" ", label_assigned=label_assigned, compl_assigned=" ", compl2=infovoie.complement)
