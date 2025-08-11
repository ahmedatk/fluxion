from fluxion.core.scene import Scene
from fluxion.objects.circle import Circle
from fluxion.utils.easing import ease_out_quad

def build_scene():
    scene = Scene(width=640, height=360, bg=(255,255,255), fps=30, duration=3)
    # add a circle centered left
    c = Circle(x=80, y=180, r=40, color=(255,0,0))
    scene.add(c)
    # animate circle x from 80 to 560 between t=0.2 and 2.2 seconds
    scene.timeline.add(
        # animate property 'x' on circle: start=80, end=560, start_time=0.2, duration=2.0
        # reuse core.animation.Animation signature
        __import__("fluxion").core.animation.Animation(c, "x", 80, 560, 0.2, 2.0, easing=ease_out_quad)
    )
    return scene

if __name__ == "__main__":
    s = build_scene()
    # quick local export
    from fluxion.render.exporter import render_to_file
    render_to_file(s, "circle_demo.mp4")
    print("Rendered circle_demo.mp4")
