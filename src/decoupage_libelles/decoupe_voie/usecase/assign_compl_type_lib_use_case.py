from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase


class AssignComplTypeLibUseCase:

    def __init__(self, get_words_between_use_case: GetWordsBetweenUseCase = GetWordsBetweenUseCase()):
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case

    def execute(
        self,
        infovoie: InfoVoie,
        type_principal: InformationOnTypeOrdered,
    ) -> VoieDecoupee:
        label_assigned = self.get_words_between_use_case.execute(type_principal.position_end + 1)
        compl_assigned = self.get_words_between_use_case.execute(0, type_principal.position_start)

        return VoieDecoupee(label_raw=infovoie.label_raw, type_assigned=type_principal.type_name, label_assigned=label_assigned, compl_assigned=compl_assigned)
