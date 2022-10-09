from functools import wraps
from typing import Any, Callable, TypeVar, cast

from .timer import Timer

# TODO: Use ParamSpec et al when only python version >=3.10 is supported
F = TypeVar("F", bound=Callable[..., Any])


def timed(fn: F) -> F:
    """Decorates a function with a Timer, named by the function's module and qualified name"""
    name = f"{fn.__module__}.{fn.__qualname__}"

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with Timer(name):
            return fn(*args, **kwargs)

    return cast(F, wrapper)
