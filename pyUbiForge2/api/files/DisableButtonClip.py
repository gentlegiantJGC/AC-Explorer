from pyUbiForge2.api.game import SubclassBaseFile
from .Clip import Clip as _Clip


class DisableButtonClip(SubclassBaseFile):
    ResourceType = 0x84ACB000
    ParentResourceType = _Clip.ResourceType
    parent: _Clip