from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from informations_on_lib.informations_on_type_and_lib.model.infolib import InfoLib

class TypeIsLongitudinalUseCase:

    TYPESLONGITUDINAUX = ['ROUTE',
                         'BOULEVARD',
                         'RUE',
                         'AVENUE',
                         'IMPASSE',
                         'CHEMIN',
                         'VOIE',
                         'PLACE',
                         'CHEMINEMENT',
                         'VOIE COMMUNALE']

    TYPESLONGITUDINAUX2 = ['ROUTE',
                           'BOULEVARD',
                           'RUE',
                           'AVENUE',
                           'IMPASSE',
                           'CHEMIN',
                           'VOIE',
                           'PLACE',
                           'CHEMINEMENT',
                           'VOIE COMMUNALE',
                           'ALLEE']

    def execute(self, infolib: InfoLib, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
            if len(infolib.types_and_positions) == 1:
                types_long = TypeIsLongitudinalUseCase.TYPESLONGITUDINAUX
            else:
                types_long = TypeIsLongitudinalUseCase.TYPESLONGITUDINAUX2
            
            if information_on_type_ordered.type_name in types_long:
                 information_on_type_ordered.is_longitudinal = True
            
            return information_on_type_ordered
