import numpy as np
from PIL import Image
from pyrr import Matrix44
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import moderngl


VERT_TEX = """
#version 330
uniform mat4 Mvp;
in vec3 in_vert;
in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = Mvp * vec4(in_vert, 1.0);
    v_uv = in_uv;
}
"""

FRAG_TEX = """
#version 330
in vec2 v_uv;
out vec4 f_color;
uniform sampler2D tex;
uniform float opacity;
void main() {
    vec4 c = texture(tex, v_uv);
    f_color = vec4(c.rgb, c.a * opacity);
}
"""

class LaTeXPlane:
    def __init__(self, latex_str=r"$\psi(x,t)=A\sin(kx-\omega t)$", fontsize=40):
        self.latex_str = latex_str
        self.fontsize = fontsize
        self.ctx = None
        self.texture = None
        self.prog = None
        self.vbo = None
        self.ibo = None
        self.vao = None
        self.opacity = 1.0
        self.model = Matrix44.identity()

    def _render_latex_to_image(self):
        fig = plt.figure(figsize=(6,2), dpi=200)
        fig.patch.set_alpha(0.0)
        plt.text(0.5, 0.5, self.latex_str, horizontalalignment='center', verticalalignment='center',
                 fontsize=self.fontsize, color='white')
        plt.axis('off')
        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        data = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        data = data.reshape((h, w, 4))
        data = data[:, :, [1,2,3,0]]
        plt.close(fig)
        img = Image.fromarray(data, mode='RGBA')
        return img

    def _get_program(self, ctx):
        return ctx.program(vertex_shader=VERT_TEX, fragment_shader=FRAG_TEX)

    def _on_added(self, ctx):
        self.ctx = ctx
        img = self._render_latex_to_image()
        rgba = img.tobytes()
        self.texture = ctx.texture(img.size, 4, rgba)
        self.texture.build_mipmaps()
        self.texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        w = 4.0
        h = 1.0 * (img.size[1] / img.size[0]) * w
        verts = np.array([
            -w/2,  h/2, 0.0,  0.0, 1.0,
             w/2,  h/2, 0.0,  1.0, 1.0,
             w/2, -h/2, 0.0,  1.0, 0.0,
            -w/2, -h/2,0.0,   0.0, 0.0,
        ], dtype='f4')
        inds = np.array([0,1,2, 0,2,3], dtype='i4')
        self.prog = self._get_program(ctx)
        self.vbo = ctx.buffer(verts.tobytes())
        self.ibo = ctx.buffer(inds.tobytes())
        self.vao = ctx.vertex_array(self.prog, [(self.vbo, '3f 2f', 'in_vert', 'in_uv')], self.ibo)

    def model_matrix(self):
        return self.model

    def render(self, mvp, light_pos, cam_pos):
        self.prog['Mvp'].write(mvp.astype('f4').tobytes())
        self.texture.use(location=0)
        self.prog['tex'].value = 0
        try:
            self.prog['opacity'].value = float(self.opacity)
        except Exception:
            pass
        self.vao.render()
