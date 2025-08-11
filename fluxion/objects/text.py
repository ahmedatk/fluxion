from PIL import ImageDraw, ImageFont
from .shape import Shape

class Text(Shape):
    def __init__(self, x=0, y=0, text="Hello", size=24, color=(0,0,0)):
        super().__init__(x, y, color)
        self.text = text
        self.size = size
        try:
            self.font = ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            from PIL import ImageFont
            self.font = ImageFont.load_default()

    def draw(self, image_draw: ImageDraw.ImageDraw):
        image_draw.text((self.x, self.y), self.text, fill=self.color, font=self.font)
