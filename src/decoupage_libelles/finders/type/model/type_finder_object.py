from dataclasses import dataclass, field
from typing import List, Optional

from decoupage_libelles.information_generators.libelle.model.infovoie import InfoVoie
from decoupage_libelles.finders.type.model.type_finder_utils import TypeFinderUtils


@dataclass
class TypeFinderObject:
    voie_big: InfoVoie
    type_data: TypeFinderUtils
    voie_sep: Optional[List[str]] = field(default_factory=list)
    voie: Optional[str] = ""
