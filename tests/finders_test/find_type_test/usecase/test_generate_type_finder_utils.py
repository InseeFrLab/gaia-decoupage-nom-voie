from unittest.mock import MagicMock
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import GenerateTypeFinderUtilsUseCase
from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
import pandas as pd


def use_case(ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = MagicMock()):
    return GenerateTypeFinderUtilsUseCase(ponctuation_preprocessor_use_case)


def test_execute():
    # Given
    type_voie_df_data = {
        "LIBELLE": ["Rue", "Avenue", "Boulevard", "Place", "Impasse"],
        "CODE": ["R", "AV", "BD", "PL", "IMP"],
    }
    type_voie_df = pd.DataFrame(type_voie_df_data)

    type_finder_utils = TypeFinderUtils(
        type_voie_df=type_voie_df,
        code2lib={},
    )
    ponctuation_preprocessor_use_case = MagicMock()
    ponctuation_preprocessor_use_case.execute.return_value = InfoVoie(label_origin="", label_raw="", complement="")
    # When
    result = use_case(ponctuation_preprocessor_use_case).execute(type_finder_utils)

    # Then
    assert isinstance(result, TypeFinderUtils)
    assert len(result.codes) == 5
    assert isinstance(result.lib2code, dict)
    assert len(result.types_lib_preproc2types_lib_raw) == 1
    assert len(result.types_lib_preproc) == 5
