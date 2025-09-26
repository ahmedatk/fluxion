class TimeAnimator:
    def __init__(self, scene, duration=5.0, fps=30):
        self.scene = scene
        self.duration = duration
        self.fps = fps

    def run(self, update_fn):
        total_frames = max(1, int(self.duration * self.fps))
        frames = []
        for i in range(total_frames):
            t = i / self.fps
            update_fn(t)
            frame = self.scene.render_frame()
            frames.append(frame)
            if (i+1) % 60 == 0:
                print(f"Rendered {i+1}/{total_frames} frames")
        return frames

# Simple convenience animations (stateless helpers used inside update)
class FadeIn:
    def __init__(self, obj, duration=1.0):
        self.obj = obj
        self.duration = duration

    def apply(self, t, total_duration):
        pct = t / total_duration
        if pct < (self.duration / total_duration):
            self.obj.opacity = pct * (total_duration / self.duration)
        else:
            self.obj.opacity = 1.0

class Rotate:
    def __init__(self, obj, axis=(0,0,1), speed_deg=90.0):
        self.obj = obj
        self.axis = axis
        self.speed = speed_deg

    def apply(self, t):
        # simplistic: rotate around z
        self.obj.rotation = (0.0, 0.0, t * self.speed)

class CameraPath:
    def __init__(self, path_points, duration=2):
        self.path_points = path_points
        self.duration = duration

    def apply(self, camera):
        # Simple linear interpolation between path points
        import numpy as np
        num_points = len(self.path_points)
        for t in np.linspace(0, 1, num_points):
            idx = int(t * (num_points - 1))
            camera.position = self.path_points[idx]
            camera.update()

