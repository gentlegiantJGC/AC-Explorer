from pyUbiForge2.api.game import SubclassBaseFile
from .Event import Event as _Event


class NotorietyEvent(SubclassBaseFile):
    ResourceType = 0x044ABAA2
    ParentResourceType = _Event.ResourceType
    parent: _Event