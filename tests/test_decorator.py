import inspect
from unittest import mock

from klokke import Timer, timed


@timed
def inner(x: int, y: float) -> float:
    return 15 * x - y


def test_timed_preserves_annotations() -> None:

    sig = inspect.signature(inner)
    assert sig.return_annotation == float
    assert len(sig.parameters) == 2
    assert sig.parameters["x"].annotation == int
    assert sig.parameters["y"].annotation == float


def test_timed_times_single_call_correctly() -> None:
    outer_enter = 0
    inner_enter = 1
    inner_exit = 2
    outer_exit = 3
    with mock.patch("time.time", autospec=True) as t:
        t.side_effect = [
            outer_enter,
            inner_enter,
            inner_exit,
            outer_exit,
        ]
        with Timer("outer") as outer:
            rv = inner(1, 2)

    assert rv == 13.0
    assert outer.elapsed.total_time == outer_exit - outer_enter
    expected_name = f"{inner.__module__}.{inner.__qualname__}"
    assert expected_name in outer.elapsed.sub_timers
    inner_timing = outer.elapsed.sub_timers[expected_name]
    assert inner_timing.total_time == inner_exit - inner_enter
    assert inner_timing.n_executed == 1


def test_timed_times_multiple_calls_correctly() -> None:
    outer_enter = 0
    first_inner_enter = 1
    first_inner_exit = 2
    second_inner_enter = 3
    second_inner_exit = 4
    outer_exit = 5
    with mock.patch("time.time", autospec=True) as t:
        t.side_effect = [
            outer_enter,
            first_inner_enter,
            first_inner_exit,
            second_inner_enter,
            second_inner_exit,
            outer_exit,
        ]
        with Timer("outer") as outer:
            rv = inner(1, 2) + inner(4, 5)

    assert rv == 68.0
    assert outer.elapsed.total_time == outer_exit - outer_enter
    expected_name = f"{inner.__module__}.{inner.__qualname__}"
    assert expected_name in outer.elapsed.sub_timers
    inner_timing = outer.elapsed.sub_timers[expected_name]
    assert inner_timing.total_time == (first_inner_exit - first_inner_enter) + (
        second_inner_exit - second_inner_enter
    )
    assert inner_timing.n_executed == 2
