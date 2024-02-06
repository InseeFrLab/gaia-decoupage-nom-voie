from injector import inject

from informations_on_lib.analyse_type.analyse_position.usecase.position_of_types_in_lib_analyser_use_case import PositionOfTypesInLibAnalyserUseCase
from informations_on_lib.analyse_type.analyse_linguistique.usecase.apply_postagging_use_case import ApplyPostaggingUseCase
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib


class GenerateInformationOnLibUseCase:
    @inject
    def __init__(self, apply_postagging_use_case: ApplyPostaggingUseCase, position_of_types_in_lib_analyser_use_case: PositionOfTypesInLibAnalyserUseCase):
        self.apply_postagging_use_case: ApplyPostaggingUseCase = apply_postagging_use_case
        self.position_of_types_in_lib_analyser_use_case: PositionOfTypesInLibAnalyserUseCase = position_of_types_in_lib_analyser_use_case

    def execute(self, infolib: InfoLib, apply_nlp_model: bool = False):
        self.position_of_types_in_lib_analyser_use_case.execute(infolib)
        if apply_nlp_model:
            self.apply_postagging_use_case.execute(infolib)