import os
import imageio
import numpy as np
from PIL import Image

def render_to_file(frames, output_path="output.mp4", fps=30):
    """
    Render a list of PIL Image frames to a video file without requiring system FFmpeg.
    
    Args:
        frames (list): List of PIL.Image objects or NumPy arrays.
        output_path (str): Output video file path.
        fps (int): Frames per second.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Convert all frames to RGB numpy arrays
    processed_frames = []
    for frame in frames:
        if isinstance(frame, Image.Image):
            frame = frame.convert("RGB")
            processed_frames.append(np.array(frame))  # ✅ Convert PIL → NumPy
        else:
            processed_frames.append(frame)  # Already NumPy

    # Write video using imageio-ffmpeg
    with imageio.get_writer(output_path, fps=fps) as writer:
        for frame in processed_frames:
            writer.append_data(frame)

    print(f"✅ Video saved to {output_path}")
