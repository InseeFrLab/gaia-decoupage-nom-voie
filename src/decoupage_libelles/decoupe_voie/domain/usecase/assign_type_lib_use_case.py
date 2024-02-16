from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.usecase.get_words_between_use_case import GetWordsBetweenUseCase


class AssignTypeLibUseCase:
    @inject
    def __init__(self, get_words_between_use_case: GetWordsBetweenUseCase):
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case
        

    def execute(
            self,
            infovoie: InfoVoie,
            type_principal: InformationOnTypeOrdered
            ) -> VoieDecoupee:
        label_assigned = self.get_words_between_use_case.execute(infovoie, type_principal.position_start+1)

        return VoieDecoupee(
            label_raw=infovoie.label_raw,
            type_assigned=type_principal.type_name,
            label_assigned=label_assigned,
            compl_assigned=' '
        )
