import numpy as np
from pyrr import Matrix44
import moderngl

VERT = """
#version 330
uniform mat4 Mvp;
in vec3 in_pos;
in vec3 in_color;
out vec3 v_color;
void main() {
    gl_Position = Mvp * vec4(in_pos,1.0);
    v_color = in_color;
}
"""
FRAG = """
#version 330
in vec3 v_color;
out vec4 f_color;
void main() {
    f_color = vec4(v_color, 1.0);
}
"""

class ParametricCurve:
    def __init__(self, func_xyz, t_range=(0,1), samples=400, color=(1.0,1.0,1.0)):
        self.func = func_xyz
        self.tmin, self.tmax = t_range
        self.samples = samples
        self.color = color
        self.ctx = None
        self.program = None
        self.vbo = None
        self.vao = None

    def _on_added(self, ctx):
        self.ctx = ctx
        self.program = ctx.program(vertex_shader=VERT, fragment_shader=FRAG)
        pts = []
        cols = []
        for i in range(self.samples):
            t = self.tmin + (self.tmax - self.tmin) * i/(self.samples-1)
            x,y,z = self.func(t)
            pts.extend([x,y,z])
            cols.extend(list(self.color))
        inter = []
        for i in range(self.samples):
            inter += pts[i*3:i*3+3] + cols[i*3:i*3+3]
        inter = np.array(inter, dtype='f4')
        self.vbo = ctx.buffer(inter.tobytes())
        self.vao = ctx.vertex_array(self.program, [(self.vbo, '3f 3f', 'in_pos', 'in_color')])

    def model_matrix(self):
        return Matrix44.identity()

    def render(self, mvp, light_pos, cam_pos):
        self.program['Mvp'].write(mvp.astype('f4').tobytes())
        # GL_LINE_STRIP mode
        self.vao.render(mode=moderngl.LINE_STRIP)
