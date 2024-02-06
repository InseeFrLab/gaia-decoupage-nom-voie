from typing import List

from voie_classes.decoupage_voie import DecoupageVoie


class ComplementFinderUseCase():
    TYPES_COMPLEMENT_0 = ['IMM', 'IMMEUBLE',
                         'BLOC',
                         'BAT', 'BATIMENT']

    TYPES_COMPLEMENT_1_2 = ['PAVILLON', 'PAV',
                            'LDT',
                            'IMM', 'IM', 'IMMEUBLE',
                            'BLOC',
                            'BAT', 'BATIMENT']

    TYPES_COMPLEMENT_IMMEUBLE = ['HLM',
                                'CROIX',
                                'RUE',
                                'GALERIE',
                                'COTE',
                                'CENTRE',
                                'HAMEAU',
                                'DOMAINE',
                                'MAISON',
                                'CHALET',
                                'LOTISSEMENT',
                                'VILLA',
                                'PARKING',
                                'PARC',
                                'RESIDENCE',
                                'PLACE',
                                'QUARTIER',
                                'ESPACE']

    ORTHOGRAPHES_IMMEUBLE = ['IM', 'IMM', 'IMMEUBLE']

    def execute(self,
                 voie: DecoupageVoie,
                 types_complement: list) -> DecoupageVoie:
        for type_compl in types_complement:  # parcours de la liste de types "complément"
            if type_compl in voie.infolib.label_preproc:
                position_type = voie.infolib.label_preproc.index(type_compl)
                positions = (position_type, position_type)
                voie.infolib.types_and_positions[(type_compl, 1)] = positions
                voie.infolib.sort_types_by_position()
                return voie
