import argparse

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.preprocessing.pipeline.usecase.voie_lib_preprocessor_use_case import VoieLibPreprocessorUseCase
from decoupage_libelles.information_generators.libelle.usecase.apply_postagging_use_case import ApplyPostaggingUseCase


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Applique le modèle NLP sur le libellé de voie"
    )

    parser.add_argument(
        "voie_ou_appliquer",
        type=str,
        help="Libellé de voie où appliquer le modele NLP",
    )

    args = parser.parse_args()
    voie_lib_preprocessor_use_case: VoieLibPreprocessorUseCase = VoieLibPreprocessorUseCase()

    infovoie = InfoVoie(label_origin=args.voie_ou_appliquer)
    voie_preprocessed = voie_lib_preprocessor_use_case.execute([infovoie])[0]

    apply_postagging_use_case: ApplyPostaggingUseCase = ApplyPostaggingUseCase()

    r = apply_postagging_use_case.execute(voie_preprocessed)

    print(f"Les étiquettes synthaxiques sont respectivement : {r.label_postag}")
