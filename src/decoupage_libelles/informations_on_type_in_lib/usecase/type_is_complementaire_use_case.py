from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_complement.usecase.complement_finder_use_case import ComplementFinderUseCase


class TypeIsComplementaireUseCase:
    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        if len(infovoie.types_and_positions) == 0:
            types_compl = ComplementFinderUseCase.TYPES_COMPLEMENT_0
        else:
            types_compl = ComplementFinderUseCase.TYPES_COMPLEMENT_1_2

        information_on_type_ordered.is_complement = True if information_on_type_ordered.type_name in types_compl else False
        information_on_type_ordered.is_escalier_or_appartement = True if information_on_type_ordered.type_name in ComplementFinderUseCase.TYPES_APPART_ESC else False

        return information_on_type_ordered
