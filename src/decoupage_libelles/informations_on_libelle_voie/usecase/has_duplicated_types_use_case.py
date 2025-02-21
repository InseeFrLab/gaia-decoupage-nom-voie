from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class HasDuplicatedTypesUseCase:
    def execute(self, infovoie: InfoVoie) -> InfoVoie:
        infovoie.has_duplicated_types = False
        if infovoie.types_and_positions:
            for __, occurence in infovoie.types_and_positions.keys():
                if occurence > 1:
                    infovoie.has_duplicated_types = True
        return infovoie
