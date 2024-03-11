from decoupage_libelles.informations_on_type_in_lib.model.information_on_type_ordered import InformationOnTypeOrdered
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class TypeIsLongitudinalUseCase:
    TYPESLONGITUDINAUX = ["ROUTE", "BOULEVARD", "RUE", "AVENUE", "IMPASSE", "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE"]

    TYPESLONGITUDINAUX2 = ["ROUTE", "BOULEVARD", "RUE", "AVENUE", "IMPASSE", "CHEMIN", "VOIE", "PLACE", "CHEMINEMENT", "VOIE COMMUNALE", "ALLEE"]

    def execute(self, infovoie: InfoVoie, information_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
        if len(infovoie.types_and_positions) == 1:
            types_long = TypeIsLongitudinalUseCase.TYPESLONGITUDINAUX
        else:
            types_long = TypeIsLongitudinalUseCase.TYPESLONGITUDINAUX2

        information_on_type_ordered.is_longitudinal = True if information_on_type_ordered.type_name in types_long else False

        information_on_type_ordered.is_longitudinal_or_agglomerant = True if information_on_type_ordered.is_agglomerant or information_on_type_ordered.is_longitudinal else False

        return information_on_type_ordered
