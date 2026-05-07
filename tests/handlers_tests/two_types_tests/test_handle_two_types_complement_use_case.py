from unittest.mock import MagicMock

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.handlers.two_types.usecase.handle_two_types_complement_use_case import HandleTwoTypesComplUseCase


def _voie() -> InfoVoie:
    v = InfoVoie()
    v.label_preproc = ["RUE", "HOCHE", "BAT", "BLEU"]
    v.types_and_positions = {("RUE", 1): (0, 0), ("BATIMENT", 1): (2, 2)}
    return v


def use_case(
    gen_info=MagicMock(),
    assign_lib=MagicMock(),
    two_long_agglo=MagicMock(),
    first_compl=MagicMock(),
    second_compl=MagicMock(),
    third_compl=MagicMock(),
) -> HandleTwoTypesComplUseCase:
    return HandleTwoTypesComplUseCase(
        gen_info, assign_lib, two_long_agglo, first_compl, second_compl, third_compl
    )


def test_premier_use_case_qui_retourne_gagne():
    # Given — two_long_agglo retourne un résultat
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = "long_agglo_result"
    first_mock = MagicMock(); second_mock = MagicMock(); third_mock = MagicMock()
    # When
    result, _ = use_case(gen_info_mock, MagicMock(), two_long_mock, first_mock, second_mock, third_mock).execute(_voie())
    # Then — les suivants ne sont pas appelés
    assert result == "long_agglo_result"
    first_mock.execute.assert_not_called()
    second_mock.execute.assert_not_called()
    third_mock.execute.assert_not_called()


def test_cascade_jusqua_assign_lib_si_aucun_ne_retourne():
    # Given — tous les use cases spécialisés retournent None
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = None
    first_mock = MagicMock(); first_mock.execute.return_value = None
    second_mock = MagicMock(); second_mock.execute.return_value = None
    third_mock = MagicMock(); third_mock.execute.return_value = None
    assign_lib_mock = MagicMock(); assign_lib_mock.execute.return_value = "lib_result"
    # When
    result, _ = use_case(gen_info_mock, assign_lib_mock, two_long_mock, first_mock, second_mock, third_mock).execute(_voie())
    # Then — fallback sur assign_lib
    assert result == "lib_result"
    assign_lib_mock.execute.assert_called_once()


def test_second_retour_toujours_none():
    # Given — ComplImmeubleBeforeTypeUseCase retiré → 2ème valeur toujours None
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = "result"
    # When
    _, voie_to_treat = use_case(gen_info_mock, MagicMock(), two_long_mock).execute(_voie())
    # Then
    assert voie_to_treat is None


def test_generate_info_lib_appele_sans_nlp():
    # Given
    gen_info_mock = MagicMock(); gen_info_mock.execute.side_effect = lambda v, **kw: v
    two_long_mock = MagicMock(); two_long_mock.execute.return_value = "result"
    voie = _voie()
    # When
    use_case(gen_info_mock, MagicMock(), two_long_mock).execute(voie)
    # Then — apply_nlp_model=False
    gen_info_mock.execute.assert_called_once_with(voie, apply_nlp_model=False)
