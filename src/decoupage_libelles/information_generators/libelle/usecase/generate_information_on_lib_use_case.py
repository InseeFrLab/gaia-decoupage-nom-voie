from decoupage_libelles.information_generators.libelle.usecase.position_of_types_in_lib_analyser_use_case import PositionOfTypesInLibAnalyserUseCase
from decoupage_libelles.information_generators.libelle.usecase.apply_postagging_use_case import ApplyPostaggingUseCase
from decoupage_libelles.information_generators.libelle.usecase.has_duplicated_types_use_case import HasDuplicatedTypesUseCase
from decoupage_libelles.information_generators.libelle.usecase.types_detected_use_case import TypesDetectedUseCase
from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie


class GenerateInformationOnLibUseCase:
    def __init__(
        self,
        apply_postagging_use_case: ApplyPostaggingUseCase = ApplyPostaggingUseCase(),
        position_of_types_in_lib_analyser_use_case: PositionOfTypesInLibAnalyserUseCase = PositionOfTypesInLibAnalyserUseCase(),
        has_duplicated_types_use_case: HasDuplicatedTypesUseCase = HasDuplicatedTypesUseCase(),
        types_detected_use_case: TypesDetectedUseCase = TypesDetectedUseCase(),
    ):
        self.apply_postagging_use_case: ApplyPostaggingUseCase = apply_postagging_use_case
        self.position_of_types_in_lib_analyser_use_case: PositionOfTypesInLibAnalyserUseCase = position_of_types_in_lib_analyser_use_case
        self.has_duplicated_types_use_case: HasDuplicatedTypesUseCase = has_duplicated_types_use_case
        self.types_detected_use_case: TypesDetectedUseCase = types_detected_use_case

    def execute(self, infovoie: InfoVoie, apply_nlp_model: bool = False) -> InfoVoie:
        if apply_nlp_model:
            self.apply_postagging_use_case.execute(infovoie)
        self.position_of_types_in_lib_analyser_use_case.execute(infovoie)
        self.has_duplicated_types_use_case.execute(infovoie)
        self.types_detected_use_case.execute(infovoie)
        return infovoie
