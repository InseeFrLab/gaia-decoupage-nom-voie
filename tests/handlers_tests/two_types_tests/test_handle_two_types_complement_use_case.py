from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase


def _voie() -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = ["RUE", "HOCHE", "BAT", "BLEU"]
    v.types_and_positions = {("RUE", 1): (0, 0), ("BATIMENT", 1): (2, 2)}
    return v


def use_case(
    gen_info=None,
    assign_lib=None,
    two_long_agglo=None,
    first_compl=None,
    second_compl=None,
    third_compl=None,
) -> HandleTwoTypesComplUseCase:
    # None par défaut pour éviter le piège des MagicMock() partagés entre appels
    return HandleTwoTypesComplUseCase(
        gen_info or MagicMock(),
        assign_lib or MagicMock(),
        two_long_agglo or MagicMock(),
        first_compl or MagicMock(),
        second_compl or MagicMock(),
        third_compl or MagicMock(),
    )


def test_second_retour_toujours_none():
    # Given — 2ème valeur de retour toujours None
    gen_info_mock = MagicMock()
    gen_info_mock.execute.side_effect = lambda v, apply_nlp_model=False: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = "result"
    # When
    _, voie_to_treat = use_case(gen_info_mock, two_long_agglo=two_long_mock).execute(_voie())
    # Then
    assert voie_to_treat is None


def test_generate_info_lib_appele_sans_nlp():
    # Given
    gen_info_mock = MagicMock()
    gen_info_mock.execute.side_effect = lambda v, apply_nlp_model=False: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = "result"
    voie = _voie()
    # When
    use_case(gen_info_mock, two_long_agglo=two_long_mock).execute(voie)
    # Then
    gen_info_mock.execute.assert_called_once_with(voie, apply_nlp_model=False)