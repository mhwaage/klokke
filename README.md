# klokke
klokke is a small library for high level measurement of code execution time. klokke keeps track of running timers, and nests them according to execution order. This allows you to keep track of which sub-sections of code contributes the most to your overall time spent.

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
