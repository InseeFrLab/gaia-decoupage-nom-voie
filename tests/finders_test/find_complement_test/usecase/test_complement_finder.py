from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase


def test_complement_finder_no_type():
    # Given
    voie = InfoVoie(label_origin="LE TILLET BAT A", label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={})
    # When
    use_case = ComplementFinderUseCase()
    voie_treated = use_case.execute(voie, ["BAT"])
    # Then
    voie_target = InfoVoie(label_origin="LE TILLET BAT A", label_raw="LE TILLET BAT A", label_preproc=["LE", "TILLET", "BAT", "A"], types_and_positions={("BAT", 1): (2, 2)})
    assert voie_target == voie_treated


def test_complement_finder_one_type():
    # Given
    voie = InfoVoie(label_origin="LE TILLET BAT A", label_raw="IMM L ANJOU AVE DE VLAMINC", label_preproc=["IMM", "L", "ANJOU", "AVE", "DE", "VLAMINC"], types_and_positions={("AVE", 1): (3, 3)})
    # When
    use_case = ComplementFinderUseCase()
    voie_treated = use_case.execute(voie, ["IMM"])
    # Then
    voie_target = InfoVoie(
        label_origin="IMM L ANJOU AVE DE VLAMINC",
        label_raw="IMM L ANJOU AVE DE VLAMINC",
        label_preproc=["IMM", "L", "ANJOU", "AVE", "DE", "VLAMINC"],
        types_and_positions={("IMM", 1): (0, 0), ("AVE", 1): (3, 3)},
    )
    assert voie_target == voie_treated


def test_complement_finder_returns_empty_voie():
    # Given
    voie = InfoVoie()
    # When
    use_case = ComplementFinderUseCase()
    voie_treated = use_case.execute(voie, ["BAT"])
    # Then
    assert voie_treated == voie_treated
