from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_libelle_voie.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.order_type_in_lib_use_case import OrderTypeInLib
from decoupage_libelles.decoupe_voie.usecase.dilated_voie_decoupee_use_case import DilatedVoieDecoupeeUseCase


class AssignLibComplUseCase:
    def __init__(
        self,
        get_words_between_use_case: GetWordsBetweenUseCase = GetWordsBetweenUseCase(),
        order_type_in_lib_use_case: OrderTypeInLib = OrderTypeInLib(),
        dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = DilatedVoieDecoupeeUseCase()
    ):
        self.get_words_between_use_case: GetWordsBetweenUseCase = get_words_between_use_case
        self.order_type_in_lib_use_case: OrderTypeInLib = order_type_in_lib_use_case
        self.dilated_voie_decoupee_use_case: DilatedVoieDecoupeeUseCase = dilated_voie_decoupee_use_case

    def execute(
        self,
        infovoie: InfoVoie,
    ) -> VoieDecoupee:
        type_principal = self.order_type_in_lib_use_case.execute(infovoie, 1)
        label_assigned = self.get_words_between_use_case.execute(infovoie, 0, type_principal.position_start)
        compl_assigned = self.get_words_between_use_case.execute(infovoie, type_principal.position_start)

        voiedecoupee = VoieDecoupee(label_origin=infovoie.label_origin, type_assigned=" ", label_assigned=label_assigned, compl_assigned=compl_assigned, compl2=infovoie.complement)
        voiedecoupee = self.dilated_voie_decoupee_use_case.execute(voiedecoupee)

        return voiedecoupee