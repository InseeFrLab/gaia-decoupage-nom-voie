from typing import List

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class ComplementFinderUseCase:
    # TYPES_COMPLEMENT_0 = ["IMM", "IMMEUBLE", "BLOC", "BAT", "BATIMENT"]
    TYPES_COMPLEMENT_0 = ["BLOC", "ESC", "APPARTEMENT", "ESCALIER", "APRT"]

    # TYPES_COMPLEMENT_1_2 = ["PAVILLON", "PAV", "LDT", "IMM", "IM", "IMMEUBLE", "BLOC", "BAT", "BATIMENT"]
    TYPES_COMPLEMENT_1_2 = TYPES_COMPLEMENT_0

    TYPES_COMPLEMENT_IMMEUBLE = [
        "HLM",
        "CROIX",
        "RUE",
        "GALERIE",
        "COTE",
        "CENTRE",
        "HAMEAU",
        "DOMAINE",
        "MAISON",
        "CHALET",
        "LOTISSEMENT",
        "VILLA",
        "PARKING",
        "PARC",
        "RESIDENCE",
        "PLACE",
        "QUARTIER",
        "ESPACE",
    ]

    ORTHOGRAPHES_IMMEUBLE = ["IM", "IMM", "IMMEUBLE"]

    def execute(self, infovoie: InfoVoie, types_complement: List[str]) -> InfoVoie:
        for type_compl in types_complement:  # parcours de la liste de types "complément"
            if type_compl in infovoie.label_preproc:
                position_type = infovoie.label_preproc.index(type_compl)
                positions = (position_type, position_type)
                infovoie.types_and_positions[(type_compl, 1)] = positions
                infovoie.types_and_positions = dict(sorted(infovoie.types_and_positions.items(), key=lambda x: x[1][0]))
                return infovoie
