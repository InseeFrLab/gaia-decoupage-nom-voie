import pandas as pd
from injector import inject

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from prepare_data.ponctuation.domain.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from finders.find_type.domain.model.type_finder_utils import TypeFinderUtils


class GenerateTypeFinderUtilsUseCase:
    @inject
    def __init__(self, ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase):
        self.ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = ponctuation_preprocessor_use_case

    def execute(self,
                type_finder_utils: TypeFinderUtils,) -> TypeFinderUtils:

        types_lib = type_finder_utils.type_voie_df['LIBELLE'].tolist()
        types_lib = [InfoVoie(lib_raw) for lib_raw in types_lib]
        for i, lib in enumerate(types_lib):
            lib = self.ponctuation_preprocessor_use_case.execute(lib)
            types_lib[i] = lib

        types_lib_preproc_raw = [[(' ').join(elt.label_preproc),
                                  elt.label_raw] for elt in types_lib]
        types_lib_preproc2types_lib_raw = dict(types_lib_preproc_raw)

        types_lib_preproc = [(' ').join(elt.label_preproc) for elt in types_lib]
        types_lib_preproc = [elt for elt in types_lib_preproc if elt not in type_finder_utils.codes]

        type_finder_utils.types_lib_preproc2types_lib_raw = types_lib_preproc2types_lib_raw
        type_finder_utils.types_lib_preproc = types_lib_preproc

        return type_finder_utils
