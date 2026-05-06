from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.find_type.usecase.detect_types_use_case import DetectTypesUseCase
from decoupage_libelles.finders.find_type.usecase.update_occurrences_by_order_use_case import UpdateOccurrencesByOrderUseCase
from decoupage_libelles.finders.find_type.usecase.remove_duplicates_use_case import RemoveDuplicatesUseCase
from decoupage_libelles.finders.find_type.usecase.remove_wrong_detections_use_case import RemoveWrongDetectionsUseCase
from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie


class TypeFinderUseCase:
    """
    Orchestre la détection du type de voie dans un libellé.

    Pipeline :
      1. Détecter toutes les variantes connues (mono et multi-mots)
      2. Si plusieurs types trouvés :
         a. Réordonner les occurrences par position d'apparition
         b. Supprimer les doublons adjacents (garde le type le plus long)
         c. Supprimer les faux positifs (type court inclus dans ou adjacent à un type long)

    Différence avec l'ancienne version :
      - Plus de distinction code / libellé : une seule passe de détection.
      - Plus de code intermédiaire (CODE) : on travaille directement avec le
        LIBELLE_CANONIQUE comme identifiant de référence.
      - Moins de use cases : 14 → 6.
    """

    def __init__(
        self,
        detect_types_use_case: DetectTypesUseCase = DetectTypesUseCase(),
        update_occurrences_by_order_use_case: UpdateOccurrencesByOrderUseCase = UpdateOccurrencesByOrderUseCase(),
        remove_duplicates_use_case: RemoveDuplicatesUseCase = RemoveDuplicatesUseCase(),
        remove_wrong_detections_use_case: RemoveWrongDetectionsUseCase = RemoveWrongDetectionsUseCase(),
    ):
        self.detect_types = detect_types_use_case
        self.update_occurrences = update_occurrences_by_order_use_case
        self.remove_duplicates = remove_duplicates_use_case
        self.remove_wrong_detections = remove_wrong_detections_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> InfoVoie:
        # Initialiser les vues du libellé prétraité
        type_finder_object.voie_sep = type_finder_object.voie_big.label_preproc[:]
        type_finder_object.voie = " ".join(type_finder_object.voie_big.label_preproc)

        # 1. Détection unifiée (variantes mono et multi-mots)
        type_finder_object = self.detect_types.execute(type_finder_object)

        # 2. Nettoyage si plusieurs types détectés
        if len(type_finder_object.voie_big.types_and_positions) > 1:
            type_finder_object = self.update_occurrences.execute(type_finder_object)
            type_finder_object = self.remove_duplicates.execute(type_finder_object)
            type_finder_object = self.remove_wrong_detections.execute(type_finder_object)

        return type_finder_object.voie_big
