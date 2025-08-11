def test_smoke():
    from fluxion.core.scene import Scene
    from fluxion.objects.circle import Circle
    s = Scene(width=200, height=100, fps=10, duration=0.5)
    c = Circle(x=50, y=50, r=10)
    s.add(c)
    frames = s.play()
    assert len(frames) == int(10 * 0.5)
