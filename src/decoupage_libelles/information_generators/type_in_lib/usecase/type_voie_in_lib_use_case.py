from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.information_generators.type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered


class TypeVoieInLibUseCase:
    def execute(
        self,
        infovoie: InfoVoie,
        information_on_type_ordered: InformationOnTypeOrdered
    ) -> InformationOnTypeOrdered:

        pos_start = information_on_type_ordered.position_start
        pos_end = information_on_type_ordered.position_end+1
        type_name_in_lib = (' ').join(infovoie.label_preproc[pos_start:pos_end])
        information_on_type_ordered.type_name_in_lib = type_name_in_lib

        return information_on_type_ordered
