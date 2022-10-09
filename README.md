# klokke
klokke is a small library for high level measurement of code execution time. klokke keeps track of running timers, and nests them according to execution order. This allows you to keep track of which sub-sections of code contributes the most to your overall time spent.
In addition, a decorator `@timed` is provided for timing function execution.

## Examples
Timing a snippet of code:
```python
>>> from time import sleep
>>> from klokke import Timer
>>> with Timer("Something expensive") as timer:
...     sleep(5)
... 
>>> print(timer)
Something expensive: 5.004069805145264 seconds
```

Nesting timers:
```python
>>> from time import sleep
>>> from klokke import Timer
>>> with Timer("outer") as outer:
...     with Timer("inner") as inner:
...         sleep(1)
...     sleep(2)
... 
>>> print(outer)
outer: 3.0084269046783447 seconds
Of which:
  inner: 1.0031757354736328 seconds
```

Using a decorator:
```python
>>> from time import sleep
>>> from klokke import Timer, timed
>>> @timed
... def foo():
...     sleep(2)
...     return 5
... 
>>> with Timer("bar") as t:
...     x = foo() + foo()
... 
>>> print(t)
bar: 4.010395050048828 seconds
Of which:
  __main__.foo: 4.010124683380127 seconds
```

Setting up timers to automatically print on completion:
```python
>>> from time import sleep
>>> from klokke import Timer
>>> with Timer("Something expensive", autoprint=print) as timer:
...     sleep(5)
... 
Something expensive: 5.000231981277466 seconds
```

All keyword arguments to `Timer` can also be passed through the `@timed` decorator:
```python
>>> from time import sleep
>>> from klokke import timed
>>> import logging
>>> logger = logging.getLogger("foo")
>>> @timed(name="foo_log", autoprint=logger.warning)
... def foo():
...     sleep(1)
... 
>>> foo()
foo_log: 1.0042669773101807 seconds
```
