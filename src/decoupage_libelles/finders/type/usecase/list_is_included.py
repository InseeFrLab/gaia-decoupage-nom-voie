from typing import List


def list_is_included(sub: List[str], full: List[str]) -> bool:
    """Vérifie si `sub` apparaît comme sous-séquence contiguë dans `full`."""
    if not sub:
        return False
    n = len(sub)
    return any(full[i : i + n] == sub for i in range(len(full) - n + 1))
