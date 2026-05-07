from decoupage_libelles.finders.type.model.type_finder_object import TypeFinderObject
from decoupage_libelles.finders.type.usecase.remove_type_from_lib_use_case import RemoveTypeFromLibUseCase
from decoupage_libelles.information_generators.type_in_lib.usecase.generate_information_on_type_ordered_use_case import GenerateInformationOnTypeOrderedUseCase


class RemoveWrongDetectionsUseCase:
    """
    Fusionne la logique des deux anciens use cases :
      - RemoveWrongDetectedCodesUseCase  : supprime le type court quand il est
        inclus DANS le span d'un type plus long (ex: 'CHE' dans 'ANCIEN CHEMIN')
        → on garde le long, on ne retire rien du libellé.
      - RemoveWrongTypesInLibUseCase     : supprime le type court quand il est
        ADJACENT au type long qui le contient (ex: 'ROUTE' juste avant/après
        'ANCIENNE ROUTE') → on garde le long, on retire le court du libellé.

    Dans les deux cas, le principe est le même :
      - Comparer deux types consécutifs (par position).
      - Si le libellé du plus court est une sous-chaîne du plus long et que
        leurs spans se chevauchent ou sont adjacents → faux positif à supprimer.
    """

    def __init__(
        self,
        remove_type_from_lib_use_case: RemoveTypeFromLibUseCase = RemoveTypeFromLibUseCase(),
        generate_information_on_type_ordered_use_case: GenerateInformationOnTypeOrderedUseCase = GenerateInformationOnTypeOrderedUseCase(),
    ):
        self.remove_type_from_lib = remove_type_from_lib_use_case
        self.get_type_info = generate_information_on_type_ordered_use_case

    def execute(self, type_finder_object: TypeFinderObject) -> TypeFinderObject:
        voie_big = type_finder_object.voie_big
        n = len(voie_big.types_and_positions)

        a_supprimer_sans_retrait = []   # faux positif inclus dans un plus long
        a_supprimer_avec_retrait = []   # faux positif adjacent à un plus long

        i = 1
        while i < n:
            ti = self.get_type_info.execute(voie_big, i)
            ti1 = self.get_type_info.execute(voie_big, i + 1)

            if ti.type_name == ti1.type_name:
                i += 1
                continue

            # Identifier le plus court (moins d'espaces = moins de mots)
            if ti.type_name.count(" ") <= ti1.type_name.count(" "):
                court, long_ = ti, ti1
            else:
                court, long_ = ti1, ti

            nom_court = court.type_name
            nom_long = long_.type_name
            s_court, e_court = court.position_start, court.position_end
            s_long, e_long = long_.position_start, long_.position_end

            if nom_court not in nom_long:
                i += 1
                continue

            # Cas 1 : le span du court est entièrement inclus dans le span du long
            if s_long <= s_court and e_court <= e_long:
                a_supprimer_sans_retrait.append((nom_court, court.occurence))

            # Cas 2 : adjacent (le court colle au long et en fait partie sémantiquement)
            elif (s_court - e_long == 1) or (s_long - e_court == 1):
                a_supprimer_avec_retrait.append(
                    ((nom_court, court.occurence), s_court, e_court)
                )

            i += 1

        # Supprimer les faux positifs inclus (pas de retrait du libellé)
        for key in set(a_supprimer_sans_retrait):
            voie_big.types_and_positions.pop(key, None)

        # Supprimer les faux positifs adjacents (avec retrait du libellé)
        for key, s, e in set(a_supprimer_avec_retrait):
            voie_big.types_and_positions.pop(key, None)
            voie_big = self.remove_type_from_lib.execute(voie_big, s, e)

        type_finder_object.voie_big = voie_big
        return type_finder_object
