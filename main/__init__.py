from enum import Enum


class StudentGroupsType(Enum):
    MKM = "МКМ"
    MKIS = "МКИС"

    @classmethod
    def getEnumTuple(self):
        return tuple(map(lambda group: group.value, self))


class GroupsType():
    StudentGroups = StudentGroupsType.getEnumTuple()


s = GroupsType()
print(s.StudentGroups)


