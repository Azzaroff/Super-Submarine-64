# -*- Mode:Python -*-

##########################################################################
#                                                                        #
# This file is part of Avango.                                           #
#                                                                        #
# Copyright 1997 - 2008 Fraunhofer-Gesellschaft zur Foerderung der       #
# angewandten Forschung (FhG), Munich, Germany.                          #
#                                                                        #
# Avango is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Lesser General Public License as         #
# published by the Free Software Foundation, version 3.                  #
#                                                                        #
# Avango is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU Lesser General Public       #
# License along with Avango. If not, see <http://www.gnu.org/licenses/>. #
#                                                                        #
# Avango is a trademark owned by FhG.                                    #
#                                                                        #
##########################################################################


# import modules from vr application library
from vr_lib.menu import *
from lib.viewing import *
from vr_lib.simple_navigation import *

# import modules from local library
from lib.scene import *
from lib.navigation import *
from lib.gamecontroller import *

import time

class Application:

	# constructor
	def __init__(self):

		# class instancies
		self.Menu = Menu()

		self.Scene = Scene(self.Menu)


		# init lights (if no lights are defined --> default OpenGL headlight is applied)
		self.Scene.make_light(avango.osg.Vec4(0.0,0.0,0.0,1.0), avango.osg.Vec4(0.15,0.15,0.15,1.0), avango.osg.Vec4(0.2,0.2,0.2,1.0), avango.osg.Vec4(-80,300,-50,1.0))
		self.Scene.make_light(avango.osg.Vec4(0.0,0.0,0.0,1.0), avango.osg.Vec4(0.15,0.15,0.15,1.0), avango.osg.Vec4(0.2,0.2,0.2,1.0), avango.osg.Vec4(60,300,-50,1.0))
		self.Scene.make_light(avango.osg.Vec4(0.0,0.0,0.0,1.0), avango.osg.Vec4(0.15,0.15,0.15,1.0), avango.osg.Vec4(0.2,0.2,0.2,1.0), avango.osg.Vec4(-80,300,40,1.0)) 
		self.Scene.make_light(avango.osg.Vec4(0.0,0.0,0.0,1.0), avango.osg.Vec4(0.15,0.15,0.15,1.0), avango.osg.Vec4(0.2,0.2,0.2,1.0), avango.osg.Vec4(60,300,40,1.0)) 
		
	
		# init scene objects
#		_mat =	avango.osg.make_scale_mat(12,12,12) * \
#				avango.osg.make_rot_mat(math.pi,1,0,0) * \
#				avango.osg.make_trans_mat(-7.0,0.0,-5.0)
#		self.museum = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/shader_textured_museum3_small/museum_building.obj", Matrix = _mat)
#		self.Scene.environment_root.Children.value.append(self.museum)
#
#		# exhibition objects
#		_mat = 	avango.osg.make_scale_mat(1.3,1.3,1.3) * \
#				avango.osg.make_rot_mat(math.radians(80.0),0,0,1) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_trans_mat(1.7,1.2,-14.0)
#		self.horse = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/horse.obj", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.horse)
#
#		_mat = 	avango.osg.make_scale_mat(0.0006,0.0006,0.0006) * \
#				avango.osg.make_rot_mat(math.radians(135.0),0,0,1) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_trans_mat(-16.0,0.6,-3.0)
#		self.athene = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/athene.3ds", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.athene)
#
#		_mat = 	avango.osg.make_scale_mat(0.028,0.028,0.028) * \
#				avango.osg.make_rot_mat(math.radians(60.0),0,0,1) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_trans_mat(-2.1,1.45,-0.75)
#		self.buddha = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/64david-sculpture.3ds", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.buddha)
#
#		_mat = 	avango.osg.make_scale_mat(0.008,0.008,0.008) * \
#				avango.osg.make_rot_mat(math.pi,1,0,0) * \
#				avango.osg.make_rot_mat(math.pi,0,1,0) * \
#				avango.osg.make_trans_mat(4.1,1.0,5.8)
#		self.buddha = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/buddha.obj", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.buddha)
#
#		_mat = 	avango.osg.make_scale_mat(0.004,0.004,0.004) * \
#				avango.osg.make_rot_mat(math.pi,-1,0,0)	* \
#				avango.osg.make_trans_mat(2.15,0.97,-3.55)
#		self.chess = avango.osg.nodes.Loaself.SCENE.finish_group.get_bounding_spheredFile(Filename = "/opt/3d_models/exhibition/chess-game.obj", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.chess)
#
#		_mat = 	avango.osg.make_scale_mat(0.14,0.14,0.14) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0)	* \
#				avango.osg.make_trans_mat(-1.7,1.0,-17.65)
#		self.dino = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/dino.obj", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.dino)
#
#		_mat = 	avango.osg.make_scale_mat(0.055,0.055,0.055) * \
#				avango.osg.make_rot_mat(math.pi,1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(65.0),0,1,0) * \
#				avango.osg.make_trans_mat(-15.4,1.1,-14.25)
#		self.shoe = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/shoe.obj", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.shoe)
#
#		_mat = 	avango.osg.make_scale_mat(0.00008,0.00008,0.00008) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(90.0),0,-1,0) * \
#				avango.osg.make_trans_mat(-12.5,1.2,-17.8)
#		self.ear = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/ear-medical.3ds", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.ear)
#
#		_mat = 	avango.osg.make_scale_mat(0.00013,0.00013,0.00013) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(90.0),0,0,0) * \
#				avango.osg.make_trans_mat(-8.7,1.1,-14.0)
#		self.boat = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/Diesel_Tug.3ds", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.boat)
#
#		_mat = 	avango.osg.make_scale_mat(0.03,0.03,0.03) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(135),0,1,0) * \
#				avango.osg.make_trans_mat(-18.0,0.0,4.0)
#		self.passat = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/cars/passat/passat.3ds", Matrix = _mat)
#		self.Scene.object_root.Children.value.append(self.passat)


		_mat = 	avango.osg.make_scale_mat(.1,.1,.1) * \
				avango.osg.make_rot_mat(math.radians(0),1,0,0) * \
				avango.osg.make_rot_mat(math.radians(-90),1,0,0) * \
				avango.osg.make_trans_mat(120.0, -200.0,250.0)
		self.landscape = avango.osg.nodes.LoadFile(Filename = "data/Map/graben_new.obj", Matrix = _mat)
		self.Scene.environment_root.Children.value.append(self.landscape)
		
		#self.Scene.deko_root.Matrix.value = avango.osg.make_trans_mat(120.0, -200.0,250.0)
		
		#Ziel
		_mat = avango.osg.make_rot_mat(math.radians(270),1,0,0) * avango.osg.make_trans_mat(1170.637451, -84.802658, -63.487019)
		self.finish_1 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_ident_mat())
		self.finish_2 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_rot_mat(math.radians(90),0,1,0) * avango.osg.make_trans_mat(-145, 0, 0))
		self.Scene.finish_group = avango.osg.nodes.MatrixTransform(Matrix = _mat)
		self.Scene.finish_group.Children.value = [self.finish_1, self.finish_2]
		self.Scene.deko_root.Children.value.append(self.Scene.finish_group)
		
		#Checkpoint1
		#-287.149078 -63.845512 830.017517
		_mat = avango.osg.make_rot_mat(math.radians(270),1,0,0) * avango.osg.make_trans_mat(-287.149078, -63.845512, 830.017517)
		self.checkpoint1_1 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_ident_mat())
		self.checkpoint1_2 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_rot_mat(math.radians(90),0,0,1) * avango.osg.make_trans_mat(-145, 0, 0))
		self.Scene.checkpoint1_group = avango.osg.nodes.MatrixTransform(Matrix = _mat)
		self.Scene.checkpoint1_group.Children.value = [self.checkpoint1_1, self.checkpoint1_2]
		self.Scene.deko_root.Children.value.append(self.Scene.checkpoint1_group)
		
		

		#Checkpoint2
		#-1070.442871 -79.164711 -329.316742
		#-901.965027 -57.412403 -444.109253
		_mat = avango.osg.make_rot_mat(math.radians(270),1,0,0) * avango.osg.make_trans_mat(-1060.442871, -70.164711, -329.316742)
		self.checkpoint2_1 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_rot_mat(math.radians(20),0,1,0) * avango.osg.make_rot_mat(math.radians(180),0,0,1))
		self.checkpoint2_2 = avango.osg.nodes.LoadFile(Filename = "data/weed2.obj", Matrix = avango.osg.make_rot_mat(math.radians(20),0,1,0) * avango.osg.make_rot_mat(math.radians(180),0,0,1) * avango.osg.make_trans_mat(130, 0, 0))
		self.Scene.checkpoint2_group = avango.osg.nodes.MatrixTransform(Matrix = _mat)
		self.Scene.checkpoint2_group.Children.value = [self.checkpoint2_1, self.checkpoint2_2]
		self.Scene.deko_root.Children.value.append(self.Scene.checkpoint2_group)
		
		_mat = 	avango.osg.make_scale_mat(0.013,0.013,0.013) * \
				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
				avango.osg.make_rot_mat(math.radians(90.0),0,0,0) * \
				avango.osg.make_trans_mat(-855, -64, 1191)
		self.boat = avango.osg.nodes.LoadFile(Filename = "/opt/3d_models/exhibition/Diesel_Tug.3ds", Matrix = _mat)
		self.Scene.deko_root.Children.value.append(self.boat)
		
		#-320.791777  -50.348597 -631.051344
		_mat = 	avango.osg.make_scale_mat(10,10,10) * \
				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
				avango.osg.make_rot_mat(math.radians(258.0),0,1,0) * \
				avango.osg.make_trans_mat(-325.791777, -50.348597, -636.051344)
		self.shark = avango.osg.nodes.LoadFile(Filename = "data/Deko/Fische/shark/Great White.lwo", Matrix = _mat)
		self.Scene.deko_root.Children.value.append(self.shark)
		

#		_mat = 	avango.osg.make_scale_mat(10,10,10) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(180.0),0,1,0) * \
#				avango.osg.make_trans_mat(1300.791777, 40.348597, 90.051344)
#		self.fish1 = avango.osg.nodes.LoadFile(Filename = "data/Deko/Fische/TropicalFish_obj/TropicalFish03.obj", Matrix = _mat)
#		self.Scene.deko_root.Children.value.append(self.fish1)
#		
#		_mat = 	avango.osg.make_scale_mat(10,10,10) * \
#				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
#				avango.osg.make_rot_mat(math.radians(180.0),0,1,0) * \
#				avango.osg.make_trans_mat(1200.791777, 30.348597, 90.051344)
#		self.fish2 = avango.osg.nodes.LoadFile(Filename = "data/Deko/Fische/TropicalFish_obj/TropicalFish02.obj", Matrix = _mat)
#		self.Scene.deko_root.Children.value.append(self.fish2)
		
		#1219.455259  -24.842079 -628.119584
		_mat = 	avango.osg.make_scale_mat(2,2,2) * \
				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
				avango.osg.make_rot_mat(math.radians(-90.0),0,1,0) * \
				avango.osg.make_trans_mat(1019.791777, -24.348597, -628.051344)
		self.whale = avango.osg.nodes.LoadFile(Filename = "data/Deko/Fische/whale/whale.3ds", Matrix = _mat)
		self.Scene.deko_root.Children.value.append(self.whale)
		
		
		# 634.717487   26.079331  942.262169
		_mat = 	avango.osg.make_scale_mat(0.01,0.01,0.01) * \
				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
				avango.osg.make_rot_mat(math.radians(90.0),0,1,0) * \
				avango.osg.make_trans_mat(634.717487, 50.079331, 935.262169)
		self.turtle = avango.osg.nodes.LoadFile(Filename = "data/Deko/TURTLE/TURTLE/TURTLE_L.3DS", Matrix = _mat)
		self.Scene.deko_root.Children.value.append(self.turtle)

		_mat = 	avango.osg.make_scale_mat(0.13,.13,.13) * \
				avango.osg.make_rot_mat(math.pi*0.5,-1,0,0) * \
				avango.osg.make_rot_mat(math.radians(90.0),0,0,0) * \
				avango.osg.make_trans_mat(-858, -38.5, -722)
		self.anchor = avango.osg.nodes.LoadFile(Filename = "data/Deko/anchor1.obj", Matrix = _mat)
		self.Scene.deko_root.Children.value.append(self.anchor)
		
		#bounding sphere buggy deswegen dieser hack
		self.anchorsphere = avango.osg.nodes.Sphere(Radius = 23, Matrix = avango.osg.make_trans_mat(-858, -24.5, -722))
		#self.Scene.deko_root.Children.value.append(self.anchorsphere)
		
		#Collision Map
		
		self.collision_root = avango.osg.nodes.Group()
		
		_mat = 	avango.osg.make_scale_mat(.1,.1,.1) * \
				avango.osg.make_rot_mat(math.radians(0),1,0,0) * \
				avango.osg.make_rot_mat(math.radians(-90),1,0,0) * \
				avango.osg.make_trans_mat(120.0, -200.0,250.0)
		self.collision_landscape = avango.osg.nodes.LoadFile(Filename = "data/Map/graben_new_reduced.obj", Matrix = _mat)
		
		self.collision_root.Children.value.append(self.collision_landscape)
		self.collision_root.Children.value.append(self.boat)
		self.collision_root.Children.value.append(self.anchorsphere)
		self.collision_root.Children.value.append(self.turtle)
		self.collision_root.Children.value.append(self.shark)
		self.collision_root.Children.value.append(self.whale)
		
		
		
		#_mat = avango.osg.make_scale_mat(10000,10000,10000) * \
        #avango.osg.make_rot_mat(math.radians(180),1,0,0) * \
        #avango.osg.make_rot_mat(math.radians(90),1,0,0)
		#self.skybox = avango.osg.nodes.LoadFile(Filename = "data/Skybox/skybox.obj", Matrix = _mat)
		#self.Scene.skybox_root.Children.value.append(self.skybox)
		
		#snow stuff
		self.precip, self.snowstate = make_precipitation()
		self.sky, self.skyfog = make_sky()
		
		#self.skyfog.Color.connect_from(self.precip.Fog.value.Color)
		self.skyfog.Color.value = avango.osg.Vec4(0.0,0.6,0.8, 3.0)
		
		self.Scene.environment_root.StateSet.value = self.snowstate
		self.Scene.skybox_root.Children.value.append(self.sky)
		self.Scene.environment_root.Children.value.append(self.precip)

			#self.Scene.navigation_transform.Matrix.value = avango.osg.make_trans_mat(0.0,0.0,0.0)


		self.Spacemouse = SpacemouseDevice()

		self.ImpactController = GameControllerDevice()
		self.SaitekController = GameControllerDevice2()

		#self.Navigation = Navigation()
		#self.Navigation.my_constructor(self.Scene, self.ViewingSetup, self.ImpactController)
		self.snow(0.3)
		self.time_sav = time.time()
		self.Scene.GameController = GAMECONTROLLER()
		
		if gl_viewing_setup == "desktop" or gl_viewing_setup == "anaglyph":
			self.Scene.Player0 = Player()
			self.Scene.Player0.my_constructor(self.Scene, self.ImpactController, "./data/Submarine/My_YellowSubmarine.obj", self.collision_root, 0, self.time_sav)
			self.Scene.Player0.create_hud()
			self.Scene.GameController.my_constructor(self.Scene, 1)
		elif gl_viewing_setup == "splitscreen":
			self.Scene.Player0 = Player()
			self.Scene.Player1 = Player()
			self.Scene.Player0.my_constructor(self.Scene, self.ImpactController, "./data/Submarine/My_YellowSubmarine.obj", self.collision_root, 0, self.time_sav)
			self.Scene.Player1.my_constructor(self.Scene, self.SaitekController, "./data/Submarine/My_RedSubmarine.obj", self.collision_root, 1, self.time_sav)
			self.Scene.Player0.create_hud()
			self.Scene.Player1.create_hud()
			self.Scene.GameController.my_constructor(self.Scene, 2)
		
		#print self.Scene.Player0
		#print self.Scene.Player1
		
		

		self.Scene.GameController.start_countdown(10)

		#####  run evaluation and render loop  #####		
		self.ViewingSetup = ViewingSetup(self.Scene, self.Menu)
		
		self.ViewingSetup.start_render_loop()
		
	def snow(self, value):
		self.precip.Snow.value = value
		self.precip.ParticleSize.value = 0.1
		self.precip.ParticleSpeed.value = 0.05
		self.precip.MaximumParticleDensity.value = 0.05
		self.precip.NearTransition.value = 0.00
		self.precip.FarTransition.value = 0.00
		self.precip.Fog.value.Density.value *= 0.8
		self.precip.Fog.value.Color.value = avango.osg.Vec4(0.0,0.6,0.8, 0.6)
		self.skyfog.Density.value = self.precip.Fog.value.Density.value * 0.0
		self.precip.Wind.value = avango.osg.Vec3( 0, 0.25, 0)
		
	def rain(self, value):
		self.precip.Rain = value
		self.precip.Fog.value.Density.value *= 1.5
		self.skyfog.Density.value = self.precip.Fog.value.Density.value * 0.2
		self.precip.Wind.value = avango.osg.Vec3(0, 0, 0.5)
	
def make_sky():
	_mat = avango.osg.make_scale_mat(10000,10000,10000) * \
    avango.osg.make_rot_mat(math.radians(180),1,0,0) * \
    avango.osg.make_rot_mat(math.radians(90),1,0,0)
	sky = avango.osg.nodes.LoadFile(Filename = "data/Skybox/skybox.obj", Matrix = _mat)
	skystate = avango.osg.nodes.StateSet(Fog = avango.osg.nodes.Fog(), FogMode = 1)
	sky.StateSet.value = skystate
	return sky, skystate.Fog.value

		
def make_precipitation():
	# setup a precipitation effect with fog
	precip = avango.osg.particle.nodes.PrecipitationEffect(Fog = avango.osg.nodes.Fog())
	precip.CellSize.value = avango.osg.Vec3(1,1,1)

	# setup stateset
	state = avango.osg.nodes.StateSet(FogMode = 1, Fog = precip.Fog.value)

	return precip, state


Application = Application()



