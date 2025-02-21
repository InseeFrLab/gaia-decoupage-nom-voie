from dataclasses import dataclass
from typing import List, Optional

from decoupage_libelles.informations_on_libelle_voie.model.infovoie import InfoVoie
from decoupage_libelles.finders.find_type.usecase.generate_type_finder_utils_use_case import TypeFinderUtils


@dataclass
class TypeFinderObject:
    voie_big: InfoVoie
    type_data: TypeFinderUtils
    voie_sep: Optional[List[str]] = None
    voie: Optional[str] = None
