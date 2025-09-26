from .scene3d import Scene3D, Camera
from .objects.graph3d import ParametricSurface
from .objects.curve3d import ParametricCurve
from .objects.axes3d import Axes3D
from .objects.latex import LaTeXPlane
from .animation import TimeAnimator, FadeIn, Rotate, CameraPath
from .exporter import save_video
from .physics import projectile_motion, pendulum_simulation

__all__ = [
    "Scene3D","Camera",
    "ParametricSurface","ParametricCurve","Axes3D","LaTeXPlane",
    "TimeAnimator","FadeIn","Rotate","CameraPath",
    "save_video",
    "projectile_motion","pendulum_simulation"
]
