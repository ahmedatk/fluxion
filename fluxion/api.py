from PIL import Image, ImageDraw
from .render.exporter import render_to_file

class Scene:
    def __init__(self):
        self.frames = []

    def add_frame(self, draw_function):
        img = Image.new("RGB", (800, 600), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw_function(draw)
        self.frames.append(img)

    def render(self, output_path="output.mp4", fps=30):
        render_to_file(self.frames, output_path, fps)
