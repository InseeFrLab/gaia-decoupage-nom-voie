from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class InfoVoie:
    label_raw: str
    label_preproc: Optional[List[str]] = field(default_factory=list)
    types_and_positions: Optional[dict] = field(default_factory=dict)
    label_postag: Optional[List[str]] = None
    types_detected: Optional[List[str]] = None
    nb_types_detected: Optional[List[int]] = 0
    has_type_in_first_pos: Optional[bool] = False
    has_type_in_second_pos: Optional[bool]  = False
    has_type_in_last_pos: Optional[bool]  = False
    has_duplicated_types: Optional[bool]  = False
