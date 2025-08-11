from typing import List
from ..render.renderer import Renderer
from ..core.timeline import Timeline
from ..objects.shape import Shape

class Scene:
    def __init__(self, width=800, height=600, bg=(255,255,255), fps=30, duration=5):
        self.width = width
        self.height = height
        self.bg = bg
        self.fps = fps
        self.duration = duration
        self.objects: List[Shape] = []
        self.timeline = Timeline()
        self.renderer = Renderer(width, height, bg)

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def play(self, export_path=None):
        total_frames = int(self.fps * self.duration)
        frames = []
        for frame_i in range(total_frames):
            t = frame_i / self.fps
            # advance timeline (this mutates objects)
            self.timeline.step(t)
            # render current frame
            img = self.renderer.render(self.objects)
            frames.append(img)
        # Export if requested
        if export_path:
            from ..render.exporter import export_frames_to_video
            export_frames_to_video(frames, self.fps, export_path)
        return frames
