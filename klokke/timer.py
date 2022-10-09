import time
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, DefaultDict, List, Optional


def _pad_newlines(s: str) -> str:
    return s.replace("\n", "\n  ")


class TimerError(Exception):
    pass


class TimerContext:
    _global_instance = None

    def __init__(self) -> None:
        """
        Creates a TimerContext instance.
        (NB: you generally do not want to instantiate this yourself)
        """
        self._stack: List["Timer"] = []

    def add_to_stack(self, timer: "Timer") -> None:
        self._stack.append(timer)

    def pop_stack(self) -> "Timer":
        return self._stack.pop()

    def current_timer(self) -> Optional["Timer"]:
        if self._stack:
            return self._stack[-1]
        return None

    @classmethod
    def get(cls) -> "TimerContext":
        if cls._global_instance is None:
            cls._global_instance = TimerContext()
            cls._global_instance.add_to_stack(Timer("__global_timer__"))
        return cls._global_instance


@dataclass
class Elapsed:
    n_executed: int = field(default=0)
    total_time: float = field(default=0.0)
    sub_timers: DefaultDict[str, "Elapsed"] = field(
        default_factory=lambda: defaultdict(Elapsed)
    )

    def __add__(self, other: "Elapsed") -> "Elapsed":
        merged_sub_timers = deepcopy(self.sub_timers)
        for k, v in other.sub_timers.items():
            merged_sub_timers[k] += v
        return Elapsed(
            n_executed=self.n_executed + other.n_executed,
            total_time=self.total_time + other.total_time,
            sub_timers=merged_sub_timers,
        )

    def __str__(self) -> str:
        s = f"{self.total_time} seconds"
        if self.sub_timers:
            s += "\nOf which:\n  " + "\n  ".join(
                f"{n}: {_pad_newlines(str(t))}" for n, t in self.sub_timers.items()
            )
        return s


@dataclass
class Timer:
    name: str
    elapsed: Elapsed = field(init=False, default_factory=Elapsed)
    start: float = field(init=False, default=0.0)
    end: float = field(init=False, default=0.0)

    def __str__(self) -> str:
        s = f"{self.name}: {self.elapsed}"
        return s

    def __enter__(self) -> "Timer":
        context = TimerContext.get()
        context.add_to_stack(self)
        self.start = time.time()
        self.elapsed.n_executed += 1
        return self

    def __exit__(self, *_: Any, **__: Any) -> None:
        self.end = time.time()
        self.elapsed.total_time += self.end - self.start
        context = TimerContext.get()
        # Check that current timer context is ourselves,
        # otherwise something terrible is happening
        current_timer_stack = context.pop_stack()
        if current_timer_stack is not self:
            raise TimerError(
                f"Popping context stack on exiting timer with id {id(self)}"
                f" resulted in popping timer of id {id(current_timer_stack)}"
            )
        parent_timer = context.current_timer()
        if parent_timer is not None:
            parent_timer.track_sub_timer(self)

    def track_sub_timer(self, sub_timer: "Timer") -> None:
        self.elapsed.sub_timers[sub_timer.name] += sub_timer.elapsed
