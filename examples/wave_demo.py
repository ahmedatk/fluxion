import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fluxion.scene3d import Scene3D
from fluxion.objects.graph3d import ParametricSurface
from fluxion.objects.latex import LaTeXPlane
from fluxion.animation import TimeAnimator
from fluxion.exporter import save_video

k = 2.0
omega = 2.0
def wave(x, y, t):
    return 0.8 * np.sin(k * x - omega * t) * np.exp(-0.05 * (x**2 + y**2))

def color_fn(x, y, z, t):
    val = (z + 1.0) / 2.0
    return (0.1 + 0.9*val, 0.1 + 0.4*(1-val), 0.3 + 0.7*(1-val))

scene = Scene3D(width=1280, height=720, background=(8,8,16))
surface = ParametricSurface(wave, x_range=(-6,6), y_range=(-3,3), res=(200,140), color_fn=color_fn)
title = LaTeXPlane(latex_str=r"$\psi(x,t)=A\sin(kx-\omega t)$", fontsize=48)

scene.add(surface)
scene.add(title)
title.model = title.model * title.model.from_translation((0.0, -3.6, 0.0))

anim = TimeAnimator(scene, duration=8.0, fps=30)

def update(t):
    surface.update(t)
    ang = 0.3 * t
    radius = 8.0
    scene.set_camera_pos(
        (radius*np.cos(ang), radius*np.sin(ang), 3.5),
        target=(0,0,0)
    )
    if t < 1.0:
        title.opacity = t / 1.0
    elif t > 7.0:
        title.opacity = max(0.0, (8.0 - t) / 1.0)
    else:
        title.opacity = 1.0

frames = anim.run(update)
save_video(frames, "wave_demo.mp4", fps=30)
print("Saved wave_demo.mp4")
