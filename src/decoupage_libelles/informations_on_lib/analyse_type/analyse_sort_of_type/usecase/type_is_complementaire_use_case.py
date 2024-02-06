from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib
from finders.find_complement.domain.usecase.complement_finder_use_case import ComplementFinderUseCase

class TypeIsComplementaireUseCase:

    def execute(self, infolib: InfoLib, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
            if len(infolib.types_and_positions) == 0:
                types_compl = ComplementFinderUseCase.TYPES_COMPLEMENT_0
            else:
                types_compl = ComplementFinderUseCase.TYPES_COMPLEMENT_1_2
            
            if information_on_type_ordered.type_name in types_compl:
                 information_on_type_ordered.is_complement = True
            
            return information_on_type_ordered
