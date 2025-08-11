from PIL import ImageDraw
from .shape import Shape

class Circle(Shape):
    def __init__(self, x=0, y=0, r=50, color=(0,0,0)):
        super().__init__(x, y, color)
        self.r = r

    def draw(self, image_draw: ImageDraw.ImageDraw):
        x0 = self.x - self.r
        y0 = self.y - self.r
        x1 = self.x + self.r
        y1 = self.y + self.r
        image_draw.ellipse([x0, y0, x1, y1], fill=self.color)
