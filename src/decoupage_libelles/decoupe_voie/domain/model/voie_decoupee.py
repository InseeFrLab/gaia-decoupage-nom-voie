from dataclasses import dataclass
from typing import Optional


@dataclass
class VoieDecoupee:
    label_raw: str
    type_assigned: Optional[str] = None
    label_assigned: Optional[str] = None
    compl_assigned: Optional[str] = None
    num_assigned: Optional[str] = None
