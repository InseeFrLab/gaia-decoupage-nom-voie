from .config.type_voie_decoupage_launcher import TypeVoieDecoupageLauncher

_launcher = TypeVoieDecoupageLauncher()


def decoupe_voies(list_voies: list[str]):
    return _launcher.execute(voies_data=list_voies)
