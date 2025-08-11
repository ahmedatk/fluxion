import os
import tempfile
from moviepy.editor import ImageSequenceClip

def export_frames_to_video(frames, fps, out_path):
    # frames: list of PIL Images
    tmpdir = tempfile.mkdtemp(prefix="fluxion_frames_")
    paths = []
    try:
        for i, im in enumerate(frames):
            p = os.path.join(tmpdir, f"frame_{i:05d}.png")
            im.save(p)
            paths.append(p)
        clip = ImageSequenceClip(paths, fps=fps)
        # choose codec depending on extension
        ext = out_path.split(".")[-1].lower()
        if ext in ("mp4", "m4v"):
            clip.write_videofile(out_path, codec="libx264", audio=False, verbose=False, logger=None)
        elif ext in ("gif",):
            clip.write_gif(out_path, fps=fps, verbose=False, logger=None)
        else:
            # default to mp4
            clip.write_videofile(out_path, codec="libx264", audio=False, verbose=False, logger=None)
    finally:
        # cleanup frames
        try:
            for p in paths:
                os.remove(p)
            os.rmdir(tmpdir)
        except Exception:
            pass

# convenience wrapper
def render_to_file(scene, out_path):
    frames = scene.play(export_path=None)  # get frames
    export_frames_to_video(frames, scene.fps, out_path)
