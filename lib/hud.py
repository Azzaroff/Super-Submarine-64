import avango
import avango.osg
import time

from avango.script import field_has_changed

# import modules from local library
from lib.globals import *

class HUD(avango.script.Script):
    
    
    #absolute_transform = avango.osg.SFMatrix()
     # constructor
    def __init__(self):
        self.super(HUD).__init__()
        
    
    def my_constructor(self, SCENE, CAMERA_TANSFORM, PLAYERID):
        
        self.hud_transform = avango.osg.nodes.MatrixTransform()
        self.camera = CAMERA_TANSFORM
        self.id = PLAYERID
        self.Scene = SCENE
        self.hud_transform.Matrix.connect_from(self.camera.AbsoluteMatrix)
        
        #minimap
        self.minimapgroup = avango.osg.nodes.MatrixTransform()
        
        _mat = avango.osg.make_scale_mat(150,150,150) * avango.osg.make_trans_mat(0, 500, 0)
        
        self.player0 = avango.osg.nodes.Sphere(Matrix = _mat)
        self.player0.get_field(8).value = avango.osg.Vec4(1,0,0,1)
        self.player0_transform = avango.osg.nodes.MatrixTransform()
        self.player0_transform.Matrix.connect_from(self.Scene.Player0.group.Matrix)
        self.player0_transform.Children.value.append(self.player0)
        
        self.player1 = avango.osg.nodes.Sphere(Matrix = _mat)
        self.player1.get_field(8).value = avango.osg.Vec4(1,1,0,1)
        self.player1_transform = avango.osg.nodes.MatrixTransform()
        self.player1_transform.Matrix.connect_from(self.Scene.Player1.group.Matrix)
        self.player1_transform.Children.value.append(self.player1)
        
        _mat =  avango.osg.make_scale_mat(.1,.1,.1) * \
                avango.osg.make_rot_mat(math.radians(0),1,0,0) * \
                avango.osg.make_rot_mat(math.radians(-90),1,0,0) * \
                avango.osg.make_trans_mat(120.0, -200.0,250.0)
        self.minimap = avango.osg.nodes.LoadFile(Filename = "data/Map/graben_new_reduced.obj", Matrix = _mat)
        
        self.minimapgroup.Children.value.append(self.minimap)
        self.minimapgroup.Children.value.append(self.player0_transform)
        self.minimapgroup.Children.value.append(self.player1_transform)
        
        
        
        # mode visualization nodes
        if gl_viewing_setup == "desktop":
            #move minimap
            leftminimapoffset = 0.034
            self.minimapgroup.Matrix.value = avango.osg.make_scale_mat(.000015,.000015,.000015) * \
                                                avango.osg.make_rot_mat(math.radians(90), 1, 0, 0) * \
                                                avango.osg.make_trans_mat((-gl_physical_screen_width * 0.5 + leftminimapoffset),gl_physical_screen_height * -0.40,0)
            #move hud
            leftlabeloffset = 0.012
            lefttextoffset = 0.068
            rightlabeloffset = 0.15
            righttextoffset = 0.065
            self.label0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), gl_physical_screen_height * 0.44, 0.0), "Runde:");
            self.text0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), gl_physical_screen_height * 0.44, 0.0), "1/3");
            self.label1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), gl_physical_screen_height * 0.41, 0.0), "Position:");
            self.text1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), gl_physical_screen_height * 0.41, 0.0), "1/2");
            self.label2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), gl_physical_screen_height * 0.44, 0.0), "Zeit:");
            self.text2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), gl_physical_screen_height * 0.44, 0.0), "00:00:000");
            self.label3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), gl_physical_screen_height * 0.41, 0.0), "Rundenzeit:");
            self.text3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), gl_physical_screen_height * 0.41, 0.0), "--:--:---");
            
        elif gl_viewing_setup == "splitscreen":
            #move minimap
            leftminimapoffset = 0.034
            self.minimapgroup.Matrix.value = avango.osg.make_scale_mat(.000015,.000015,.000015) * \
                                                avango.osg.make_rot_mat(math.radians(90), 1, 0, 0) * \
                                                avango.osg.make_trans_mat((-gl_physical_screen_width * 0.5 + leftminimapoffset),gl_physical_screen_height * -0.40,0)
            #move hud
            leftlabeloffset = 0.012
            lefttextoffset = 0.068
            rightlabeloffset = 0.15
            righttextoffset = 0.065
            self.label0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), -.01, 0.0), "Runde:");
            self.text0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), -.01, 0.0), "1/3");
            self.label1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), -.022, 0.0), "Position:");
            self.text1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), -.022, 0.0), "1/2");
            self.label2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), -.01, 0.0), "Zeit:");
            self.text2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), -.01, 0.0), "00:00:000");
            self.label3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), -.022, 0.0), "Rundenzeit:");
            self.text3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), -.022, 0.0), "--:--:---");
            
        self.geode = avango.osg.nodes.LayerGeode(Drawables = [self.label0, self.text0, self.label1, self.text1, self.label2, self.text2, self.label3, self.text3], StateSet = avango.osg.nodes.StateSet(LightingMode = 0), Name="HUD" + str(self.id))
        
        self.Scene.root.Children.value.append(self.hud_transform)
        self.hud_transform.Children.value.append(self.geode) # append gui to navigation node --> head up display
        self.hud_transform.Children.value.append(self.minimapgroup)
        
    def create_text(self, position, content):
        text = avango.osg.nodes.Text(Size = 0.01, Alignment = 1, Fontname = "VeraBI.ttf", Color = avango.osg.Vec4(1.0,1.0,1.0,1.0), BackdropType = 8)
        text.String.value = content
        text.Position.value = position
        return text
    
    def change_text(self, textid,new_content):
        if textid == 0:
            self.text0.String.value = new_content + "/3"
        elif textid == 1:
            self.text1.String.value = new_content
        elif textid == 2:
            self.text2.String.value = new_content
        elif textid == 3:
            self.text3.String.value = new_content
