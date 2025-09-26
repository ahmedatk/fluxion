import moderngl
from pyrr import Matrix44, Vector3
from .utils import read_fbo_to_ndarray

class Camera:
    def __init__(self, fov=45.0, aspect=16/9, near=0.1, far=100.0):
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.position = Vector3([6.0, 3.0, 6.0])
        self.target = Vector3([0.0, 0.0, 0.0])
        self.up = Vector3([0.0, 0.0, 1.0])
        self.proj = Matrix44.perspective_projection(self.fov, self.aspect, self.near, self.far)

    def view_matrix(self):
        return Matrix44.look_at(self.position, self.target, self.up)

class Scene3D:
    def __init__(self, width=1280, height=720, background=(8,8,16)):
        self.width = width
        self.height = height
        self.background = background
        self.ctx = moderngl.create_standalone_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        try:
            self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
        except Exception:
            pass
        self.camera = Camera(aspect=width/height)
        self.objects = []
        self.light_pos = (6.0, 6.0, 6.0)

    def add(self, obj):
        self.objects.append(obj)
        if hasattr(obj, "_on_added"):
            obj._on_added(self.ctx)

    def set_camera_pos(self, pos, target=None):
        self.camera.position = Vector3(pos)
        if target is not None:
            self.camera.target = Vector3(target)

    def render_frame(self):
        fbo = self.ctx.simple_framebuffer((self.width, self.height))
        fbo.use()
        r,g,b = [c/255.0 for c in self.background]
        fbo.clear(r, g, b, 1.0)
        proj = self.camera.proj
        view = self.camera.view_matrix()
        for obj in self.objects:
            model = obj.model_matrix() if hasattr(obj, "model_matrix") else Matrix44.identity()
            mvp = proj * view * model
            if hasattr(obj, "render"):
                obj.render(mvp, self.light_pos, tuple(self.camera.position))
        frame = read_fbo_to_ndarray(fbo, self.width, self.height)
        return frame
