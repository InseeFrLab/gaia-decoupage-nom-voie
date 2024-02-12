from informations_on_libelle_voie.domain.model.infovoie import InfoVoie


class TypesDetectedUseCase:
    def types_detected(self, infovoie: InfoVoie) -> InfoVoie:
        types_detected = [type_lib for type_lib, __ in infovoie.types_and_positions.keys()]
        if types_detected:
            infovoie.types_detected = types_detected
            infovoie.nb_types_detected = len(types_detected)
        return infovoie