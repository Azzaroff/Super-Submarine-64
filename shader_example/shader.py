
self.vshader = avango.osg.nodes.Shader(Type = avango.osg.shadertype.VERTEX, FileName = "phong_texture_no_material.vert")
self.fshader = avango.osg.nodes.Shader(Type = avango.osg.shadertype.FRAGMENT, FileName = "phong_texture_no_material.frag")

self.prog = avango.osg.nodes.Program(ShaderList = [self.vshader, self.fshader])

self.uniform1 = avango.osg.nodes.Uniform(Values = [0], Type = avango.osg.uniformtype.INT, UniformName = "color_map")
self.uniform2 = avango.osg.nodes.Uniform(Values = [1], Type = avango.osg.uniformtype.INT, UniformName = "NumLights")
		
self.state = avango.osg.nodes.StateSet(RescaleNormalMode = 1, NormalizeMode = 1, Program = self.prog, Uniforms = [self.uniform1, self.uniform2])
