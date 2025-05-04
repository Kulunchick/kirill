import random
from typing import List
from src.coursework.models.chain import Chain
from src.coursework.models.task import Task

class ChainGenerator:
    def __init__(self,
                 n: int,
                 min_size: int,
                 max_size: int,
                 min_t: int,
                 max_t: int,
                 min_u: int,
                 max_u: int):
        self.n = n
        self.min_size = min_size
        self.max_size = max_size
        self.min_t = min_t
        self.max_t = max_t
        self.min_u = min_u
        self.max_u = max_u

    def generate(self) -> List[Chain]:
        chains = []

        for i in range(self.n):
            chain_size = random.randint(self.min_size, self.max_size)

            # Створюємо список завдань з випадковими t та u
            tasks = [
                Task(
                    i=j,
                    t=random.randint(self.min_t, self.max_t),
                    u=random.randint(self.min_u, self.max_u)
                )
                for j in range(chain_size)
            ]

            chain = Chain(
                letter=chr(65 + i),
                tasks=tasks
            )

            chains.append(chain)

        return chains

    def generate_problems(self, n: int):
        problems = []
        for i in range(n):
            problems.append(self.generate())
        return problems

    def problems_generator(self):
        while True:
            yield self.generate()