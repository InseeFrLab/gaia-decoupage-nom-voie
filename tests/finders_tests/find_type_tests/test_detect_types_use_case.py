from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.usecase.detect_types_use_case import DetectTypesUseCase


def _make_type_finder_object(
    label_preproc: list,
    variantes_mono: list,
    variantes_multi: list,
    variante2canonique: dict,
) -> TypeFinderObject:
    voie_big = InfoVoie()
    voie_big.label_preproc = label_preproc
    type_data = TypeFinderUtils()
    type_data.variantes_mono = variantes_mono
    type_data.variantes_multi = variantes_multi
    type_data.variante2canonique = variante2canonique
    obj = TypeFinderObject(voie_big=voie_big, type_data=type_data)
    obj.voie_sep = label_preproc[:]
    obj.voie = " ".join(label_preproc)
    return obj


def test_aucune_variante_connue():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["LES", "LILAS"],
        variantes_mono=["AV", "RUE"],
        variantes_multi=[],
        variante2canonique={"AV": "AVENUE", "RUE": "RUE"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {}


def test_variante_mono_detectee():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "HUGO"],
        variantes_mono=["AV"],
        variantes_multi=[],
        variante2canonique={"AV": "AVENUE"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("AVENUE", 1): (0, 0)}


def test_variante_mono_position_correcte():
    # Given — variante en milieu de libellé
    obj = _make_type_finder_object(
        label_preproc=["VICTOR", "AV", "HUGO"],
        variantes_mono=["AV"],
        variantes_multi=[],
        variante2canonique={"AV": "AVENUE"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("AVENUE", 1): (1, 1)}


def test_variante_multi_detectee():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["ANC", "CHEM", "DES", "PINS"],
        variantes_mono=[],
        variantes_multi=["ANC CHEM"],
        variante2canonique={"ANC CHEM": "ANCIEN CHEMIN"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("ANCIEN CHEMIN", 1): (0, 1)}


def test_variante_multi_position_correcte():
    # Given — variante multi-mots en fin de libellé
    obj = _make_type_finder_object(
        label_preproc=["DES", "PINS", "ANC", "CHEM"],
        variantes_mono=[],
        variantes_multi=["ANC CHEM"],
        variante2canonique={"ANC CHEM": "ANCIEN CHEMIN"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {("ANCIEN CHEMIN", 1): (2, 3)}


def test_deux_variantes_differentes_detectees():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "RUE", "HUGO"],
        variantes_mono=["AV", "RUE"],
        variantes_multi=[],
        variante2canonique={"AV": "AVENUE", "RUE": "RUE"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert ("AVENUE", 1) in res.voie_big.types_and_positions
    assert ("RUE", 1) in res.voie_big.types_and_positions


def test_meme_variante_deux_fois_deux_occurrences():
    # Given
    obj = _make_type_finder_object(
        label_preproc=["AV", "VICTOR", "AV", "HUGO"],
        variantes_mono=["AV"],
        variantes_multi=[],
        variante2canonique={"AV": "AVENUE"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert ("AVENUE", 1) in res.voie_big.types_and_positions
    assert ("AVENUE", 2) in res.voie_big.types_and_positions


def test_variante_multi_absente_du_libelle():
    # Given — "ANC CHEM" n'est pas dans le libellé
    obj = _make_type_finder_object(
        label_preproc=["VICTOR", "HUGO"],
        variantes_mono=[],
        variantes_multi=["ANC CHEM"],
        variante2canonique={"ANC CHEM": "ANCIEN CHEMIN"},
    )
    # When
    res = DetectTypesUseCase().execute(obj)
    # Then
    assert res.voie_big.types_and_positions == {}
