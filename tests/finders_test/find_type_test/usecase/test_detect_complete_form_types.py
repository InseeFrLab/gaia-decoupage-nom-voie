from unittest.mock import MagicMock
from decoupage_libelles.finders.find_type.usecase.detect_complete_form_types_use_case import DetectCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.usecase.list_is_included_in_other_list_use_case import ListIsIncludedInOtherListUseCase
from decoupage_libelles.finders.find_type.usecase.detect_one_word_complete_form_types_use_case import DetectOneWordCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.usecase.detect_multi_words_complete_form_types_use_case import DetectMultiWordsCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import TypeFinderUtils


def use_case(
    detect_one_word_complete_form_types_use_case: DetectOneWordCompleteFormTypesUseCase = MagicMock(),
    detect_multi_words_complete_form_types_use_case: DetectMultiWordsCompleteFormTypesUseCase = MagicMock(),
    list_is_included_in_other_list_use_case: ListIsIncludedInOtherListUseCase = MagicMock(),
):
    return DetectCompleteFormTypesUseCase(detect_one_word_complete_form_types_use_case, detect_multi_words_complete_form_types_use_case, list_is_included_in_other_list_use_case)


def test_execute_type_en_un_mot():
    # Given
    type_lib = "type_lib_preproc"
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            types_lib_preproc=[type_lib],
            types_lib_preproc2types_lib_raw={type_lib: "type"},
            code2lib={"type": "type"},
            lib2code={"type": "type"},
        ),
        voie_sep=[type_lib],
        voie=[],
    )
    detect_one_word_complete_form_types_use_case = MagicMock()
    expected_res = TypeFinderObject(voie_big=None, type_data=None)
    detect_one_word_complete_form_types_use_case.execute.return_value = expected_res
    list_is_included_in_other_list_use_case = MagicMock()
    list_is_included_in_other_list_use_case.execute.return_value = True
    # When
    res = use_case(detect_one_word_complete_form_types_use_case, MagicMock(), list_is_included_in_other_list_use_case).execute(type_finder_object)
    # Then
    assert res == expected_res


def test_execute_type_en_plusieurs_mot():
    # Given
    type_lib = "type_lib_preproc mot2"
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            types_lib_preproc=[type_lib],
            types_lib_preproc2types_lib_raw={type_lib: "type"},
            code2lib={"type": "type"},
            lib2code={"type": "type"},
        ),
        voie_sep=[type_lib],
        voie=[type_lib],
    )
    detect_multi_words_complete_form_types_use_case = MagicMock()
    expected_res = TypeFinderObject(voie_big=None, type_data=None)
    detect_multi_words_complete_form_types_use_case.execute.return_value = expected_res
    list_is_included_in_other_list_use_case = MagicMock()
    list_is_included_in_other_list_use_case.execute.return_value = True
    # When
    res = use_case(MagicMock(), detect_multi_words_complete_form_types_use_case, list_is_included_in_other_list_use_case).execute(type_finder_object)
    # Then
    assert res == expected_res


def test_execute_type_vide():
    # Given
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            types_lib_preproc=[],
            types_lib_preproc2types_lib_raw={},
            code2lib={},
            lib2code={},
        ),
        voie_sep=[],
        voie=[],
    )
    list_is_included_in_other_list_use_case = MagicMock()
    list_is_included_in_other_list_use_case.execute.return_value = True
    # When
    res = use_case(MagicMock(), MagicMock, list_is_included_in_other_list_use_case).execute(type_finder_object)
    # Then
    assert res == type_finder_object
