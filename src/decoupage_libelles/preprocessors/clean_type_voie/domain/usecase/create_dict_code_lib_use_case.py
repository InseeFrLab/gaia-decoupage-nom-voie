from injector import inject

from preprocessors.clean_type_voie.domain.usecase.apply_ponctuation_preprocessing_on_type_voie_use_case import ApplyPonctuationPreprocessingOnTypeVoie


class CreatDictCodeLibUseCase:
     @inject
     def __init__(self, apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie):
           self.apply_ponctuation_preprocessing_on_type_voie_use_case: ApplyPonctuationPreprocessingOnTypeVoie = apply_ponctuation_preprocessing_on_type_voie_use_case


def create_dict_code_lib(self):
        """
        Crée un dictionnaire à partir du DataFrame en mappant les codes de
        type de voie à leurs libellés uniques.

        Cette méthode transforme le DataFrame 'type_voie_df', en un
        dictionnaire où chaque code de type de voie (CODE) est mappé à un
        libellé unique (LIBELLE). Les libellés complets sont nettoyés des
        ponctuations.

        Retourne :
            Un dictionnaire avec les codes de type de voie comme clés
            et les libellés correspondants comme valeurs.
        """
        self.type_voie_df['LIBELLE'] = self.type_voie_df['LIBELLE'].apply(self.apply_ponctuation_preprocessing_on_type_voie_use_case().execute)

        return self.type_voie_df.set_index('CODE')['LIBELLE'].to_dict()