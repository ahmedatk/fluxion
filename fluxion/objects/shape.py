from typing import Tuple

class Shape:
    def __init__(self, x=0, y=0, color=(0,0,0), opacity=255):
        self.x = x
        self.y = y
        self.color = color
        self.opacity = opacity

    def draw(self, image_draw):
        raise NotImplementedError("draw must be implemented by subclasses")

    # convenience animate helper
    def animate(self, scene, prop, start, end, start_time, duration, easing=None):
        from ..core.animation import Animation
        anim = Animation(self, prop, start, end, start_time, duration, easing)
        scene.timeline.add(anim)
        return anim
