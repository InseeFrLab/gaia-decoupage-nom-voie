from dataclasses import dataclass
from typing import List, Optional

from informations_on_libelle_voie.domain.model.infovoie import InfoVoie
from finders.find_type.domain.usecase.generate_type_finder_utils_use_case import TypeFinderUtils

@dataclass
class TypeFinderObject:
    voie_big: InfoVoie
    type_data: TypeFinderUtils
    voie_sep: Optional[List[str]] = None
    voie: Optional[str] = None
