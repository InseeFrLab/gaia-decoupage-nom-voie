from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from prepare_data.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase


class ApplyPonctuationPreprocessingOnTypeVoie:
    @inject
    def __init__(self, ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, libelle: str) -> str:
        lib_without_preprocessed_ponctuation = InfoVoie(label_raw=libelle)
        lib_with_preprocessed_ponctuation = self.ponctuation_preprocessor_use_case.execute(
            lib_without_preprocessed_ponctuation
            )
        return (" ").join(lib_with_preprocessed_ponctuation.label_preproc)