import moderngl
import numpy as np
from PIL import Image
from pyrr import Matrix44

class Fluxion3DScene:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.ctx = moderngl.create_standalone_context()
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                uniform mat4 Mvp;
                in vec3 in_vert;
                in vec3 in_color;
                out vec3 v_color;
                void main() {
                    gl_Position = Mvp * vec4(in_vert, 1.0);
                    v_color = in_color;
                }
            ''',
            fragment_shader='''
                #version 330
                in vec3 v_color;
                out vec4 f_color;
                void main() {
                    f_color = vec4(v_color, 1.0);
                }
            ''',
        )
        # Cube vertices
        vertices = np.array([
            # pos         # color
            -1, -1,  1,  1, 0, 0,
             1, -1,  1,  0, 1, 0,
             1,  1,  1,  0, 0, 1,
            -1,  1,  1,  1, 1, 0,
            -1, -1, -1,  0, 1, 1,
             1, -1, -1,  1, 0, 1,
             1,  1, -1,  0.5, 0.5, 0.5,
            -1,  1, -1,  1, 1, 1,
        ], dtype='f4')

        indices = np.array([
            0, 1, 2, 2, 3, 0,
            1, 5, 6, 6, 2, 1,
            5, 4, 7, 7, 6, 5,
            4, 0, 3, 3, 7, 4,
            3, 2, 6, 6, 7, 3,
            4, 5, 1, 1, 0, 4,
        ], dtype='i4')

        vbo = self.ctx.buffer(vertices.tobytes())
        ibo = self.ctx.buffer(indices.tobytes())

        vao_content = [
            (vbo, '3f 3f', 'in_vert', 'in_color')
        ]
        self.vao = self.ctx.vertex_array(self.prog, vao_content, ibo)

    def render_frame(self, angle):
        # Create transformation
        proj = Matrix44.perspective_projection(45.0, self.width / self.height, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (3, 3, 3),
            (0, 0, 0),
            (0, 0, 1),
        )
        rotate = Matrix44.from_y_rotation(np.radians(angle))
        mvp = proj * lookat * rotate

        self.prog['Mvp'].write(mvp.astype('f4').tobytes())

        fbo = self.ctx.simple_framebuffer((self.width, self.height))
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render()

        data = fbo.read(components=3)
        img = Image.frombytes('RGB', (self.width, self.height), data)
        return img

# Example usage
if __name__ == "__main__":
    scene = Fluxion3DScene()
    frames = []
    for angle in range(0, 360, 2):
        frames.append(scene.render_frame(angle))
    frames[0].save("cube_rotation.gif", save_all=True, append_images=frames[1:], duration=40, loop=0)
