from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_second_pos_use_case import ComplTypeInFirstOrSecondPosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_middle_pos_use_case import ComplTypeInFirstOrMiddlePosUseCase
from decoupage_libelles.handle_voies_one_type.usecase.compl_type_in_first_or_last_pos_use_case import ComplTypeInFirstOrLastPosUseCase
from decoupage_libelles.prepare_data.clean_voie_lib_and_find_types.usecase.suppress_article_in_first_place_use_case import SuppressArticleInFirstPlaceUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class HandleOneTypeComplUseCase:
    def __init__(
        self,
        compl_type_in_first_or_second_pos_use_case: ComplTypeInFirstOrSecondPosUseCase = ComplTypeInFirstOrSecondPosUseCase(),
        compl_type_in_first_or_middle_pos_use_case: ComplTypeInFirstOrMiddlePosUseCase = ComplTypeInFirstOrMiddlePosUseCase(),
        compl_type_in_first_or_last_pos_use_case: ComplTypeInFirstOrLastPosUseCase = ComplTypeInFirstOrLastPosUseCase(),
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = SuppressArticleInFirstPlaceUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
    ):
        self.compl_type_in_first_or_second_pos_use_case: ComplTypeInFirstOrSecondPosUseCase = compl_type_in_first_or_second_pos_use_case
        self.compl_type_in_first_or_middle_pos_use_case: ComplTypeInFirstOrMiddlePosUseCase = compl_type_in_first_or_middle_pos_use_case
        self.compl_type_in_first_or_last_pos_use_case: ComplTypeInFirstOrLastPosUseCase = compl_type_in_first_or_last_pos_use_case
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.suppress_article_in_first_place_use_case: SuppressArticleInFirstPlaceUseCase = suppress_article_in_first_place_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case

    def execute(self, voie_compl: InfoVoie) -> VoieDecoupee:
        last_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, -1)

        if voie_compl.has_type_in_first_pos:
            if voie_compl.has_type_in_second_pos:
                return self.compl_type_in_first_or_second_pos_use_case.execute(voie_compl)

            elif voie_compl.has_type_in_last_pos:
                return self.compl_type_in_first_or_last_pos_use_case.execute(voie_compl)

            else:
                return self.compl_type_in_first_or_middle_pos_use_case.execute(voie_compl)

        elif voie_compl.has_type_in_last_pos and not last_type.is_complement:
            self.generate_information_on_lib_use_case.execute(voie_compl, apply_nlp_model=True)
            last_type = self.generate_information_on_type_ordered_use_case.execute(voie_compl, -1)
            last_type_name_in_lib = (' ').join(voie_compl.label_preproc[last_type.position_start:last_type.position_end+1])
            if (last_type.type_name == last_type_name_in_lib and
                    not last_type.has_adj_det_before):
                # 'PO IMM RUE'
                # lib + 2eme type
                return self.assign_lib_type_use_case.execute(voie_compl, last_type)
            else:
                return self.assign_lib_use_case.execute(voie_compl)
        else:
            # 'BEAU PAVILLON DE LA FORET'
            # lib
            return self.assign_lib_use_case.execute(voie_compl)
