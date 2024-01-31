from dataclasses import dataclass
from typing import List, Optional
import pandas as pd


@dataclass
class TypeFinderUtils:
    type_voie_df: pd.DataFrame
    code2lib: dict
    codes: List[str] = list(set(type_voie_df['CODE'].tolist()))
    lib2code: dict = type_voie_df.set_index('LIBELLE')['CODE'].to_dict()
    types_lib_preproc: Optional[List[str]] = None
    types_lib_preproc2types_lib_raw: Optional[dict] = None
