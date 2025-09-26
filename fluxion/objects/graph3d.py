# ParametricSurface: builds a mesh from f(x,y,t) and updates vertex heights
import numpy as np
from pyrr import Matrix44

VERT_SRC = """
#version 330
uniform mat4 Mvp;
in vec3 in_pos;
in vec3 in_norm;
in vec3 in_color;
out vec3 v_norm;
out vec3 v_color;
out vec3 v_pos;
void main() {
    gl_Position = Mvp * vec4(in_pos, 1.0);
    v_pos = in_pos;
    v_norm = in_norm;
    v_color = in_color;
}
"""

FRAG_SRC = """
#version 330
in vec3 v_norm;
in vec3 v_color;
in vec3 v_pos;
out vec4 f_color;
uniform vec3 light_pos;
uniform vec3 cam_pos;
void main() {
    vec3 N = normalize(v_norm);
    vec3 L = normalize(light_pos - v_pos);
    float diff = max(dot(N,L), 0.0);
    vec3 color = v_color * (0.2 + 0.8*diff);
    f_color = vec4(color, 1.0);
}
"""

class ParametricSurface:
    def __init__(self, func, x_range=(-5,5), y_range=(-5,5), res=(120,120), color_fn=None):
        self.func = func
        self.xmin, self.xmax = x_range
        self.ymin, self.ymax = y_range
        self.res_x, self.res_y = res
        self.color_fn = color_fn or (lambda x,y,z,t: (0.2,0.6,1.0))
        self.ctx = None
        self.vbo = None
        self.ibo = None
        self.vao = None
        self.program = None
        self.model = Matrix44.identity()

    def _on_added(self, ctx):
        self.ctx = ctx
        self.program = ctx.program(vertex_shader=VERT_SRC, fragment_shader=FRAG_SRC)
        verts, inds = self._build_mesh(0.0)
        self.vbo = ctx.buffer(verts.astype('f4').tobytes())
        self.ibo = ctx.buffer(inds.astype('i4').tobytes())
        self.vao = ctx.vertex_array(self.program, [(self.vbo, '3f 3f 3f', 'in_pos', 'in_norm', 'in_color')], self.ibo)

    def _build_mesh(self, t):
        xs = np.linspace(self.xmin, self.xmax, self.res_x)
        ys = np.linspace(self.ymin, self.ymax, self.res_y)
        verts = []
        for ix, x in enumerate(xs):
            for iy, y in enumerate(ys):
                z = float(self.func(x, y, t))
                eps = 1e-3
                zx = self.func(x+eps, y, t) - z
                zy = self.func(x, y+eps, t) - z
                nx, ny, nz = -zx, -zy, 1.0
                nlen = max(1e-9, (nx*nx + ny*ny + nz*nz)**0.5)
                nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
                r,g,b = self.color_fn(x,y,z,t)
                verts.extend([x, y, z, nx, ny, nz, r, g, b])
        verts = np.array(verts, dtype='f4')
        inds = []
        for i in range(self.res_x - 1):
            for j in range(self.res_y - 1):
                a = i * self.res_y + j
                b = (i+1) * self.res_y + j
                inds += [a, b, a+1, b, b+1, a+1]
        inds = np.array(inds, dtype='i4')
        return verts, inds

    def update(self, t):
        verts, _ = self._build_mesh(t)
        self.vbo.orphan(size=verts.nbytes)
        self.vbo.write(verts.tobytes())

    def model_matrix(self):
        return self.model

    def render(self, mvp, light_pos, cam_pos):
        self.program['Mvp'].write(mvp.astype('f4').tobytes())
        self.program['light_pos'].value = tuple(light_pos)
        if 'cam_pos' in self.program:
            self.program['cam_pos'].value = tuple(cam_pos)

        self.vao.render()
