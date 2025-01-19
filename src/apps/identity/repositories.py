from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from django.contrib.auth.models import Group, GroupManager


class GroupRepositoryBase(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Group]:
        pass

    @abstractmethod
    def list(self) -> GroupManager[Group]:
        pass

    @abstractmethod
    def create(self, group: Group) -> None:
        pass

    @abstractmethod
    def update(self, group: Group) -> None:
        pass

    @abstractmethod
    def delete(self, group: Group) -> None:
        pass 
    
class GroupRepository(GroupRepositoryBase):
    def get_by_id(self, id: int) -> Optional[Group]:
        return Group.objects.get(id=id)

    def list(self) -> GroupManager[Group]:
        return Group.objects.order_by("name")

    def create(self, group: Group) -> None:
        group.save()

    def update(self, group: Group) -> None:
        group.save()

    def delete(self, group: Group) -> None:
        group.delete()