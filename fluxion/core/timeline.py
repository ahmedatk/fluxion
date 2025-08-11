from typing import List, Callable
from .animation import Animation

class Timeline:
    def __init__(self):
        self.animations: List[Animation] = []

    def add(self, animation: Animation):
        self.animations.append(animation)

    def step(self, t: float):
        # evaluate each animation at time t
        for anim in self.animations:
            anim.apply(t)
