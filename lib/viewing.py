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

import avango.osg.viewer
import avango.daemon
import math
import sys

# import modules from local library
from lib.globals import *

class ViewingSetup:

	# contructor
	def __init__(self, SCENE, MENU):
		
		# init viewing setup
		if gl_viewing_setup == "desktop":
			self.setup = DesktopSetup(SCENE)
			
		elif gl_viewing_setup == "splitscreen":
			self.setup = SplitScreenSetup(SCENE)

		elif gl_viewing_setup == "lcd":
			self.setup = LcdWallStereoSetup(SCENE)

		elif gl_viewing_setup == "lcd_splitscreen":
			self.setup = LcdWallSplitScreenStereoSetup(SCENE)			
	
		else: # viewing setup not supported

			print "Viewing Setup [{0}] NOT supported".format(gl_viewing_setup)
			sys.exit(1) # terminate application
		
		
		# reference
		self.viewer = self.setup.viewer
		self.events = self.setup.events


		# init mouse interaction with application menus
		MENU.init_mouse_menu_interaction(SCENE.navigation_transform, self.setup)

	# functions
	def start_render_loop(self):

		self.viewer.frame() # render a frame
		self.viewer.StatsMode.value = 1 # enable frame rate visualization
		self.viewer.ThreadingModel.value = 2

		self.viewer.run() # start render loop


class DesktopSetup:

	# contructor
	def __init__(self, SCENE):

		# init window
		self.window = avango.osg.viewer.nodes.GraphicsWindow()
		self.window.ScreenIdentifier.value = ":0.0"
		self.window.AutoHeight.value = False
		if anaglyph_flag:
			self.window.StereoMode.value = avango.osg.viewer.stereo_mode.STEREO_MODE_ANAGLYPHIC
		else:
			self.window.StereoMode.value = avango.osg.viewer.stereo_mode.STEREO_MODE_NONE
		
		# screen parameters
		self.window.ShowCursor.value = False
		self.window.ToggleFullScreen.value = True
		self.window.WantedWidth.value = gl_pixels_width
		self.window.WantedHeight.value = gl_pixels_height
		self.window.WantedPositionX.value = gl_wanted_position_x
		self.window.WantedPositionY.value = gl_wanted_position_y
		self.window.RealScreenWidth.value = gl_physical_screen_width
		self.window.RealScreenHeight.value = gl_physical_screen_height

		# init camera
		self.camera = avango.osg.viewer.nodes.Camera(Window = self.window)
		self.camera.ScreenTransform.value = gl_screen_transform
		self.camera.BackgroundColor.value = avango.osg.Vec4(0,0.1,1,1)#gl_background_color
		self.camera.Far.value = 40000000
		
		if anaglyph_flag:
			self.eye_offset = 0.65
			self.camera.EyeOffset.value = self.eye_offset * 0.01

		# init field connections
		#self.camera.ViewerTransform.connect_from(SCENE.navigation_transform.Matrix)
		self.camera.ViewerTransform.connect_from(SCENE.Player0.camera_absolute.AbsoluteMatrix)

		if gl_headtracking_flag == False:
			self.tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head0", TransmitterOffset = gl_transmitter_offset) # init tracking sensor
			self.camera.EyeTransform.connect_from(self.tracking_sensor.Matrix)

		else:
			self.camera.EyeTransform.value = gl_eye_transform # fixed head position

		# init viewer
		self.viewer = avango.osg.viewer.nodes.Viewer(Scene = SCENE.root, MasterCamera = self.camera)

		# init simple mouse events
		self.events = avango.osg.viewer.nodes.EventFields(View = self.viewer)

		self.window.DragEvent.connect_from(self.events.DragEvent)
		self.window.MoveEvent.connect_from(self.events.MoveEvent)
		self.window.ToggleFullScreen.connect_from(self.events.KeyAltReturn)


		self.init_ground_plane(SCENE)

	# functions
	def init_ground_plane(self, SCENE):
		if gl_ground_flag == True:
			self.ground_panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.5,0.5,0.3,0.75), Width = 1.0, Height = 1.0)
			self.ground_geode = avango.osg.nodes.LayerGeode(Drawables = [self.ground_panel], StateSet = avango.osg.nodes.StateSet(BlendMode = 1, LightingMode = 0, RenderingHint = 2))
			self.ground_transform = avango.osg.nodes.MatrixTransform(Children = [self.ground_geode])
			self.ground_transform.Matrix.value = gl_ground_plane_transform
			SCENE.root.Children.value.append(self.ground_transform)

class SplitScreenSetup:

	# contructor
	def __init__(self, SCENE):

		# parameters
		self.eye_offset1 = 0.065
		self.eye_offset2 = 0.065
		
		# init window
		self.window = avango.osg.viewer.nodes.GraphicsWindow()
		self.window.ShowCursor.value = False
		self.window.ToggleFullScreen.value = True
		self.window.ScreenIdentifier.value = ":0.0"
		self.window.ShowCursor.value = False
		self.window.AutoHeight.value = False
		self.window.Decoration.value = False
		#self.window.StereoMode.value = avango.osg.viewer.stereo_mode.STEREO_MODE_NONE
		if anaglyph_flag:
			self.window.StereoMode.value = avango.osg.viewer.stereo_mode.STEREO_MODE_ANAGLYPHIC
		else:
			self.window.StereoMode.value = avango.osg.viewer.stereo_mode.STEREO_MODE_NONE
						
		# screen parameters
		self.window.WantedWidth.value = gl_pixels_width
		self.window.WantedHeight.value = gl_pixels_height
		self.window.WantedPositionX.value = gl_wanted_position_x
		self.window.WantedPositionY.value = gl_wanted_position_y
		self.window.RealScreenWidth.value = gl_physical_screen_width
		self.window.RealScreenHeight.value = gl_physical_screen_height

		# init camera 1
		self.camera1 = avango.osg.viewer.nodes.Camera(Window = self.window)
		if anaglyph_flag:
			self.camera1.EyeOffset.value = self.eye_offset1 * 0.01
		self.camera1.Far.value = 40000000.0
		self.camera1.ScreenTransform.value = gl_screen_transform * avango.osg.make_trans_mat(0, 0.03, 0)
		self.camera1.BackgroundColor.value = gl_background_color
		
		# init camera 2
		self.camera2 = avango.osg.viewer.nodes.Camera(Window = self.window)
		if anaglyph_flag:
			self.camera2.EyeOffset.value = self.eye_offset1 * 0.01
		self.camera2.Far.value = 40000000.0
		self.camera2.ScreenTransform.value = gl_screen_transform * avango.osg.make_trans_mat(0, -0.054, 0)
		self.camera2.BackgroundColor.value = gl_background_color
		
		self.camera1.ViewerTransform.connect_from(SCENE.Player0.camera_absolute.AbsoluteMatrix)
		self.camera2.ViewerTransform.connect_from(SCENE.Player1.camera_absolute.AbsoluteMatrix)

		self.camera1.Viewport.value = avango.osg.Vec4(0.0, 0.5, 1.0, 1.0)		
		self.camera2.Viewport.value = avango.osg.Vec4(0.0, 0.0, 1.0, 0.5)

		if gl_headtracking_flag == False:
			self.tracking_sensor1 = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head0", TransmitterOffset = gl_transmitter_offset) # init tracking sensor
			self.tracking_sensor2 = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head1", TransmitterOffset = gl_transmitter_offset) # init tracking sensor

			# connect headtracking sensor data with camera EyeTransform here
			self.camera1.EyeTransform.connect_from(self.tracking_sensor1.Matrix)
			self.camera2.EyeTransform.connect_from(self.tracking_sensor2.Matrix)			

		else:
			self.camera1.EyeTransform.value = gl_eye_transform # fixed head position
			self.camera2.EyeTransform.value = gl_eye_transform # fixed head position


		# init viewer
		self.viewer = avango.osg.viewer.nodes.Viewer(Scene = SCENE.root, MasterCamera = self.camera1, SlaveCameras = [self.camera2])

		# init simple mouse events
		self.events = avango.osg.viewer.nodes.EventFields(View = self.viewer)

		self.window.DragEvent.connect_from(self.events.DragEvent)
		self.window.MoveEvent.connect_from(self.events.MoveEvent)
		self.window.ToggleFullScreen.connect_from(self.events.KeyAltReturn)


		self.init_ground_plane(SCENE)

	# functions
	def init_ground_plane(self, SCENE):
		if gl_ground_flag == True:
			self.ground_panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.5,0.5,0.3,0.75), Width = 1.0, Height = 1.0)
			self.ground_geode = avango.osg.nodes.LayerGeode(Drawables = [self.ground_panel], StateSet = avango.osg.nodes.StateSet(BlendMode = 1, LightingMode = 0, RenderingHint = 2))
			self.ground_transform = avango.osg.nodes.MatrixTransform(Children = [self.ground_geode])
			self.ground_transform.Matrix.value = gl_ground_plane_transform
			SCENE.root.Children.value.append(self.ground_transform)


class LcdWallStereoSetup:

	# contructor
	def __init__(self, SCENE):

		# parameters
		self.eye_offset = 0.065

		self.near = 0.2
		self.far = 40000000.0

		_config_path = "/opt/avango/LCD-calibration/screen_config.txt"

		# get the screen parameters from external description
		try:
			_file = open(_config_path, "r")
			_lines = _file.readlines()
			
			_line = _lines[0].split() # read 1st line --> screen dimensions

			self.physical_screen_width = float(_line[0]) # physical screen width in meter
			self.physical_screen_height = float(_line[1]) # physical screen height in meter
			self.screen_width = int(_line[2]) # screen width in pixel
			self.screen_height = int(_line[3]) # screen height in pixel
									
			# right eye parameters									
			_line = _lines[3].split()

			self.screen_id = _line[0]						
			self.right_screen_transform = avango.osg.make_trans_mat(float(_line[5]), float(_line[6]), float(_line[7]))
			self.right_width_offset		= int(_line[1]) # screen width offset in pixel
			self.right_height_offset 	= int(_line[2]) # screen width offset in pixel
			self.right_width_dim	 	= int(_line[3]) # screen width dimension in pixel
			self.right_height_dim 		= int(_line[4]) # screen width dimension in pixel

			# left eye parameters
			_line = _lines[4].split()

			self.left_screen_transform = avango.osg.make_trans_mat(float(_line[5]), float(_line[6]), float(_line[7]))
			self.left_width_offset	= int(_line[1]) # screen width offset in pixel
			self.left_height_offset = int(_line[2]) # screen width offset in pixel
			self.left_width_dim	= int(_line[3]) # screen width dimension in pixel
			self.left_height_dim 	= int(_line[4]) # screen width dimension in pixel
			
			_file.close()

		except IOError:
			print "error while loading screen config file"
			sys.exit(1)
		
		else:

			# right eye camera setup
			self.right_window = avango.osg.viewer.nodes.GraphicsWindow()
			self.right_window.ScreenIdentifier.value = self.screen_id
			self.right_window.ShowCursor.value = False
			self.right_window.Decoration.value = False
			self.right_window.AutoHeight.value = False
			self.right_window.RealScreenWidth.value = self.physical_screen_width
			self.right_window.RealScreenHeight.value = self.physical_screen_height		
			self.right_window.WantedPositionX.value = self.right_width_offset
			self.right_window.WantedPositionY.value = self.right_height_offset
			self.right_window.WantedWidth.value = self.right_width_dim # in pixel
			self.right_window.WantedHeight.value = self.right_height_dim

			self.right_camera = avango.osg.viewer.nodes.Camera(Window = self.right_window)
			self.right_camera.EyeOffset.value = self.eye_offset * 0.5
			self.right_camera.Far.value = self.far
			self.right_camera.ScreenTransform.value = self.right_screen_transform
			self.right_camera.BackgroundColor.value = gl_background_color
		
			# left eye camera setup
			self.left_window = avango.osg.viewer.nodes.GraphicsWindow()
			self.left_window.ScreenIdentifier.value = self.screen_id
			self.left_window.ShowCursor.value = False
			self.left_window.Decoration.value = False
			self.left_window.AutoHeight.value = False
			self.left_window.RealScreenWidth.value = self.physical_screen_width
			self.left_window.RealScreenHeight.value = self.physical_screen_height		
			self.left_window.WantedPositionX.value = self.left_width_offset
			self.left_window.WantedPositionY.value = self.left_height_offset
			self.left_window.WantedWidth.value = self.left_width_dim # in pixel
			self.left_window.WantedHeight.value = self.left_height_dim

			self.left_camera = avango.osg.viewer.nodes.Camera(Window = self.left_window)
			self.left_camera.EyeOffset.value = self.eye_offset * -0.5
			self.left_camera.Far.value = self.far
			self.left_camera.ScreenTransform.value = self.left_screen_transform
			self.left_camera.BackgroundColor.value = gl_background_color


			if gl_headtracking_flag == True:
				self.tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head1", TransmitterOffset = avango.osg.make_trans_mat(0.0,-1.42,2.0)) # init tracking sensor
				self.right_camera.EyeTransform.connect_from(self.tracking_sensor.Matrix)
				self.left_camera.EyeTransform.connect_from(self.tracking_sensor.Matrix)
			
			else:
				self.right_camera.EyeTransform.value = avango.osg.make_trans_mat(0.0,0.0,2.0) # fixed head position
				self.left_camera.EyeTransform.value = avango.osg.make_trans_mat(0.0,0.0,2.0) # fixed head position


			# init viewer
			self.viewer = avango.osg.viewer.nodes.Viewer(Scene = SCENE.root, MasterCamera = self.right_camera, SlaveCameras = [self.left_camera])

			# init simple mouse events
			self.events = avango.osg.viewer.nodes.EventFields(View = self.viewer)

			self.right_window.DragEvent.connect_from(self.events.DragEvent)
			self.right_window.MoveEvent.connect_from(self.events.MoveEvent)


			#self.init_ground_plane(SCENE)

	# functions
	def init_ground_plane(self, SCENE):
		if gl_ground_flag == True:
			self.ground_panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.5,0.5,0.3,0.75), Width = 1.0, Height = 1.0)
			self.ground_geode = avango.osg.nodes.LayerGeode(Drawables = [self.ground_panel], StateSet = avango.osg.nodes.StateSet(BlendMode = 1, LightingMode = 0, RenderingHint = 2))
			self.ground_transform = avango.osg.nodes.MatrixTransform(Children = [self.ground_geode])
			self.ground_transform.Matrix.value = gl_ground_plane_transform
			SCENE.root.Children.value.append(self.ground_transform)


class LcdWallSplitScreenStereoSetup:

	# contructor
	def __init__(self, SCENE):

		# parameters
		self.eye_offset1 = 0.065
		self.eye_offset2 = 0.065

		self.near = 0.2
		self.far = 40000000.0

		_config_path = "/opt/avango/LCD-calibration/screen_config.txt"

		# get the screen parameters from external description
		try:
			_file = open(_config_path, "r")
			_lines = _file.readlines()
			
			_line = _lines[0].split() # read 1st line --> screen dimensions

			self.physical_screen_width = float(_line[0]) # physical screen width in meter
			self.physical_screen_height = float(_line[1]) # physical screen height in meter
			self.screen_width = int(_line[2]) # screen width in pixel
			self.screen_height = int(_line[3]) # screen height in pixel
									
			# right eye parameters									
			_line = _lines[3].split()

			self.screen_id = _line[0]						
			self.right_screen_transform = avango.osg.make_trans_mat(float(_line[5]), float(_line[6]), float(_line[7]))
			self.right_width_offset		= int(_line[1]) # screen width offset in pixel
			self.right_height_offset 	= int(_line[2]) # screen width offset in pixel
			self.right_width_dim	 	= int(_line[3]) # screen width dimension in pixel
			self.right_height_dim 		= int(_line[4]) # screen width dimension in pixel

			# left eye parameters
			_line = _lines[4].split()

			self.left_screen_transform = avango.osg.make_trans_mat(float(_line[5]), float(_line[6]), float(_line[7]))
			self.left_width_offset	= int(_line[1]) # screen width offset in pixel
			self.left_height_offset = int(_line[2]) # screen width offset in pixel
			self.left_width_dim	= int(_line[3]) # screen width dimension in pixel
			self.left_height_dim 	= int(_line[4]) # screen width dimension in pixel
			
			_file.close()

		except IOError:
			print "error while loading screen config file"
			sys.exit(1)
		
		else:

			# right eye camera setup
			self.right_window = avango.osg.viewer.nodes.GraphicsWindow()
			self.right_window.ScreenIdentifier.value = self.screen_id
			self.right_window.ShowCursor.value = False
			self.right_window.Decoration.value = False
			self.right_window.AutoHeight.value = False
			self.right_window.RealScreenWidth.value = self.physical_screen_width
			self.right_window.RealScreenHeight.value = self.physical_screen_height		
			self.right_window.WantedPositionX.value = self.right_width_offset
			self.right_window.WantedPositionY.value = self.right_height_offset
			self.right_window.WantedWidth.value = self.right_width_dim # in pixel
			self.right_window.WantedHeight.value = self.right_height_dim

			self.right_camera1 = avango.osg.viewer.nodes.Camera(Window = self.right_window)
			self.right_camera1.EyeOffset.value = self.eye_offset1 * 0.5
			self.right_camera1.Far.value = self.far
			self.right_camera1.ScreenTransform.value = self.right_screen_transform
			self.right_camera1.BackgroundColor.value = gl_background_color
			self.right_camera1.Viewport.value = avango.osg.Vec4(0.0,0.0,0.5,1.0)
			self.right_camera1.ViewerTransform.connect_from(SCENE.Player0.camera_absolute.AbsoluteMatrix) # init field connection


			self.right_camera2 = avango.osg.viewer.nodes.Camera(Window = self.right_window)
			self.right_camera2.EyeOffset.value = self.eye_offset2 * 0.5
			self.right_camera2.Far.value = self.far
			self.right_camera2.ScreenTransform.value = self.right_screen_transform
			self.right_camera2.BackgroundColor.value = gl_background_color	
			self.right_camera2.Viewport.value = avango.osg.Vec4(0.5,0.0,0.5,1.0)
			self.right_camera2.ViewerTransform.connect_from(SCENE.Player1.camera_absolute.AbsoluteMatrix) # init field connection
		
			# left eye camera setup
			self.left_window = avango.osg.viewer.nodes.GraphicsWindow()
			self.left_window.ScreenIdentifier.value = self.screen_id
			self.left_window.ShowCursor.value = False
			self.left_window.Decoration.value = False
			self.left_window.AutoHeight.value = False
			self.left_window.RealScreenWidth.value = self.physical_screen_width
			self.left_window.RealScreenHeight.value = self.physical_screen_height		
			self.left_window.WantedPositionX.value = self.left_width_offset
			self.left_window.WantedPositionY.value = self.left_height_offset
			self.left_window.WantedWidth.value = self.left_width_dim # in pixel
			self.left_window.WantedHeight.value = self.left_height_dim

			self.left_camera1 = avango.osg.viewer.nodes.Camera(Window = self.left_window)
			self.left_camera1.EyeOffset.value = self.eye_offset1 * -0.5
			self.left_camera1.Far.value = self.far
			self.left_camera1.ScreenTransform.value = self.left_screen_transform
			self.left_camera1.BackgroundColor.value = gl_background_color
			self.left_camera1.ViewerTransform.connect_from(SCENE.Player0.camera_absolute.AbsoluteMatrix) # init field connection
			self.left_camera1.Viewport.value = avango.osg.Vec4(0.0,0.0,0.5,1.0)

			self.left_camera2 = avango.osg.viewer.nodes.Camera(Window = self.left_window)
			self.left_camera2.EyeOffset.value = self.eye_offset2 * -0.5
			self.left_camera2.Far.value = self.far
			self.left_camera2.ScreenTransform.value = self.left_screen_transform
			self.left_camera2.BackgroundColor.value = gl_background_color
			self.left_camera2.ViewerTransform.connect_from(SCENE.Player1.camera_absolute.AbsoluteMatrix) # init field connection
			self.left_camera2.Viewport.value = avango.osg.Vec4(0.5,0.0,0.5,1.0)

		
		

			if gl_headtracking_flag == True:
				self.tracking_sensor1 = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head1", TransmitterOffset = avango.osg.make_trans_mat(0.75,-1.42,2.0)) # init tracking sensor
				self.right_camera1.EyeTransform.connect_from(self.tracking_sensor1.Matrix)
				self.left_camera1.EyeTransform.connect_from(self.tracking_sensor1.Matrix)
			
				self.tracking_sensor2 = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService(), Station = "tracking-head2", TransmitterOffset = avango.osg.make_trans_mat(-0.75,-1.42,2.0)) # init tracking sensor
				self.right_camera2.EyeTransform.connect_from(self.tracking_sensor2.Matrix)
				self.left_camera2.EyeTransform.connect_from(self.tracking_sensor2.Matrix)

			else:
				self.right_camera1.EyeTransform.value = gl_eye_transform # fixed head position
				self.left_camera1.EyeTransform.value = gl_eye_transform # fixed head position
				self.right_camera2.EyeTransform.value = gl_eye_transform # fixed head position
				self.left_camera2.EyeTransform.value = gl_eye_transform # fixed head position

			# init viewer
			self.viewer = avango.osg.viewer.nodes.Viewer(Scene = SCENE.root, MasterCamera = self.right_camera1, SlaveCameras = [self.left_camera1, self.right_camera2, self.left_camera2])

			# init simple mouse events
			self.events = avango.osg.viewer.nodes.EventFields(View = self.viewer)

			self.right_window.DragEvent.connect_from(self.events.DragEvent)
			self.right_window.MoveEvent.connect_from(self.events.MoveEvent)


			#self.init_ground_plane(SCENE)

	# functions
	def init_ground_plane(self, SCENE):
		if gl_ground_flag == True:
			self.ground_panel = avango.osg.nodes.Panel(PanelColor = avango.osg.Vec4(0.5,0.5,0.3,0.75), Width = 1.0, Height = 1.0)
			self.ground_geode = avango.osg.nodes.LayerGeode(Drawables = [self.ground_panel], StateSet = avango.osg.nodes.StateSet(BlendMode = 1, LightingMode = 0, RenderingHint = 2))
			self.ground_transform = avango.osg.nodes.MatrixTransform(Children = [self.ground_geode])
			self.ground_transform.Matrix.value = gl_ground_plane_transform
			SCENE.root.Children.value.append(self.ground_transform)
