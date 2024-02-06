from injector import inject

from voie_classes.voie import Voie
from preprocessors.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase


class ApplyPonctuationPreprocessingOnTypeVoie:
    @inject
    def __init__(self, ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, libelle: str) -> str:
        lib_without_preprocessed_ponctuation = Voie(label_raw=libelle)
        lib_with_preprocessed_ponctuation = self.ponctuation_preprocessor_use_case.execute(
            lib_without_preprocessed_ponctuation
            )
        return (" ").join(lib_with_preprocessed_ponctuation.infolib.label_preproc)