from injector import Module, singleton, Binder

from prepare_data.clean_type_voie.domain.usecase.type_voie_majic_preprocessor_use_case import TypeVoieMajicPreprocessorUseCase
from prepare_data.clean_voie_lib_and_find_types.domain.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from handle_voies_no_type.domain.usecase.no_type_voies_handler_use_case import NoTypeVoiesHandlerUseCase
from handle_voies_one_type.domain.usecase.one_type_voies_handler_use_case import OneTypeVoiesHandlerUseCase
from handle_voies_two_types.domain.usecase.two_types_voies_handler_use_case import TwoTypesVoiesHandlerUseCase
from handle_voies_three_types_and_more.domain.usecase.three_types_and_more_voies_handler_use_case import ThreeTypesAndMoreVoiesHandlerUseCase
from config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher

from informations_on_libelle_voie.domain.usecase.apply_postagging_use_case import ApplyPostaggingUseCase
from informations_on_libelle_voie.domain.usecase.generate_information_on_lib_use_case import GenerateInformationOnLibUseCase
from informations_on_libelle_voie.domain.usecase.get_words_between_use_case import GetWordsBetweenUseCase
from informations_on_libelle_voie.domain.usecase.has_duplicated_types_use_case import HasDuplicatedTypesUseCase
from informations_on_libelle_voie.domain.usecase.nlp_model_singleton import NLPModelSingleton
from informations_on_libelle_voie.domain.usecase.types_detected_use_case import TypesDetectedUseCase
from informations_on_libelle_voie.domain.usecase.position_of_types_in_lib_analyser_use_case import PositionOfTypesInLibAnalyserUseCase

from informations_on_type_in_lib.domain.usecase.find_order_of_apparition_in_lib_use_case import FindOrderOfApparitionInLibUseCase
from informations_on_type_in_lib.domain.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase
from informations_on_type_in_lib.domain.usecase.is_in_middle_pos_use_case import IsInMiddlePositionUseCase
from informations_on_type_in_lib.domain.usecase.is_in_penultimate_position_use_case import IsInPenultimatePositionUseCase
from informations_on_type_in_lib.domain.usecase.order_type_in_lib_use_case import OrderTypeInLib
from informations_on_type_in_lib.domain.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase
from informations_on_type_in_lib.domain.usecase.type_after_type_use_case import TypeAfterTypeUseCase
from informations_on_type_in_lib.domain.usecase.word_before_type_use_case import WordBeforeTypeUseCase
from informations_on_type_in_lib.domain.usecase.word_after_type_use_case import WordAfterTypeUseCase
from informations_on_type_in_lib.domain.usecase.type_is_agglomerant_use_case import TypeIsAgglomerantUseCase
from informations_on_type_in_lib.domain.usecase.type_is_complementaire_use_case import TypeIsComplementaireUseCase
from informations_on_type_in_lib.domain.usecase.type_is_longitudinal_use_case import TypeIsLongitudinalUseCase

from prepare_data.clean_type_voie.domain.usecase.enrich_reduced_lib_use_case import EnrichReducedLibUseCase
from prepare_data.clean_type_voie.domain.usecase.choose_unique_lib_use_case import ChooseUniqueLibUseCase
from prepare_data.clean_type_voie.domain.usecase.new_codes_lib_use_case import NewCodesLibUseCase
from prepare_data.clean_type_voie.domain.usecase.create_dict_code_lib_use_case import CreatDictCodeLibUseCase
from prepare_data.clean_type_voie.domain.usecase.new_spelling_for_code_use_case import NewSpellingForCodeUseCase
from prepare_data.clean_type_voie.domain.usecase.apply_ponctuation_preprocessing_on_type_voie_use_case import ApplyPonctuationPreprocessingOnTypeVoie

from prepare_data.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from prepare_data.ponctuation.domain.usecase.separate_words_with_apostrophe_and_supress_ponctuation_use_case import SeparateWordsWithApostropheAndSupressPonctuationUseCase
from prepare_data.ponctuation.domain.usecase.suppress_ponctuation_in_words_use_case import SuppressPonctuationInWordsUseCase

from prepare_data.clean_voie_lib_and_find_types.domain.usecase.apply_ponctuation_preprocessor_on_voies_use_case import ApplyPonctuationPreprocessorOnVoiesUseCase
from prepare_data.clean_voie_lib_and_find_types.domain.usecase.apply_type_finder_on_voies_use_case import ApplyTypeFinderOnVoiesUseCase

from finders.find_type.domain.usecase.type_finder_use_case import TypeFinderUseCase
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import GenerateTypeFinderUtilsUseCase
from finders.find_type.domain.usecase.detect_codified_types_use_case import DetectCodifiedTypesUseCase
from finders.find_type.domain.usecase.detect_complete_form_types_use_case import DetectCompleteFormTypesUseCase
from finders.find_type.domain.usecase.update_occurences_by_order_of_apparition_use_case import UpdateOccurencesByOrderOfApparitionUseCase
from finders.find_type.domain.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from finders.find_type.domain.usecase.remove_wrong_detected_codes_use_case import RemoveWrongDetectedCodesUseCase
from finders.find_type.domain.usecase.detect_multi_words_complete_form_types_use_case import DetectMultiWordsCompleteFormTypesUseCase
from finders.find_type.domain.usecase.detect_one_word_complete_form_types_use_case import DetectOneWordCompleteFormTypesUseCase
from finders.find_type.domain.usecase.determin_min_and_max_str_according_to_count_of_espaces_in_strs_use_case import DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase
from finders.find_type.domain.usecase.find_position_of_word_in_sentence_list_use_case import FindPositionOfWordInSentenceListUseCase
from finders.find_type.domain.usecase.find_positions_of_word_in_sentence_str_use_case import FindPositionsOfWordInSentenceStrUseCase
from finders.find_type.domain.usecase.list_is_included_in_other_list_use_case import ListIsIncludedInOtherListUseCase
from finders.find_type.domain.usecase.remove_type_from_lib_and_types_use_case import RemoveTypeFromLibAndTypesUseCase

from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase
from finders.find_complement.domain.usecase.apply_complement_finder_on_voies_use_case import ApplyComplementFinderOnVoiesUseCase

from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_one_type_use_case import DetectTypeFictifForOneTypeUseCase
from finders.find_voie_fictive.domain.usecase.detect_type_fictif_for_multi_types_use_case import DetectTypeFictifForMultiTypesUseCase
from finders.find_voie_fictive.domain.usecase.voie_fictive_finder_use_case import VoieFictiveFinderUseCase
from finders.find_voie_fictive.domain.usecase.apply_voie_fictive_finder_on_voies_use_case import ApplyVoieFictiveFinderOnVoiesUseCase

from decoupe_voie.domain.usecase.assign_compl_type_lib_compl_use_case import AssignComplTypeLibComplUseCase
from decoupe_voie.domain.usecase.assign_compl_type_lib_use_case import AssignComplTypeLibUseCase
from decoupe_voie.domain.usecase.assign_lib_compl_use_case import AssignLibComplUseCase
from decoupe_voie.domain.usecase.assign_lib_type_use_case import AssignLibTypeUseCase
from decoupe_voie.domain.usecase.assign_lib_use_case import AssignLibUseCase
from decoupe_voie.domain.usecase.assign_type_lib_compl_use_case import AssignTypeLibComplUseCase
from decoupe_voie.domain.usecase.assign_type_lib_use_case import AssignTypeLibUseCase

from handle_voies_no_type.domain.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase

from handle_voies_one_type.domain.usecase.compl_type_in_first_or_last_pos_use_case import ComplTypeInFirstOrLastPosUseCase
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_middle_pos_use_case import ComplTypeInFirstOrMiddlePosUseCase
from handle_voies_one_type.domain.usecase.compl_type_in_first_or_second_pos_use_case import ComplTypeInFirstOrSecondPosUseCase
from handle_voies_one_type.domain.usecase.handle_one_type_complement_use_case import HandleOneTypeComplUseCase
from handle_voies_one_type.domain.usecase.handle_one_type_not_compl_not_fictif_use_case import HandleOneTypeNotComplNotFictifUseCase
from handle_voies_one_type.domain.usecase.type_agglo_not_first_pos_use_case import TypeAggloNotFirstPosUseCase
from handle_voies_one_type.domain.usecase.type_long_not_first_pos_use_case import TypeLongNotFirstPosUseCase
from handle_voies_one_type.domain.usecase.type_route_not_first_pos_use_case import TypeRouteNotFirstPosUseCase

from handle_voies_two_types.domain.usecase.compl_first_type_compl_use_case import ComplFirstTypeComplUseCase
from handle_voies_two_types.domain.usecase.compl_immeuble_before_type_use_case import ComplImmeubleBeforeTypeUseCase
from handle_voies_two_types.domain.usecase.compl_second_type_compl_use_case import ComplSecondTypeComplUseCase
from handle_voies_two_types.domain.usecase.compl_third_type_compl_use_case import ComplThirdTypeComplUseCase
from handle_voies_two_types.domain.usecase.compl_two_types_long_or_agglo_use_case import ComplTwoTypesLongOrAggloUseCase
from handle_voies_two_types.domain.usecase.handle_has_type_in_first_pos_use_case import HandleHasTypeInFirstPosUseCase
from handle_voies_two_types.domain.usecase.handle_no_type_in_first_pos_use_case import HandleNoTypeInFirstPosUseCase
from handle_voies_two_types.domain.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase
from handle_voies_two_types.domain.usecase.handle_two_types_voie_fictive_use_case import HandleTwoTypesVoieFictiveUseCase


class ConfigurerInjection(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(EnrichReducedLibUseCase, to=EnrichReducedLibUseCase, scope=singleton)
        binder.bind(ChooseUniqueLibUseCase, to=ChooseUniqueLibUseCase, scope=singleton)
        binder.bind(NewCodesLibUseCase, to=NewCodesLibUseCase, scope=singleton)
        binder.bind(CreatDictCodeLibUseCase, to=CreatDictCodeLibUseCase, scope=singleton)
        binder.bind(NewSpellingForCodeUseCase, to=NewSpellingForCodeUseCase, scope=singleton)

        binder.bind(ApplyPonctuationPreprocessorOnVoiesUseCase, to=ApplyPonctuationPreprocessorOnVoiesUseCase, scope=singleton)
        binder.bind(SeparateWordsWithApostropheAndSupressPonctuationUseCase, to=SeparateWordsWithApostropheAndSupressPonctuationUseCase, scope=singleton)
        binder.bind(SuppressPonctuationInWordsUseCase, to=SuppressPonctuationInWordsUseCase, scope=singleton)
        binder.bind(PonctuationPreprocessorUseCase, to=PonctuationPreprocessorUseCase, scope=singleton)
        binder.bind(ApplyPonctuationPreprocessingOnTypeVoie, to=ApplyPonctuationPreprocessingOnTypeVoie, scope=singleton)
        
        binder.bind(ApplyTypeFinderOnVoiesUseCase, to=ApplyTypeFinderOnVoiesUseCase, scope=singleton)
        binder.bind(GenerateTypeFinderUtilsUseCase, to=GenerateTypeFinderUtilsUseCase, scope=singleton)
        binder.bind(TypeFinderUseCase, to=TypeFinderUseCase, scope=singleton)
        binder.bind(DetectCodifiedTypesUseCase, to=DetectCodifiedTypesUseCase, scope=singleton)
        binder.bind(DetectCompleteFormTypesUseCase, to=DetectCompleteFormTypesUseCase, scope=singleton)
        binder.bind(UpdateOccurencesByOrderOfApparitionUseCase, to=UpdateOccurencesByOrderOfApparitionUseCase, scope=singleton)
        binder.bind(RemoveDuplicatesUseCase, to=RemoveDuplicatesUseCase, scope=singleton)
        binder.bind(RemoveWrongDetectedCodesUseCase, to=RemoveWrongDetectedCodesUseCase, scope=singleton)
        binder.bind(DetectMultiWordsCompleteFormTypesUseCase, to=DetectMultiWordsCompleteFormTypesUseCase, scope=singleton)
        binder.bind(DetectOneWordCompleteFormTypesUseCase, to=DetectOneWordCompleteFormTypesUseCase, scope=singleton)
        binder.bind(DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase, to=DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase, scope=singleton)
        binder.bind(FindPositionOfWordInSentenceListUseCase, to=FindPositionOfWordInSentenceListUseCase, scope=singleton)
        binder.bind(FindPositionsOfWordInSentenceStrUseCase, to=FindPositionsOfWordInSentenceStrUseCase, scope=singleton)
        binder.bind(ListIsIncludedInOtherListUseCase, to=ListIsIncludedInOtherListUseCase, scope=singleton)
        binder.bind(RemoveTypeFromLibAndTypesUseCase, to=RemoveTypeFromLibAndTypesUseCase, scope=singleton)

        binder.bind(TypeVoieMajicPreprocessorUseCase, to=TypeVoieMajicPreprocessorUseCase, scope=singleton)
        binder.bind(VoieLibPreprocessorUseCase, to=VoieLibPreprocessorUseCase, scope=singleton)

        binder.bind(ApplyPostaggingUseCase, to=ApplyPostaggingUseCase, scope=singleton)
        binder.bind(GenerateInformationOnLibUseCase, to=GenerateInformationOnLibUseCase, scope=singleton)
        binder.bind(GetWordsBetweenUseCase, to=GetWordsBetweenUseCase, scope=singleton)
        binder.bind(HasDuplicatedTypesUseCase, to=HasDuplicatedTypesUseCase, scope=singleton)
        binder.bind(NLPModelSingleton, to=NLPModelSingleton, scope=singleton)
        binder.bind(TypesDetectedUseCase, to=TypesDetectedUseCase, scope=singleton)
        binder.bind(PositionOfTypesInLibAnalyserUseCase, to=PositionOfTypesInLibAnalyserUseCase, scope=singleton)

        binder.bind(FindOrderOfApparitionInLibUseCase, to=FindOrderOfApparitionInLibUseCase, scope=singleton)
        binder.bind(GenerateInformationOnTypeOrderedUseCase, to=GenerateInformationOnTypeOrderedUseCase, scope=singleton)
        binder.bind(IsInMiddlePositionUseCase, to=IsInMiddlePositionUseCase, scope=singleton)
        binder.bind(IsInPenultimatePositionUseCase, to=IsInPenultimatePositionUseCase, scope=singleton)
        binder.bind(OrderTypeInLib, to=OrderTypeInLib, scope=singleton)
        binder.bind(TypeAfterTypeUseCase, to=TypeAfterTypeUseCase, scope=singleton)
        binder.bind(WordBeforeTypeUseCase, to=WordBeforeTypeUseCase, scope=singleton)
        binder.bind(WordAfterTypeUseCase, to=WordAfterTypeUseCase, scope=singleton)
        binder.bind(TypeIsAgglomerantUseCase, to=TypeIsAgglomerantUseCase, scope=singleton)
        binder.bind(TypeIsComplementaireUseCase, to=TypeIsComplementaireUseCase, scope=singleton)
        binder.bind(TypeIsLongitudinalUseCase, to=TypeIsLongitudinalUseCase, scope=singleton)
        binder.bind(PostagBeforeTypeUseCase, to=PostagBeforeTypeUseCase, scope=singleton)
        
        binder.bind(ComplementFinderUseCase, to=ComplementFinderUseCase, scope=singleton)
        binder.bind(ApplyComplementFinderOnVoiesUseCase, to=ApplyComplementFinderOnVoiesUseCase, scope=singleton)

        binder.bind(DetectTypeFictifForOneTypeUseCase, to=DetectTypeFictifForOneTypeUseCase, scope=singleton)
        binder.bind(DetectTypeFictifForMultiTypesUseCase, to=DetectTypeFictifForMultiTypesUseCase, scope=singleton)
        binder.bind(VoieFictiveFinderUseCase, to=VoieFictiveFinderUseCase, scope=singleton)
        binder.bind(ApplyVoieFictiveFinderOnVoiesUseCase, to=ApplyVoieFictiveFinderOnVoiesUseCase, scope=singleton)

        binder.bind(HandleNoTypeComplUseCase, to=HandleNoTypeComplUseCase, scope=singleton)
        binder.bind(NoTypeVoiesHandlerUseCase, to=NoTypeVoiesHandlerUseCase, scope=singleton)

        binder.bind(ComplTypeInFirstOrLastPosUseCase, to=ComplTypeInFirstOrLastPosUseCase, scope=singleton)
        binder.bind(ComplTypeInFirstOrMiddlePosUseCase, to=ComplTypeInFirstOrMiddlePosUseCase, scope=singleton)
        binder.bind(ComplTypeInFirstOrSecondPosUseCase, to=ComplTypeInFirstOrSecondPosUseCase, scope=singleton)
        binder.bind(HandleOneTypeComplUseCase, to=HandleOneTypeComplUseCase, scope=singleton)
        binder.bind(HandleOneTypeNotComplNotFictifUseCase, to=HandleOneTypeNotComplNotFictifUseCase, scope=singleton)
        binder.bind(TypeAggloNotFirstPosUseCase, to=TypeAggloNotFirstPosUseCase, scope=singleton)
        binder.bind(TypeLongNotFirstPosUseCase, to=TypeLongNotFirstPosUseCase, scope=singleton)
        binder.bind(TypeRouteNotFirstPosUseCase, to=TypeRouteNotFirstPosUseCase, scope=singleton)
        binder.bind(OneTypeVoiesHandlerUseCase, to=OneTypeVoiesHandlerUseCase, scope=singleton)

        binder.bind(ComplFirstTypeComplUseCase, to=ComplFirstTypeComplUseCase, scope=singleton)
        binder.bind(ComplImmeubleBeforeTypeUseCase, to=ComplImmeubleBeforeTypeUseCase, scope=singleton)
        binder.bind(ComplSecondTypeComplUseCase, to=ComplSecondTypeComplUseCase, scope=singleton)
        binder.bind(ComplThirdTypeComplUseCase, to=ComplThirdTypeComplUseCase, scope=singleton)
        binder.bind(ComplTwoTypesLongOrAggloUseCase, to=ComplTwoTypesLongOrAggloUseCase, scope=singleton)
        binder.bind(HandleHasTypeInFirstPosUseCase, to=HandleHasTypeInFirstPosUseCase, scope=singleton)
        binder.bind(HandleNoTypeInFirstPosUseCase, to=HandleNoTypeInFirstPosUseCase, scope=singleton)
        binder.bind(HandleTwoTypesComplUseCase, to=HandleTwoTypesComplUseCase, scope=singleton)
        binder.bind(HandleTwoTypesVoieFictiveUseCase, to=HandleTwoTypesVoieFictiveUseCase, scope=singleton)
        binder.bind(TwoTypesVoiesHandlerUseCase, to=TwoTypesVoiesHandlerUseCase, scope=singleton)

        binder.bind(ThreeTypesAndMoreVoiesHandlerUseCase, to=ThreeTypesAndMoreVoiesHandlerUseCase, scope=singleton)

        binder.bind(AssignComplTypeLibComplUseCase, to=AssignComplTypeLibComplUseCase, scope=singleton)
        binder.bind(AssignComplTypeLibUseCase, to=AssignComplTypeLibUseCase, scope=singleton)
        binder.bind(AssignLibComplUseCase, to=AssignLibComplUseCase, scope=singleton)
        binder.bind(AssignLibTypeUseCase, to=AssignLibTypeUseCase, scope=singleton)
        binder.bind(AssignLibUseCase, to=AssignLibUseCase, scope=singleton)
        binder.bind(AssignTypeLibComplUseCase, to=AssignTypeLibComplUseCase, scope=singleton)
        binder.bind(AssignTypeLibUseCase, to=AssignTypeLibUseCase, scope=singleton)

        binder.bind(TypeVoieDecoupageLauncher, to=TypeVoieDecoupageLauncher, scope=singleton)
