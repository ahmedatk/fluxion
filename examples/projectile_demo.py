import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fluxion import Scene3D, ParametricCurve, LaTeXPlane, TimeAnimator, save_video, projectile_motion

# --- Projectile motion setup ---
pos_fn = projectile_motion(v0=25, angle_deg=55)

def traj_t(t):
    x, z = pos_fn(t)
    return (x, 0.0, z)

# --- Scene setup ---
scene = Scene3D(width=1280, height=720, background=(5, 5, 12))  # dark blue background

# Trajectory curve
curve = ParametricCurve(
    lambda tt: traj_t(tt),
    t_range=(0, 5),
    samples=300,
    color=(1.0, 0.6, 0.2)
)

# Projectile marker (tiny curve acting as a moving point)
projectile = ParametricCurve(
    lambda tt: traj_t(0),  # initial position
    t_range=(0, 0.001),    # minimal range
    samples=2,             # must be >=2 to avoid ZeroDivisionError
    color=(0.9, 0.2, 0.2)
)

# Title
title = LaTeXPlane(latex_str=r"Projectile\ Motion", fontsize=40)

# Add objects to scene
scene.add(curve)
scene.add(projectile)
scene.add(title)

# Position title slightly lower
title.model = title.model * title.model.from_translation((0.0, -3.2, 0.0))

# --- Animation setup ---
anim = TimeAnimator(scene, duration=5.0, fps=30)

def update(t):
    # Move projectile to current position
    projectile.func = lambda tt: traj_t(t)

    # Camera orbit with slight zoom
    radius = 7.0 + 0.5 * np.sin(0.5 * t)
    ang = 0.3 * t
    scene.set_camera_pos(
        (radius * np.cos(ang), radius * np.sin(ang), 3.0 + 0.3 * np.sin(0.7 * t)),
        target=(2.5, 0, 1.0)
    )

    # Title fade in/out
    if t < 1.0:
        title.opacity = t / 1.0
    elif t > 4.0:
        title.opacity = max(0.0, (5.0 - t) / 1.0)
    else:
        title.opacity = 1.0

    # Optional: change trajectory color based on height
    x, y, z = traj_t(t)
    h = (z + 5) / 10.0
    curve.color = (1.0, 0.3 + h * 0.7, 0.2 + h * 0.5)

# --- Run animation and export ---
frames = anim.run(update)
save_video(frames, "projectile_demo.mp4", fps=30)
print("Saved projectile_demo.mp4")
