from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.no_type.usecase.handle_no_type_complement_use_case import HandleNoTypeComplUseCase


def use_case(
    gen_info_lib=MagicMock(),
    gen_info_type=MagicMock(),
    assign_lib_compl=MagicMock(),
    assign_type_lib=MagicMock(),
    assign_compl_type_lib=MagicMock(),
    assign_lib=MagicMock(),
    suppress_article=MagicMock(),
) -> HandleNoTypeComplUseCase:
    return HandleNoTypeComplUseCase(
        gen_info_lib, gen_info_type, assign_lib_compl,
        assign_type_lib, assign_compl_type_lib, assign_lib, suppress_article,
    )


def _make_first_type(
    is_in_middle_position=False,
    has_adj_det_before=False,
    word_after="ERNEST",
    is_escalier_or_appartement=False,
):
    t = MagicMock()
    t.is_in_middle_position = is_in_middle_position
    t.has_adj_det_before = has_adj_det_before
    t.word_after = word_after
    t.is_escalier_or_appartement = is_escalier_or_appartement
    return t


def _voie(label: str = "BAT JEAN LAMOUR") -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = label.upper().split()
    v.types_and_positions = {("BATIMENT", 1): (0, 0)}
    return v


def test_suppress_article_appele_en_premier():
    # Given
    suppress_mock = MagicMock()
    suppress_mock.execute.side_effect = lambda v: v
    gen_info_mock = MagicMock()
    gen_info_mock.execute.side_effect = lambda v, **kw: v
    first_type = _make_first_type()
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    assign_lib_mock = MagicMock(); assign_lib_mock.execute.return_value = "lib"
    # When
    use_case(gen_info_mock, gen_type_mock, assign_lib=assign_lib_mock, suppress_article=suppress_mock).execute(_voie())
    # Then — suppress appelé avant gen_info
    suppress_mock.execute.assert_called_once()
    gen_info_mock.execute.assert_called_once()
    assert suppress_mock.execute.call_args[0][0] is not None


def test_nlp_toujours_active():
    # Given
    gen_info_mock = MagicMock()
    gen_info_mock.execute.side_effect = lambda v, **kw: v
    first_type = _make_first_type()
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    assign_lib_mock = MagicMock(); assign_lib_mock.execute.return_value = "lib"
    voie = _voie()
    # When
    use_case(gen_info_mock, gen_type_mock, assign_lib=assign_lib_mock).execute(voie)
    # Then — apply_nlp_model=True obligatoire (nécessaire pour has_adj_det_before)
    gen_info_mock.execute.assert_called_once_with(voie, apply_nlp_model=True)


def test_type_milieu_sans_adj_word_after_fictif_retourne_lib_compl():
    # Given — "LE TILLET BAT A" : BAT en milieu, pas d'adj avant, word_after = "A" (fictif)
    first_type = _make_first_type(is_in_middle_position=True, has_adj_det_before=False, word_after="A")
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_lib_compl_mock = MagicMock(); assign_lib_compl_mock.execute.return_value = "lib_compl"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_lib_compl=assign_lib_compl_mock).execute(_voie())
    # Then
    assert res == "lib_compl"
    assign_lib_compl_mock.execute.assert_called_once()


def test_type_milieu_sans_adj_escalier_retourne_lib_compl():
    # Given — type escalier en milieu → lib + compl
    first_type = _make_first_type(is_in_middle_position=True, has_adj_det_before=False, is_escalier_or_appartement=True)
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_lib_compl_mock = MagicMock(); assign_lib_compl_mock.execute.return_value = "lib_compl"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_lib_compl=assign_lib_compl_mock).execute(_voie())
    # Then
    assert res == "lib_compl"


def test_type_milieu_sans_adj_word_after_non_fictif_retourne_compl_type_lib():
    # Given — "LE TILLET BAT ERNEST RENAN" : BAT en milieu, word_after = "ERNEST" (non fictif)
    first_type = _make_first_type(is_in_middle_position=True, has_adj_det_before=False, word_after="ERNEST")
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_compl_type_lib_mock = MagicMock(); assign_compl_type_lib_mock.execute.return_value = "compl_type_lib"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_compl_type_lib=assign_compl_type_lib_mock).execute(_voie())
    # Then
    assert res == "compl_type_lib"
    assign_compl_type_lib_mock.execute.assert_called_once_with(_voie(), first_type)


def test_type_non_milieu_escalier_retourne_lib():
    # Given — "APPARTEMENT JEAN LAMOUR" : pas en milieu, is_escalier_or_appartement=True
    first_type = _make_first_type(is_in_middle_position=False, is_escalier_or_appartement=True)
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_lib_mock = MagicMock(); assign_lib_mock.execute.return_value = "lib"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_lib=assign_lib_mock).execute(_voie())
    # Then
    assert res == "lib"


def test_type_non_milieu_non_escalier_retourne_type_lib():
    # Given — "BAT JEAN LAMOUR" : pas en milieu, pas escalier
    first_type = _make_first_type(is_in_middle_position=False, is_escalier_or_appartement=False)
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_type_lib_mock = MagicMock(); assign_type_lib_mock.execute.return_value = "type_lib"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_type_lib=assign_type_lib_mock).execute(_voie())
    # Then
    assert res == "type_lib"


def test_type_milieu_avec_adj_avant_non_escalier_retourne_type_lib():
    # Given — type en milieu MAIS avec adj/det avant → traité comme non-milieu
    first_type = _make_first_type(is_in_middle_position=True, has_adj_det_before=True, is_escalier_or_appartement=False)
    gen_type_mock = MagicMock(); gen_type_mock.execute.return_value = first_type
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    assign_type_lib_mock = MagicMock(); assign_type_lib_mock.execute.return_value = "type_lib"
    # When
    res = use_case(gen_info_mock, gen_type_mock, assign_type_lib=assign_type_lib_mock).execute(_voie())
    # Then
    assert res == "type_lib"
