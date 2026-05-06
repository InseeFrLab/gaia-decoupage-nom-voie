from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.prepare_data.ponctuation.usecase.ponctuation_preprocessor_use_case import PonctuationPreprocessorUseCase
from decoupage_libelles.finders.find_type.model.type_finder_utils import TypeFinderUtils


class GenerateTypeFinderUtilsUseCase:
    """
    Prépare les structures de recherche à partir du DataFrame de référence.

    Le DataFrame doit avoir les colonnes : ['LIBELLE_CANONIQUE', 'VARIANTE']
    Chaque variante (acronyme ou forme développée) est associée à un libellé
    canonique (la forme longue retenue comme référence).

    Plus besoin de CODE intermédiaire : le libellé canonique est la clé pivot.
    """

    def __init__(
        self,
        ponctuation_preprocessor_use_case: PonctuationPreprocessorUseCase = PonctuationPreprocessorUseCase(),
    ):
        self.ponctuation_preprocessor_use_case = ponctuation_preprocessor_use_case

    def execute(self, type_finder_utils: TypeFinderUtils) -> TypeFinderUtils:
        df = type_finder_utils.type_voie_df

        # Libellés canoniques uniques
        type_finder_utils.canoniques = set(df["LIBELLE_CANONIQUE"].unique())

        # Prétraitement des variantes (ponctuation, casse…)
        variante2preproc = {}
        variante2canonique = {}

        for _, row in df.iterrows():
            variante_raw = row["VARIANTE"]
            canonique = row["LIBELLE_CANONIQUE"]

            # Prétraitement de la variante
            info = InfoVoie(variante_raw)
            info = self.ponctuation_preprocessor_use_case.execute(info)
            variante_preproc = " ".join(info.label_preproc)

            variante2preproc[variante_raw] = variante_preproc
            variante2canonique[variante_preproc] = canonique

        # Option A : le canonique se reconnaît toujours lui-même,
        # sans avoir à l'inscrire explicitement dans le CSV.
        for canonique in type_finder_utils.canoniques:
            info = InfoVoie(canonique)
            info = self.ponctuation_preprocessor_use_case.execute(info)
            canonique_preproc = " ".join(info.label_preproc)
            variante2preproc.setdefault(canonique, canonique_preproc)
            variante2canonique.setdefault(canonique_preproc, canonique)

        type_finder_utils.variante2preproc = variante2preproc
        type_finder_utils.variante2canonique = variante2canonique

        # Séparer variantes mono-mot et multi-mots pour optimiser la recherche
        type_finder_utils.variantes_mono = [v for v in variante2canonique if len(v.split()) == 1]
        type_finder_utils.variantes_multi = [v for v in variante2canonique if len(v.split()) > 1]

        return type_finder_utils
