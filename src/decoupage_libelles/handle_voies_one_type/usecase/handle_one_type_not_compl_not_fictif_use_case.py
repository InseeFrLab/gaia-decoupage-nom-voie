from decoupage_libelles.decoupe_voie.model.voie_decoupee import VoieDecoupee
from decoupage_libelles.decoupe_voie.usecase.assign_type_lib_use_case import AssignTypeLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_type_use_case import AssignTypeUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_lib_use_case import AssignLibUseCase
from decoupage_libelles.decoupe_voie.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.informations_on_libelle_voie.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from decoupage_libelles.informations_on_type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from decoupage_libelles.handle_voies_two_types_and_more.usecase.keep_types_without_article_adj_before_use_case import KeepTypesWithoutArticleAdjBeforeUseCase


class HandleOneTypeNotComplNotFictifUseCase:
    def __init__(
        self,
        generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = GenerateInformationOnLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
        assign_type_lib_use_case: AssignTypeLibUseCase = AssignTypeLibUseCase(),
        assign_lib_type_use_case: AssignLibTypeUseCase = AssignLibTypeUseCase(),
        assign_lib_use_case: AssignLibUseCase = AssignLibUseCase(),
        assign_type_use_case: AssignTypeUseCase = AssignTypeUseCase(),
        assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = AssignComplTypeLibUseCase(),
        keep_types_without_article_adj_before_use_case: KeepTypesWithoutArticleAdjBeforeUseCase = KeepTypesWithoutArticleAdjBeforeUseCase(),
    ):
        self.generate_information_on_lib_use_case: GenerateInformationOnLibUseCase = generate_information_on_lib_use_case
        self.generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = generate_information_on_type_ordered_use_case
        self.assign_type_lib_use_case: AssignTypeLibUseCase = assign_type_lib_use_case
        self.assign_lib_type_use_case: AssignLibTypeUseCase = assign_lib_type_use_case
        self.assign_lib_use_case: AssignLibUseCase = assign_lib_use_case
        self.assign_type_use_case: AssignTypeUseCase = assign_type_use_case
        self.keep_types_without_article_adj_before_use_case: KeepTypesWithoutArticleAdjBeforeUseCase = keep_types_without_article_adj_before_use_case
        self.assign_compl_type_lib_use_case: AssignComplTypeLibUseCase = assign_compl_type_lib_use_case

    def execute(self, voie: InfoVoie) -> VoieDecoupee:
        self.generate_information_on_lib_use_case.execute(voie, apply_nlp_model=False)
        voie_treated = None

        if voie.has_type_in_first_pos:
            unique_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
            if voie.has_type_in_last_pos:  # il n'y a que le type dans le libelle
                # 1 er type
                # "GRAND RUE"
                voie_treated = self.assign_type_use_case.execute(voie, unique_type)
            else:
                # 1er type + lib
                # 'CHE DES SEMAPHORES'
                voie_treated = self.assign_type_lib_use_case.execute(voie, unique_type)

        else:
            voie = self.keep_types_without_article_adj_before_use_case.execute(voie)
            if len(voie.types_and_positions) == 1:   # il reste un type sans adj/det devant
                unique_type = self.generate_information_on_type_ordered_use_case.execute(voie, 1)
                unique_type_name_in_lib = (' ').join(voie.label_preproc[unique_type.position_start:unique_type.position_end+1])
                if (unique_type.type_name == unique_type_name_in_lib and
                        voie.has_type_in_last_pos):
                    voie_treated = self.assign_lib_type_use_case.execute(voie, unique_type)
                else:
                    if unique_type.is_longitudinal_or_agglomerant:
                        if not voie.has_type_in_last_pos:
                            # compl + 1er type + lib
                            # 'LE BAS FAURE RUE DE TOUL'
                            return self.assign_compl_type_lib_use_case.execute(voie, unique_type)
                        else:
                            # lib + 1er type
                            # 'HOCHE RUE'
                            return self.assign_lib_type_use_case.execute(voie)

            if not voie_treated:  # ce qu'il reste
                voie_treated = self.assign_lib_use_case.execute(voie)

        return voie_treated
