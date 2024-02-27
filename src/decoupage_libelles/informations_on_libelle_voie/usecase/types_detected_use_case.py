from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class TypesDetectedUseCase:
    def execute(self, infovoie: InfoVoie) -> InfoVoie:
        types_detected = [type_lib for type_lib, __ in infovoie.types_and_positions.keys()]
        if types_detected:
            infovoie.types_detected = types_detected
        return infovoie
