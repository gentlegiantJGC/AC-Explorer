from pyUbiForge2.api.game import SubclassBaseFile
from .CLAbstract import CLAbstract as _CLAbstract


class CLHorseInterceptEntity(SubclassBaseFile):
    ResourceType = 0x176791EE
    ParentResourceType = _CLAbstract.ResourceType
    parent: _CLAbstract