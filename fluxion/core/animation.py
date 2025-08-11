from typing import Callable
from ..utils.easing import linear

class Animation:
    def __init__(self, target, prop: str, start, end, start_time: float, duration: float, easing: Callable = None):
        self.target = target
        self.prop = prop
        self.start = start
        self.end = end
        self.start_time = start_time
        self.duration = duration
        self.easing = easing or linear

    def progress(self, t: float):
        if t < self.start_time:
            return 0.0
        if t >= self.start_time + self.duration:
            return 1.0
        local_t = (t - self.start_time) / self.duration
        return self.easing(local_t)

    def apply(self, t: float):
        p = self.progress(t)
        val = self.start + (self.end - self.start) * p
        setattr(self.target, self.prop, val)
