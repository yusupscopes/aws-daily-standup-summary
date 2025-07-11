from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple
from app.domain.model.task import Task


class TasksQueryService(ABC):
    @abstractmethod
    def get_today_tasks(self) -> List[Task]:
        """Returns all tasks due today"""
        pass
