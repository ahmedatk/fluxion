from PIL import Image, ImageDraw
from typing import List
from ..objects.shape import Shape

class Renderer:
    def __init__(self, width=800, height=600, bg=(255,255,255)):
        self.width = width
        self.height = height
        self.bg = bg

    def render(self, objects: List[Shape]):
        img = Image.new("RGB", (self.width, self.height), self.bg)
        draw = ImageDraw.Draw(img)
        for obj in objects:
            obj.draw(draw)
        return img
