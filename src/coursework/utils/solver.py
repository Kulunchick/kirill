import itertools
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

from src.coursework.models.chain import Chain
from src.coursework.models.task import Task


class MetricType(Enum):
    WAITING_TIME = auto()
    COMPLETION_TIME = auto()


@dataclass
class TaskSequence:
    chain_letter: str
    length: int
    ratio: float


@dataclass
class TaskMetrics:
    waiting_time: float
    completion_time: float
    is_average: bool


class NonUniqueRatioError(Exception):
    def __init__(self):
        message = "Знайдено декілька послідовностей з однаковим співвідношенням:\n"
        super().__init__(message)


class Solver:
    @staticmethod
    def calculate_task_metrics(tasks: list[Task], average: bool = False) -> TaskMetrics:
        if not tasks:
            return TaskMetrics(0, 0, average)

        current_time = 0

        metrics = []

        for task in tasks:
            metrics.append(TaskMetrics(
                waiting_time=task.u * current_time,
                completion_time=task.u * (current_time + task.t),
                is_average=False
            ))
            current_time += task.t

        if average:
            waiting_time = np.average([m.waiting_time for m in metrics])
            completion_time = np.average([m.completion_time for m in metrics])
        else:
            waiting_time = np.sum([m.waiting_time for m in metrics])
            completion_time = np.sum([m.completion_time for m in metrics])

        return TaskMetrics(waiting_time, completion_time, average)

    @staticmethod
    def get_metric_value(metrics: TaskMetrics, metric_type: MetricType) -> float:
        if metric_type == MetricType.WAITING_TIME:
            return metrics.waiting_time
        return metrics.completion_time

    @staticmethod
    def solve_with_chains(
            chains: list[Chain],
            reverse: bool = False,
            metric_type: MetricType = MetricType.COMPLETION_TIME,
            average: bool = False
    ) -> tuple[str, float]:
        sorted_chains = sorted(chains, key=lambda x: sum(task.t for task in x.tasks) / sum(task.u for task in x.tasks),
                               reverse=reverse)

        optimal_order = " ".join(chain.letter for chain in sorted_chains)
        tasks = itertools.chain.from_iterable(chain.tasks for chain in sorted_chains)

        metrics = Solver.calculate_task_metrics(tasks, average=average)
        criterion = Solver.get_metric_value(metrics, metric_type)

        return optimal_order, criterion

    @staticmethod
    def solve_with_tasks(
            chains: list[Chain],
            reverse: bool = False,
            metric_type: MetricType = MetricType.COMPLETION_TIME,
            average: bool = False
    ) -> tuple[str, float]:
        remaining_chains = deepcopy(chains)
        optimal_sequence = []

        while any(chain.tasks for chain in remaining_chains):
            sequences_by_ratio = defaultdict(list)
            best_ratio = np.inf if not reverse else -np.inf

            for chain_idx, chain in enumerate(remaining_chains):
                if not chain.tasks:
                    continue

                ratios = np.cumsum([task.t for task in chain.tasks]) / np.cumsum([task.u for task in chain.tasks])
                for seq_length, ratio in enumerate(ratios, start=1):
                    sequence = TaskSequence(
                        chain_letter=chain.letter,
                        length=seq_length,
                        ratio=ratio
                    )

                    sequences_by_ratio[ratio].append((sequence, chain_idx))

                    if (not reverse and ratio < best_ratio) or (reverse and ratio > best_ratio):
                        best_ratio = ratio

            best_sequences = sequences_by_ratio[best_ratio]
            # if len(best_sequences) > 1:
            #     raise NonUniqueRatioError()

            best_sequence, best_chain_index = best_sequences[0]
            chain = remaining_chains[best_chain_index]

            optimal_sequence.append((f"{chain.letter}", chain.tasks[:best_sequence.length]))

            remaining_chains[best_chain_index].tasks = chain.tasks[best_sequence.length:]

        optimal_order = " ".join(f"{chain[0]}{task.i}" for chain in optimal_sequence for task in chain[1])
        tasks = itertools.chain.from_iterable(chain[1] for chain in optimal_sequence)

        metrics = Solver.calculate_task_metrics(tasks, average=average)
        criterion = Solver.get_metric_value(metrics, metric_type)

        return optimal_order, criterion
