from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Union, cast, overload

from .timer import Timer

# TODO: Use ParamSpec et al when only python version >=3.10 is supported
F = TypeVar("F", bound=Callable[..., Any])


@overload
def timed(__fn: F) -> F:
    ...


@overload
def timed(*, name: Optional[str] = None, **timer_kwargs: Any) -> Callable[[F], F]:
    ...


def timed(
    __fn: Optional[F] = None, *, name: Optional[str] = None, **timer_kwargs: Any
) -> Union[F, Callable[[F], F]]:
    """
    Function decorator. Decorated functions are wrapped by
    a timer named by the function's module and qualified name.
    (unless explicitly named)
    Any arguments that could be passed to a klokke.Timer constructor
    can be passed as keyword arguments to the decorator instead
    """

    def _timed(fn: F) -> F:
        _name = name or f"{fn.__module__}.{fn.__qualname__}"

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with Timer(_name, **timer_kwargs):
                return fn(*args, **kwargs)

        return cast(F, wrapper)

    if __fn is not None:
        return _timed(__fn)

    return _timed
