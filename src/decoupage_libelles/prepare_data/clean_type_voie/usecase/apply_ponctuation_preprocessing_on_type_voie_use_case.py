from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase


class ApplyPonctuationPreprocessingOnTypeVoie:
    def __init__(
        self,
        ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = PonctuationPreprocessorUseCase(),
    ):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self, libelle: str) -> str:
        lib_without_preprocessed_ponctuation = InfoVoie(label_origin=libelle)
        lib_with_preprocessed_ponctuation = self.ponctuation_preprocessor_use_case.execute(lib_without_preprocessed_ponctuation)
        return (" ").join(lib_with_preprocessed_ponctuation.label_preproc)
