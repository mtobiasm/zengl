import zengl


class Point:
    def __init__(self, framebuffer, uniform_buffer):
        self.ctx = zengl.context()
        self.pipeline = self.ctx.pipeline(
            vertex_shader='''
                #version 300 es
                precision highp float;

                layout (std140) uniform Common {
                    mat4 mvp;
                    vec3 eye;
                    vec3 light;
                };

                vec3 vertices[12] = vec3[](
                    vec3(0.000000, 0.000000, -1.000000),
                    vec3(0.723600, -0.525720, -0.447215),
                    vec3(-0.276385, -0.850640, -0.447215),
                    vec3(-0.894425, 0.000000, -0.447215),
                    vec3(-0.276385, 0.850640, -0.447215),
                    vec3(0.723600, 0.525720, -0.447215),
                    vec3(0.276385, -0.850640, 0.447215),
                    vec3(-0.723600, -0.525720, 0.447215),
                    vec3(-0.723600, 0.525720, 0.447215),
                    vec3(0.276385, 0.850640, 0.447215),
                    vec3(0.894425, 0.000000, 0.447215),
                    vec3(0.000000, 0.000000, 1.000000)
                );

                vec2 texcoords[22] = vec2[](
                    vec2(0.181819, 0.000000),
                    vec2(0.363637, 0.000000),
                    vec2(0.909091, 0.000000),
                    vec2(0.727273, 0.000000),
                    vec2(0.545455, 0.000000),
                    vec2(0.272728, 0.157461),
                    vec2(1.000000, 0.157461),
                    vec2(0.090910, 0.157461),
                    vec2(0.818182, 0.157461),
                    vec2(0.636364, 0.157461),
                    vec2(0.454546, 0.157461),
                    vec2(0.181819, 0.314921),
                    vec2(0.000000, 0.314921),
                    vec2(0.909091, 0.314921),
                    vec2(0.727273, 0.314921),
                    vec2(0.545455, 0.314921),
                    vec2(0.363637, 0.314921),
                    vec2(0.272728, 0.472382),
                    vec2(0.090910, 0.472382),
                    vec2(0.818182, 0.472382),
                    vec2(0.636364, 0.472382),
                    vec2(0.454546, 0.472382)
                );

                int vertex_indices[60] = int[](
                    0, 1, 2, 1, 0, 5, 0, 2, 3, 0, 3, 4, 0, 4, 5, 1, 5, 10, 2, 1, 6, 3, 2, 7, 4, 3, 8, 5, 4, 9, 1, 10,
                    6, 2, 6, 7, 3, 7, 8, 4, 8, 9, 5, 9, 10, 6, 10, 11, 7, 6, 11, 8, 7, 11, 9, 8, 11, 10, 9, 11
                );

                int texcoord_indices[60] = int[](
                    0, 5, 7, 5, 1, 10, 2, 6, 8, 3, 8, 9, 4, 9, 10, 5, 10, 16, 7, 5, 11, 8, 6, 13, 9, 8, 14, 10, 9, 15,
                    5, 16, 11, 7, 11, 12, 8, 13, 14, 9, 14, 15, 10, 15, 16, 11, 16, 17, 12, 11, 18, 14, 13, 19, 15, 14,
                    20, 16, 15, 21
                );

                out vec3 v_vertex;
                out vec3 v_normal;
                out vec2 v_texcoord;

                void main() {
                    v_vertex = vertices[vertex_indices[gl_VertexID]];
                    v_normal = vertices[vertex_indices[gl_VertexID]];
                    v_texcoord = texcoords[texcoord_indices[gl_VertexID]];
                    gl_Position = mvp * vec4(v_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 300 es
                precision highp float;

                layout (std140) uniform Common {
                    mat4 mvp;
                    vec3 eye;
                    vec3 light;
                };

                in vec3 v_normal;

                layout (location = 0) out vec4 out_color;

                void main() {
                    float lum = dot(normalize(light.xyz), normalize(v_normal)) * 0.7 + 0.3;
                    out_color = vec4(lum, lum, lum, 1.0);
                }
            ''',
            layout=[
                {
                    'name': 'Common',
                    'binding': 0,
                },
            ],
            resources=[
                {
                    'type': 'uniform_buffer',
                    'binding': 0,
                    'buffer': uniform_buffer,
                },
            ],
            framebuffer=framebuffer,
            topology='triangles',
            cull_face='back',
            vertex_count=60,
        )

    def render(self):
        self.pipeline.render()


if __name__ == '__main__':
    import preview
    from grid import Grid

    preview.show([Grid, Point])
