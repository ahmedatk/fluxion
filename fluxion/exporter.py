import os
import imageio.v2 as imageio

def save_video(frames, path, fps=30):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    imageio.mimsave(path, frames, fps=fps)
