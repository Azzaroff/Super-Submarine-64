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
        self.player0.get_field(8).value = avango.osg.Vec4(1,1,0,1)
        self.player0_transform = avango.osg.nodes.MatrixTransform()
        self.player0_transform.Matrix.connect_from(self.Scene.Player0.group.Matrix)
        self.player0_transform.Children.value.append(self.player0)
        
        if gl_viewing_setup == "splitscreen":
            self.player1 = avango.osg.nodes.Sphere(Matrix = _mat)
            self.player1.get_field(8).value = avango.osg.Vec4(1,0,0,1)
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
        if gl_viewing_setup == "splitscreen":
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
            self.label0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), gl_physical_screen_height * 0.44, 0.0), "Runde:", 0.01, 1, 32);
            num_of_laps = "1/" + "%d" % (self.Scene.GameController.number_of_laps)
            self.text0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), gl_physical_screen_height * 0.44, 0.0), num_of_laps, 0.01, 1, 32);
            self.label1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), gl_physical_screen_height * 0.41, 0.0), "Position:", 0.01, 1, 32);
            self.text1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), gl_physical_screen_height * 0.41, 0.0), "1/1", 0.01, 1, 32);
            self.label2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), gl_physical_screen_height * 0.44, 0.0), "Zeit:", 0.01, 1, 32);
            self.text2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), gl_physical_screen_height * 0.44, 0.0), "--:--:---", 0.01, 1, 32);
            self.label3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), gl_physical_screen_height * 0.41, 0.0), "Rundenzeit:", 0.01, 1, 32);
            self.text3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), gl_physical_screen_height * 0.41, 0.0), "--:--:---", 0.01, 1, 32);
            
            self.text4 = self.create_text(avango.osg.Vec3(0, 0, 0.0), "3", 0.05, 3, 120);
            
            self.label5 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), gl_physical_screen_height * 0.38, 0.0), "Beste Runde:", 0.01, 1, 32);
            self.text5 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), gl_physical_screen_height * 0.38, 0.0), "--:--:---", 0.01, 1, 32);
            
            
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
            self.label0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), -.01, 0.0), "Runde:", 0.01, 1, 32);
            num_of_laps = "1/" + "%d" % (self.Scene.GameController.number_of_laps)
            self.text0 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), -.01, 0.0), num_of_laps, 0.01, 1, 32);
            self.label1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + leftlabeloffset), -.022, 0.0), "Position:", 0.01, 1, 32);
            self.text1 = self.create_text(avango.osg.Vec3((-gl_physical_screen_width * 0.5 + lefttextoffset), -.022, 0.0), "1/2", 0.01, 1, 32);
            self.label2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), -.01, 0.0), "Zeit:", 0.01, 1, 32);
            self.text2 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), -.01, 0.0), "--:--:---", 0.01, 1, 32);
            self.label3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), -.022, 0.0), "Rundenzeit:", 0.01, 1, 32);
            self.text3 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), -.022, 0.0), "--:--:---", 0.01, 1, 32);
            
            self.text4 = self.create_text(avango.osg.Vec3(-.014, -.1, 0.0), "3", 0.05, 2, 120);
            
            self.label5 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - rightlabeloffset), -.034, 0.0), "Beste Runde:", 0.01, 1, 32);
            self.text5 = self.create_text(avango.osg.Vec3((gl_physical_screen_width * 0.5 - righttextoffset), -.034, 0.0), "--:--:---", 0.01, 1, 32);
            
        self.geode = avango.osg.nodes.LayerGeode(Drawables = [self.label0, self.text0, self.label1, self.text1, self.label2, self.text2, self.label3, self.text3, self.text4, self.label5, self.text5], StateSet = avango.osg.nodes.StateSet(LightingMode = 0), Name="HUD" + str(self.id))
        
        self.Scene.root.Children.value.append(self.hud_transform)
        self.hud_transform.Children.value.append(self.geode) # append gui to navigation node --> head up display
        self.hud_transform.Children.value.append(self.minimapgroup)
        
    def create_text(self, position, content, size = 0.01, align = 1, resolution = 32):
        text = avango.osg.nodes.Text(Size = size, Alignment = align, Fontname = "VeraBI.ttf", Color = avango.osg.Vec4(1.0,1.0,1.0,1.0), BackdropType = 8, Resolution = resolution)
        text.String.value = content
        text.Position.value = position
        return text
    
    def change_text(self, textid,new_content):
        if textid == 0:
            num_of_laps = "/" + "%d" % (self.Scene.GameController.number_of_laps)
            self.text0.String.value = new_content + num_of_laps
        elif textid == 1:
            self.text1.String.value = new_content
        elif textid == 2:
            self.text2.String.value = new_content
        elif textid == 3:
            self.text3.String.value = new_content
        elif textid == 4:
            self.text4.String.value = new_content
        elif textid == 5:
            self.text5.String.value = new_content

    def show_results(self, player0_data = [], player1_data = []):
        self.label0.String.value = ""
        self.label1.String.value = ""
        self.label2.String.value = ""
        self.label3.String.value = ""
        self.label5.String.value = ""
        self.text0.String.value = ""
        self.text1.String.value = ""
        self.text2.String.value = ""
        self.text3.String.value = ""
        self.text5.String.value = ""
        
        if gl_viewing_setup == "desktop":
            self.score_label0 = self.create_text(avango.osg.Vec3(0, gl_physical_screen_height * 0.44, 0.0), "Gewonnen!", 0.01, 1, 32);        
            self.score_label1 = self.create_text(avango.osg.Vec3(-0.065, gl_physical_screen_height * 0.41, 0.0), "Rundenzeit", 0.01, 1, 32);
            self.score_label2 = self.create_text(avango.osg.Vec3(0.065, gl_physical_screen_height * 0.41, 0.0), "Position", 0.01, 1, 32);
            help = []
            help.append(self.score_label0)
            help.append(self.score_label1)
            help.append(self.score_label2)
            #print data
            for x in range(0, len(player0_data)):
                time = player0_data[x]
                seconds = math.floor(time)
                minutes = math.floor(seconds / 60)
                milliseconds = math.floor((time - seconds)*1000)
                seconds = seconds - (minutes * 60)
                text = "%02d%s%02d%s%02d" % (minutes, ":", seconds, ":", milliseconds)
                timeentry = self.create_text(avango.osg.Vec3(-0.065, gl_physical_screen_height * (0.38-0.03*x), 0.0), text, 0.01, 1, 32);
                positionentry = self.create_text(avango.osg.Vec3(0.065, gl_physical_screen_height * (0.38-0.03*x), 0.0), "1/1", 0.01, 1, 32);
                help.append(timeentry)
                help.append(positionentry)               
            
            self.geode2 = avango.osg.nodes.LayerGeode(Drawables = help, StateSet = avango.osg.nodes.StateSet(LightingMode = 0), Name="HUD" + str(self.id))
            self.hud_transform.Children.value.append(self.geode2)
            
        elif gl_viewing_setup == "splitscreen":
            self.score_label0 = self.create_text(avango.osg.Vec3(0, -.01, 0.0), "Gewonnen!", 0.01, 1, 32);        
            self.score_label1 = self.create_text(avango.osg.Vec3(-0.065, -.022, 0.0), "Rundenzeit", 0.01, 1, 32);
            self.score_label2 = self.create_text(avango.osg.Vec3(0.065, -.022, 0.0), "Position", 0.01, 1, 32);
            help = []
            help.append(self.score_label0)
            help.append(self.score_label1)
            help.append(self.score_label2)
            sum0 = 0
            sum1 = 0
            #print data
            for x in range(0, len(player0_data)):
                time0 = player0_data[x]
                time1 = player1_data[x]
                sum0 += time0
                sum1 += time1                
                seconds = math.floor(time0)
                minutes = math.floor(seconds / 60)
                milliseconds = math.floor((time0 - seconds)*1000)
                seconds = seconds - (minutes * 60)
                text = "%02d%s%02d%s%02d" % (minutes, ":", seconds, ":", milliseconds)
                timeentry = self.create_text(avango.osg.Vec3(-0.065, (-0.034-0.012*x), 0.0), text, 0.01, 1, 32);
                positionentry = self.create_text(avango.osg.Vec3(0.065, (-0.034-0.012*x), 0.0), "1/2", 0.01, 1, 32);
                if sum0 > sum1:
                    positionentry.String.value = "2/2"
                help.append(timeentry)
                help.append(positionentry)
            
            if sum0 > sum1:
                self.score_label0.String.value = "Verloren!"
            self.geode2 = avango.osg.nodes.LayerGeode(Drawables = help, StateSet = avango.osg.nodes.StateSet(LightingMode = 0), Name="HUD" + str(self.id))
            self.hud_transform.Children.value.append(self.geode2)
            
