from injector import inject

from informations_on_lib.analyse_type.analyse_linguistique.usecase.postag_before_type_use_case import PostagBeforeTypeUseCase
from informations_on_lib.informations_on_type_and_lib.model.information_on_type_ordered import InformationOnTypeOrdered

class HasAdjDetBeforeTypeUseCase:
    POSTAG = ['DET', 'ADJ', 'ADP', 'CCONJ']

    @inject
    def __init__(self, postag_before_type_use_case: PostagBeforeTypeUseCase):
        self.postag_before_type_use_case: PostagBeforeTypeUseCase = postag_before_type_use_case
        
    def execute(self, info_on_type_ordered: InformationOnTypeOrdered) -> InformationOnTypeOrdered:
            postag = info_on_type_ordered.postag_before
            if postag in HasAdjDetBeforeTypeUseCase.POSTAG:
                info_on_type_ordered.has_adj_det_before = True
            
            return info_on_type_ordered