from typing import Union


class DeterminMinAndMaxStrAccordingToCountOfEspacesInStrsUseCase:
    def execute(self, str1: str, str2: str) -> Union[str, str]:
        espaces_str1 = str1.count(" ")
        espaces_str2 = str2.count(" ")

        dict_two_strs = {str1: espaces_str1, str2: espaces_str2}

        str_min = min(dict_two_strs, key=dict_two_strs.get)
        str_max = max(dict_two_strs, key=dict_two_strs.get)

        if str_min == str_max:
            dict_two_strs_filtred = {cle: valeur for cle, valeur in dict_two_strs.items() if cle != str_min}
            str_max = next(iter(dict_two_strs_filtred.keys()))

        return str_min, str_max
