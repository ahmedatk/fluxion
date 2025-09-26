import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fluxion import Scene3D, ParametricCurve, LaTeXPlane, TimeAnimator, save_video, projectile_motion

# --- Projectile motion setup ---
v0 = 25
angle = 55
pos_fn = projectile_motion(v0=v0, angle_deg=angle)

def traj_t(t):
    x, z = pos_fn(t)
    return (x, 0.0, z)  # y=0 for 2D visualization

# --- Scene setup ---
scene = Scene3D(width=1280, height=720, background=(20, 20, 40))  # dark background

# Full trajectory curve
trajectory = ParametricCurve(
    lambda tt: traj_t(tt),
    t_range=(0, 5),
    samples=300,
    color=(0.8, 0.8, 0.2)
)

# Projectile marker (single point)
projectile = ParametricCurve(
    lambda tt: traj_t(0),
    t_range=(0, 0.001),
    samples=2,
    color=(1.0, 0.3, 0.3)
)

# Title
title = LaTeXPlane(latex_str=r"Projectile\ Motion\ (2D)", fontsize=40)
title.model = title.model * title.model.from_translation((12, -1.5, 0))

# Add objects to scene
scene.add(trajectory)
scene.add(projectile)
scene.add(title)

# --- Precompute max height and range for camera ---
x_max = max(pos_fn(t)[0] for t in np.linspace(0, 5, 100))
z_max = max(pos_fn(t)[1] for t in np.linspace(0, 5, 100))

# --- Animation setup ---
anim = TimeAnimator(scene, duration=5.0, fps=30)

# Store previous positions for fading trail
trail_positions = []

def update(t):
    # Update projectile position
    x, y, z = traj_t(t)
    projectile.func = lambda tt: (x, y, z)

    # Add fading trail for last 30 frames
    trail_positions.append((x, y, z))
    for i, pos in enumerate(trail_positions[-30:]):
        trail_color = (1.0, 0.5, 0.3 * (i/30))
        temp = ParametricCurve(
            lambda tt, p=pos: p,
            t_range=(0, 0.001),
            samples=2,
            color=trail_color
        )
        scene.add(temp)

    # Title fade in/out
    if t < 1.0:
        title.opacity = t / 1.0
    elif t > 4.0:
        title.opacity = max(0.0, (5.0 - t) / 1.0)
    else:
        title.opacity = 1.0

    # Fixed 2D side-view camera (x vs z)
    camera_pos = (x_max/2, -15, z_max/2 + 1)
    camera_target = (x_max/2, 0, z_max/2)
    scene.set_camera_pos(camera_pos, camera_target)

# --- Run animation ---
frames = anim.run(update)

# --- Save video ---
save_video(frames, "projectile_2D_demo.mp4", fps=30)
print("Saved projectile_2D_demo.mp4")
