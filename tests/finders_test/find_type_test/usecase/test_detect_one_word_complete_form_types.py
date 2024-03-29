from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.detect_one_word_complete_form_types_use_case import DetectOneWordCompleteFormTypesUseCase
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


def use_case():
    return DetectOneWordCompleteFormTypesUseCase()


def test_execute_liste_vide():
    # Given
    type_detect = ""
    type_lib = ""
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
        voie_sep=[],
    )
    # When
    res = use_case().execute(type_detect, type_lib, type_finder_object)
    # Then
    assert res == type_finder_object


def test_execute():
    # Given
    type_detect = "type_detect"
    type_lib = "voie"
    type_finder_object = TypeFinderObject(
        voie_big=InfoVoie(
            label_origin="",
            label_raw="",
            complement="",
            types_and_positions={},
        ),
        type_data=TypeFinderUtils(
            type_voie_df=None,
            code2lib={},
        ),
        voie_sep=["voie", "voie", "mot"],
    )
    # When
    res = use_case().execute(type_detect, type_lib, type_finder_object)
    # Then
    assert res == type_finder_object
    assert {("type_detect", 1): (0, 0), ("type_detect", 2): (1, 1)} == type_finder_object.voie_big.types_and_positions
