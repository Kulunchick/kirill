from dataclasses import dataclass

from src.coursework.models.task import Task


@dataclass
class Chain:
    letter: str
    tasks: list[Task]