from manim import *

class FluxionTest(ThreeDScene):
    def construct(self):
        # Title
        title = Text("Fluxion Test Animation", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Draw a square
        square = Square(side_length=2, color=YELLOW)
        self.play(Create(square))
        self.wait(1)

        # Transform square into circle
        circle = Circle(radius=1, color=GREEN)
        self.play(Transform(square, circle))
        self.wait(1)

        # Add a 3D cube with camera movement
        axes = ThreeDAxes()
        cube = Cube(side_length=2, fill_color=BLUE, fill_opacity=0.3)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Create(cube))
        self.wait(1)

        # Animate cube rotation
        self.begin_3dillusion_camera_rotation(rate=0.2)  # <-- not a valid manim method
        self.play(Rotate(cube, angle=PI, axis=RIGHT, run_time=3))
        self.wait(2)
        self.stop_3dillusion_camera_rotation()  # <-- also invalid in manim

        # Outro text
        outro = Text("Fluxion: Animation Complete", font_size=36, color=RED)
        self.play(Write(outro))
        self.wait(2)
