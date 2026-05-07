from dataclasses import dataclass
from typing import Optional


@dataclass
class InformationOnTypeOrdered:
    type_name: str
    order_in_lib: int
    position_start: int
    position_end: int
    occurence: int
    postag_before: Optional[str] = None
    word_before: Optional[str] = None
    word_after: Optional[str] = None
    type_after: Optional[str] = None
    has_adj_det_before: Optional[bool] = None
    is_in_middle_position: Optional[bool] = None
    is_in_penultimate_position: Optional[bool] = None
    is_longitudinal: Optional[bool] = None
    is_agglomerant: Optional[bool] = None
    is_longitudinal_or_agglomerant: Optional[bool] = None
    is_complement: Optional[bool] = None
    is_escalier_or_appartement: Optional[bool] = None
