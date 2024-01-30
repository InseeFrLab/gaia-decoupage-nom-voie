import pandas as pd

from voie_classes.voie import Voie
from preprocessors.ponctuation.domain.use_case.ponctuation_preprocessor_use_case import PonctuationPreprocessor
from constants.constant_lists import ponctuations
from finders.find_type.domain.model.type_finder_utils import TypeFinderUtils


class GenerateTypeFinderUtilsUseCase:
    def execute(self,
                type_finder_utils: TypeFinderUtils,):

        types_lib = type_finder_utils.type_voie_df['LIBELLE'].tolist()
        types_lib = [Voie(lib_raw) for lib_raw in types_lib]
        for i, lib in enumerate(types_lib):
            lib = PonctuationPreprocessor(lib, ponctuations).run()
            types_lib[i] = lib

        types_lib_preproc_raw = [[(' ').join(elt.infolib.label_preproc),
                                  elt.label_raw] for elt in types_lib]
        types_lib_preproc2types_lib_raw = dict(types_lib_preproc_raw)

        types_lib_preproc = [(' ').join(elt.infolib.label_preproc) for elt in types_lib]
        types_lib_preproc = [elt for elt in types_lib_preproc if elt not in type_finder_utils.codes]

        type_finder_utils.types_lib_preproc2types_lib_raw = types_lib_preproc2types_lib_raw
        type_finder_utils.types_lib_preproc = types_lib_preproc

        return type_finder_utils
