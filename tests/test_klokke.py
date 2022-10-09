from unittest import mock

from klokke import Elapsed, Timer


def test_elapsed_addition() -> None:
    e1 = Elapsed(1, 3.0)
    e2 = Elapsed(2, 5.0)

    expected = Elapsed(3, 8.0)
    assert e1 + e2 == expected


def test_elapsed_addition_nested_elapsed() -> None:
    e1 = Elapsed(1, 3.0)
    e2 = Elapsed(2, 5.0)
    e1.sub_timers["test"] = Elapsed(1, 1.0)
    e2.sub_timers["test"] = Elapsed(3, 4.0)

    expected = Elapsed(3, 8.0)
    expected.sub_timers["test"] = Elapsed(4, 5.0)
    assert e1 + e2 == expected


def test_timer_context() -> None:
    outer_start = 1
    inner_start = 2
    inner_end = 3
    outer_end = 4
    with mock.patch("time.time", autospec=True) as t:
        t.side_effect = [
            outer_start,
            inner_start,
            inner_end,
            outer_end,
        ]
        with Timer("outer") as outer:
            with Timer("inner") as inner:
                pass
    assert outer.elapsed.total_time == outer_end - outer_start
    assert "inner" in outer.elapsed.sub_timers
    assert inner.elapsed == outer.elapsed.sub_timers["inner"]
    assert inner.elapsed.total_time == inner_end - inner_start
    assert inner.elapsed.n_executed == 1

    assert (
        str(outer) == f"outer: {outer.elapsed.total_time} seconds\n"
        f"Of which:\n  inner: {inner.elapsed.total_time} seconds"
    )


def test_autoprint_executes_passed_function() -> None:
    rv = ""

    def printer(s: str) -> None:
        nonlocal rv
        rv = s

    with Timer("whatever", autoprint=printer):
        pass

    assert rv != ""
    assert "whatever:" in rv
