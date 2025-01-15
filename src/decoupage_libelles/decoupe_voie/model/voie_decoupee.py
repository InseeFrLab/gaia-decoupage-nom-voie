from dataclasses import dataclass
from typing import Optional


@dataclass
class VoieDecoupee:
    label_origin: str
    type_assigned: Optional[str] = ""
    label_assigned: Optional[str] = ""
    compl_assigned: Optional[str] = ""
    num_assigned: Optional[str] = None
    indice_rep: Optional[str] = None
    compl2: Optional[str] = None
