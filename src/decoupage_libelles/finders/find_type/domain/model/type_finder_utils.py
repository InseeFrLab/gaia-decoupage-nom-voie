from dataclasses import dataclass
from typing import List, Optional
import pandas as pd


@dataclass
class TypeFinderUtils:
    type_voie_df: pd.DataFrame
    code2lib: dict
    codes: Optional[List[str]] = None
    lib2code: Optional[dict] = None
    types_lib_preproc: Optional[List[str]] = None
    types_lib_preproc2types_lib_raw: Optional[dict] = None
