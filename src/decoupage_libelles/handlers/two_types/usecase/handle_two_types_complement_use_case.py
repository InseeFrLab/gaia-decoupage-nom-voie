from typing import Optional, Tuple
import logging

from decoupage_libelles.decoupage_final_constructors.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupage_final_constructors.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.information_generators.libelle.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.handlers.two_types.usecase.compl_two_types_long_or_agglo_use_case import ComplTwoTypesLongOrAggloUseCase
from decoupage_libelles.handlers.two_types.usecase.compl_first_type_compl_use_case import ComplFirstTypeComplUseCase
from decoupage_libelles.handlers.two_types.usecase.compl_second_type_compl_use_case import ComplSecondTypeComplUseCase
from decoupage_libelles.handlers.two_types.usecase.compl_third_type_compl_use_case import ComplThirdTypeComplUseCase


class HandleTwoTypesComplUseCase:
    """
    Gère les voies à 2 types détectés qui contiennent un type complément.

    Note : ComplImmeubleBeforeTypeUseCase a été retiré — il était commenté dans
    l'ancienne version et donc non exécuté. La logique reste inchangée.
    """

    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        compl_two_types_long_or_agglo_use_case: ComplTwoTypesLongOrAggloUseCase = ComplTwoTypesLongOrAggloUseCase(),
        compl_first_type_compl_use_case: ComplFirstTypeComplUseCase = ComplFirstTypeComplUseCase(),
        compl_second_type_compl_use_case: ComplSecondTypeComplUseCase = ComplSecondTypeComplUseCase(),
        compl_third_type_compl_use_case: ComplThirdTypeComplUseCase = ComplThirdTypeComplUseCase(),
    ):
        self.generate_information_on_lib_use_case = generate_information_on_lib_use_case
        self.assign_lib_use_case = assign_lib_use_case
        self.compl_two_types_long_or_agglo_use_case = compl_two_types_long_or_agglo_use_case
        self.compl_first_type_compl_use_case = compl_first_type_compl_use_case
        self.compl_second_type_compl_use_case = compl_second_type_compl_use_case
        self.compl_third_type_compl_use_case = compl_third_type_compl_use_case

    def execute(self, voie_compl: InfoVoie) -> Tuple[Optional[VoieDecoupee], Optional[InfoVoie]]:
        self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=False)

        # Cascade de 4 use cases spécialisés — le premier qui retourne un résultat gagne.
        # En fallback : assign_lib (tout en libellé).
        voie_treated = (
            self.compl_two_types_long_or_agglo_use_case.execute(voie_compl)
            or self.compl_first_type_compl_use_case.execute(voie_compl)
            or self.compl_second_type_compl_use_case.execute(voie_compl)
            or self.compl_third_type_compl_use_case.execute(voie_compl)
            or self.assign_lib_use_case.execute(voie_compl)
        )

        # Deuxième valeur de retour : voie à repasser en handler 2 types (None = pas nécessaire)
        return voie_treated, None
