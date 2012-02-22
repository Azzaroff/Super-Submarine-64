import avango
import avango.osg
import time

from avango.script import field_has_changed

# import modules from local library
from lib.globals import *

class HUD(avango.script.Script):
    
    hud_transform = avango.osg.nodes.MatrixTransform()
    #absolute_transform = avango.osg.SFMatrix()
     # constructor
    def __init__(self):
        self.super(HUD).__init__()
        
    
    def my_constructor(self, SCENE, CAMERA_TANSFORM, PLAYERID):
        
        self.camera = CAMERA_TANSFORM
        self.id = PLAYERID
        self.Scene = SCENE
        #self.absolute_transform.connect_from(self.camera.AbsoluteMatrix)
        self.hud_transform.Matrix.connect_from(self.camera.AbsoluteMatrix)
        
        # mode visualization nodes
        #self.panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.0,0.0,0.0,1.0), Width = 0.04, Height = 0.02, BorderWidth = 0.000)
        #self.panel.Position.value = avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.04 + 0.02)), gl_physical_screen_height * 0.45, 0.0)
        #self.panel.EdgeSmooth.value = 1
        
        self.label0 = self.create_text(avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.06 + 0.015)), gl_physical_screen_height * 0.44, 0.0), "Runde:");
        self.text0 = self.create_text(avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.02)), gl_physical_screen_height * 0.44, 0.0), "1/2");
        self.label1 = self.create_text(avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.06 + 0.015)), gl_physical_screen_height * 0.41, 0.0), "Position:");
        self.text1 = self.create_text(avango.osg.Vec3(self.id*gl_physical_screen_width*0.5 + (-(0.02)), gl_physical_screen_height * 0.41, 0.0), "1/2");
        self.label2 = self.create_text(avango.osg.Vec3((self.id-1)*gl_physical_screen_width*0.5 + (0.005), gl_physical_screen_height * 0.44, 0.0), "Zeit:");
        self.text2 = self.create_text(avango.osg.Vec3((self.id-1)*gl_physical_screen_width*0.5 + ((0.085)), gl_physical_screen_height * 0.44, 0.0), "00:00:00");
        self.label3 = self.create_text(avango.osg.Vec3((self.id-1)*gl_physical_screen_width*0.5 + (0.005), gl_physical_screen_height * 0.41, 0.0), "Rundenzeit:");
        self.text3 = self.create_text(avango.osg.Vec3((self.id-1)*gl_physical_screen_width*0.5 + ((0.085)), gl_physical_screen_height * 0.41, 0.0), "00:00:00");
        self.geode = avango.osg.nodes.LayerGeode(Drawables = [self.label0, self.text0, self.label1, self.text1, self.label2, self.text2, self.label3, self.text3], StateSet = avango.osg.nodes.StateSet(LightingMode = 0), Name="HUD1")
        
        self.Scene.root.Children.value.append(self.hud_transform)
        self.hud_transform.Children.value.append(self.geode) # append gui to navigation node --> head up display
        
    def create_text(self, position, content):
        text = avango.osg.nodes.Text(Size = 0.01, Alignment = 1, Fontname = "VeraBI.ttf", Color = avango.osg.Vec4(1.0,1.0,1.0,1.0))
        text.String.value = content
        text.Position.value = position
        return text
    
    def change_text(self, textid,new_content):
        if textid == 0:
            self.text0.String.value = new_content
        elif textid == 1:
            self.text1.String.value = new_content
        elif textid == 2:
            self.text2.String.value = new_content
        elif textid == 3:
            self.text3.String.value = new_content
