from injector import inject

from informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupe_voie.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib


class AssignLibComplUseCase:
    @inject
    def __init__(self, get_words_between_use_case: GetWordsBetweenUseCase, order_type_in_lib_use_case: OrderTypeInLib):
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        

    def execute(
            self,
            infovoie: InfoVoie,
            ) -> VoieDecoupee:
        type_principal = self.order_type_in_lib_use_case.execute(infovoie, 1)
        label_assigned = self.get_words_between_use_case.execute(infovoie, 0, type_principal.position_start)
        compl_assigned = self.get_words_between_use_case.execute(infovoie, type_principal.position_start)

        return VoieDecoupee(
            label_raw=infovoie.label_raw,
            type_assigned=' ',
            label_assigned=label_assigned,
            compl_assigned=compl_assigned
        )
