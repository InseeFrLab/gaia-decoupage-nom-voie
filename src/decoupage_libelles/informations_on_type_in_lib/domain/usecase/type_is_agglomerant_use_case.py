from informations_on_type_in_lib.domain.model.information_on_type_ordered import InformationOnTypeOrdered

class TypeIsAgglomerantUseCase:

    TYPESAGGLOMERANTS = ['DOMAINE',
                         'MAISON',
                         'CITE',
                         'LOTISSEMENT',
                         'AIRE',
                         "ZONE D'ACTIVITES",
                         "ZONE D'AMENAGEMENT CONCERTE",
                         "ZONE D'AMENAGEMENT DIFFERE",
                         'ZONE INDUSTRIELLE',
                         'ZONE A URBANISER EN PRIORITE',
                         "ZONE D'ACTIVITES ECONOMIQUES",
                         'COUR',
                         'HAMEAU',
                         'PLACETTE',
                         'BOURG',
                         'HLM',
                         'QUARTIER',
                         'CLOS',
                         'TERRAIN',
                         'ENCLOS',
                         'RESIDENCE',
                         'ZONE',
                         'VILLAGE',
                         'CARREFOUR',
                         'COIN',
                         'ILOT',
                         'VILLE',
                         'FAUBOURG',
                         'PARKING',
                         'FERME',
                         'VALLEE']

    def execute(self, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
            if information_on_type_ordered.type_name in TypeIsAgglomerantUseCase.TYPESAGGLOMERANTS:
                 information_on_type_ordered.is_agglomerant = True
            
            return information_on_type_ordered

