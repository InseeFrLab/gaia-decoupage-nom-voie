def list_incluse(
        petite_liste: list,
        grande_liste: list
        ):
    if not petite_liste:
        return False

    len_petite = len(petite_liste)
    len_grande = len(grande_liste)

    for i in range(len_grande - len_petite + 1):
        if grande_liste[i:i + len_petite] == petite_liste:
            return True

    return False


def is_last_position(
        liste: list,
        position: int
        ):
    return position == len(liste)-1
