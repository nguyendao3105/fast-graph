from .base import BaseModelClass

class Group(BaseModelClass):
    groupname: str
    number_of_member: int
    max_number_of_member: int

class FreeLanceGroup(Group):
    pass

class StaticGroup(Group):
    pass