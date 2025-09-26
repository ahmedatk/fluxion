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
void main(){ f_color = vec4(v_color,1.0); }
"""

class Axes3D:
    def __init__(self, size=5.0, divisions=10):
        self.size = size
        self.div = divisions
        self.ctx = None
        self.prog = None
        self.vbo = None
        self.vao = None

    def _on_added(self, ctx):
        self.ctx = ctx
        self.prog = ctx.program(vertex_shader=VERT, fragment_shader=FRAG)
        lines = []
        colors = []
        s = self.size
        for i in range(-self.div, self.div+1):
            x = i * s / self.div
            lines += [x, -s, 0.0, x, s, 0.0]
            colors += [0.5,0.5,0.5]*2
            y = i * s / self.div
            lines += [-s, y, 0.0, s, y, 0.0]
            colors += [0.5,0.5,0.5]*2
        inter = []
        count = len(lines)//3
        for i in range(count):
            inter += lines[i*3:i*3+3] + colors[i*3:i*3+3]
        inter = np.array(inter, dtype='f4')
        self.vbo = ctx.buffer(inter.tobytes())
        self.vao = ctx.vertex_array(self.prog, [(self.vbo, '3f 3f', 'in_pos', 'in_color')])

    def model_matrix(self):
        return Matrix44.identity()

    def render(self, mvp, light_pos, cam_pos):
        self.prog['Mvp'].write(mvp.astype('f4').tobytes())
        self.vao.render(mode=moderngl.LINES)
