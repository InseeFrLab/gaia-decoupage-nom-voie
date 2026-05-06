from decoupage_libelles.finders.find_type.model.type_finder_object import TypeFinderObject


class DetectTypesUseCase:
    """
    Détecte tous les types de voie dans le libellé, qu'il s'agisse d'une
    variante mono-mot (ex: 'AV', 'AVENUE', 'CHE') ou multi-mots
    (ex: 'ANCIEN CHEMIN', 'ANC CHEM').

    Remplace les deux anciens use cases séparés :
      - DetectCodifiedTypesUseCase   (cherchait les acronymes/codes)
      - DetectCompleteFormTypesUseCase (cherchait les formes développées)

    La logique est unifiée : on cherche toutes les variantes connues dans le
    libellé, sans distinguer si c'est un code ou un libellé.
    Le résultat associe directement le LIBELLE_CANONIQUE à ses positions.
    """

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        voie_sep = type_finder_object.voie_sep
        voie_str = type_finder_object.voie
        variante2canonique = type_finder_object.type_data.variante2canonique

        # Variantes mono-mot : recherche directe dans la liste de mots
        for variante in type_finder_object.type_data.variantes_mono:
            if variante not in voie_sep:
                continue
            canonique = variante2canonique[variante]
            positions = [i for i, mot in enumerate(voie_sep) if mot == variante]
            for pos in positions:
                self._add_detection(type_finder_object, canonique, pos, pos)

        # Variantes multi-mots : recherche de sous-séquence dans la liste de mots
        for variante in type_finder_object.type_data.variantes_multi:
            mots_variante = variante.split()
            n = len(mots_variante)
            if variante not in voie_str:
                continue
            for i in range(len(voie_sep) - n + 1):
                if voie_sep[i : i + n] == mots_variante:
                    canonique = variante2canonique[variante]
                    self._add_detection(type_finder_object, canonique, i, i + n - 1)

        return type_finder_object

    def _add_detection(
        self,
        type_finder_object: TypeFinderObject,
        canonique: str,
        pos_start: int,
        pos_end: int,
    ) -> None:
        """Ajoute une détection en gérant l'index d'occurrence (1, 2…)."""
        types_detectes = [t for t, _ in type_finder_object.voie_big.types_and_positions]
        occurence = 1 if canonique not in types_detectes else 2
        type_finder_object.voie_big.types_and_positions[(canonique, occurence)] = (pos_start, pos_end)
