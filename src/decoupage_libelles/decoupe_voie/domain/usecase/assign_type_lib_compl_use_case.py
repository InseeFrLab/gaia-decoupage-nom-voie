from injector import inject
from typing import Optional

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from decoupe_voie.domain.model.voie_decoupee import VoieDecoupee
from informations_on_libelle_voie.domain.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from informations_on_type_in_lib.domain.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered


class AssignTypeLibComplUseCase:
    @inject
    def __init__(self, get_words_between_use_case: GetWordsBetweenUseCase, order_type_in_lib_use_case: OrderTypeInLib):
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        

    def execute(
            self,
            infovoie: InfoVoie,
            type_principal: Optional[InformationOnTypeOrdered] = None,
            type_compl: Optional[InformationOnTypeOrdered] = None,
            ) -> VoieDecoupee:
        if not type_principal and not type_compl:
            type_principal = self.order_type_in_lib_use_case.execute(infovoie, 1)
            type_compl = self.order_type_in_lib_use_case.execute(infovoie, 2)
        label_assigned = self.get_words_between_use_case.execute(infovoie, type_principal.position_end+1, type_compl.position_start)
        compl_assigned = self.get_words_between_use_case.execute(infovoie, type_compl.position_start)

        return VoieDecoupee(
            label_raw=infovoie.label_raw,
            type_assigned=type_principal.type_name,
            label_assigned=label_assigned,
            compl_assigned=compl_assigned
        )
