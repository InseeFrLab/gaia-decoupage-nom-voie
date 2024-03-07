from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase


class ComplSecondTypeComplUseCase:
    def __init__(
        self,
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = AssignTypeLibComplUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
    ):
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_lib_compl_use_case: AssignTypeLibComplUseCase = assign_type_lib_compl_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        first_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 1)
        second_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 2)
        third_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, 3)

        if second_type.type_name in ComplementFinderUseCase.TYPES_COMPLEMENT_1_2:
            if first_type.is_longitudinal or first_type.is_agglomerant:
                # 1er type + lib + 2e type compl
                # "RUE HOCHE BAT LA PLAGE"
                return self.assign_type_lib_compl_use_case.execute(voie_compl)
            elif third_type.is_longitudinal or third_type.is_agglomerant:
                #  compl + 3e type + lib
                # "LA PLAGE BAT LILAS RUE DE BRAS"
                return self.assign_compl_type_lib_use_case.execute(voie_compl)
            else:
                # lib
                # "LA PLAGE BAT LILAS CHATEAU DU BAS"
                return self.assign_lib_use_case.execute(voie_compl)
