''' GUIDE STEPS. '''
from . reproportion.guide_reproportion import GUIDE_STEPS_REPROPORTION
from . datatransfer.guide_datatransfer import GUIDE_STEPS_DATATRANSFER
from . mdef.guide_mdef import GUIDE_STEPS_MDEF
from . lattices.guide_lattices import GUIDE_STEPS_LATTICES
from . actions.guide_actions import GUIDE_STEPS_ACTIONS
from . weights.guide_weights import GUIDE_STEPS_WEIGHTS
from . rig_settings.guide_rig_settings import GUIDE_STEPS_SETTINGS
from . shapekeys.guide_shapekeys import GUIDE_STEPS_SHAPEKEYS


''' ACTIONS ON END OF STEP. '''
from . reproportion.guide_reproportion_actions import end_of_step_action as reproportion_end_of_step_action
from . datatransfer.guide_datatransfer_actions import end_of_step_action as datatransfer_end_of_step_action
from . mdef.guide_mdef_actions import end_of_step_action as mdef_end_of_step_action
from . lattices.guide_lattices_actions import end_of_step_action as lattices_end_of_step_action
from . actions.guide_actions_actions import end_of_step_action as actions_end_of_step_action
from . weights.guide_weights_actions import end_of_step_action as weights_end_of_step_action
from . rig_settings.guide_rig_settings_actions import end_of_step_action as rig_settings_end_of_step_action
from . shapekeys.guide_shapekeys_actions import end_of_step_action as shapekeys_end_of_step_action


''' ENUM. '''
# Al agregar nuevas guías, importar el GUIDE_STEP... de esa guía
# y agregarlo a este Enum...
# NOTE: El nombre de la izquierda es el identificador, debe
# coincidir con el nombre de la guia ('guide_name') pero en mayus.
from enum import Enum
class GuideSteps(Enum):
    REPROPORTION = (GUIDE_STEPS_REPROPORTION, reproportion_end_of_step_action)
    DATATRANSFER = (GUIDE_STEPS_DATATRANSFER, datatransfer_end_of_step_action)
    MDEF         = (GUIDE_STEPS_MDEF        , mdef_end_of_step_action)
    LATTICES     = (GUIDE_STEPS_LATTICES    , lattices_end_of_step_action)
    ACTIONS      = (GUIDE_STEPS_ACTIONS     , actions_end_of_step_action)
    WEIGHTS      = (GUIDE_STEPS_WEIGHTS     , weights_end_of_step_action)
    RIG_SETTINGS = (GUIDE_STEPS_SETTINGS    , rig_settings_end_of_step_action)
    SHAPEKEYS    = (GUIDE_STEPS_SHAPEKEYS   , shapekeys_end_of_step_action)

    @classmethod
    def get_steps(cls, operator: 'BlenrigGuide_BaseOperator') -> tuple:
        return getattr(cls, operator.guide_name.upper())()

    @classmethod
    def get(cls,  idname: str) -> tuple:
        return getattr(cls, idname.upper(), None)()

    def __call__(self) -> tuple:
        return self.value
    
    def get_id(self) -> str:
        return self.name
