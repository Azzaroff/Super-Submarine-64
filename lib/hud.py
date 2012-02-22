import avango
import avango.osg
import time

from avango.script import field_has_changed

# import modules from local library
from lib.globals import *

class HUD(avango.script.Script):
    
    absolute_transform = avango.osg.nodes.MatrixTransform()
     # constructor
    def __init__(self):
        self.super(HUD).__init__()
        
    
    def my_constructor(self, SCENE, CAMERA, PLAYERID):
        
        self.camera = CAMERA
        self.id = PLAYERID
        self.Scene = SCENE
        self.absolute_transform.Matrix.value = self.camera.get_absolute_transform(self.camera)
        
        # mode visualization nodes
        #self.panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.0,0.0,0.0,1.0), Width = 0.04, Height = 0.02, BorderWidth = 0.000)
        #self.panel.Position.value = avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.04 + 0.02)), gl_physical_screen_height * 0.45, 0.0)
        #self.panel.EdgeSmooth.value = 1
        
        text = self.create_text(avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.04 + 0.02)), gl_physical_screen_height * 0.45, 0.0), "1/2");
        self.geode = avango.osg.nodes.LayerGeode(Drawables = [self.text], StateSet = avango.osg.nodes.StateSet(LightingMode = 0))
        
        self.Scene.root.Children.value.append(self.absolute_transform)
        self.absolute_transform.Children.value.append(self.geode) # append gui to navigation node --> head up display
        
    def create_text(self, position, content):
        self.text = avango.osg.nodes.Text(Size = 0.01, Alignment = 4, Fontname = "VeraBI.ttf", Color = avango.osg.Vec4(1.0,1.0,1.0,1.0))
        self.text.String.value = content
        self.text.Position.value = position

