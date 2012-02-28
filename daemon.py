#!/usr/bin/python
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


import avango.daemon
import os


# import modules from local library
from lib.globals import *

# functions
def init_pst_tracking():

	# create instance of DTrack
	_pst = avango.daemon.DTrack()
	_pst.port = "5002" # PST port
	
	# head tracking
	_pst.stations[6] = avango.daemon.Station('tracking-head0')
	_pst.stations[6] = avango.daemon.Station('tracking-head1')
	
	device_list.append(_pst)
	print "PST Tracking started!"
	
def init_art_tracking():

	# create instance of DTrack
	_dtrack = avango.daemon.DTrack()
	_dtrack.port = "5000" # ART port at LCD wall
	
	# head tracking
	_dtrack.stations[20] = avango.daemon.Station('tracking-head1') # passive glasses
	_dtrack.stations[19] = avango.daemon.Station('tracking-head2') # passive glasses
	
	device_list.append(_dtrack)
	print "ART Tracking started at LCD WALL"




def init_impact_controller():

	_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Mega World USB Game Controllers\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Mega World USB Game Controllers\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
    
	if len(_string) > 0:	
		_string = _string.split()[0]
	
		_controller = avango.daemon.HIDInput()
		_controller.station = avango.daemon.Station('device-impactcontroller') # create a station to propagate the input events
		_controller.device = _string

		# map incoming spacemouse events to station values
		_controller.values[0] = "EV_ABS::REL_X"   # trans X
		_controller.values[1] = "EV_ABS::REL_Y"   # trans Y
		_controller.values[2] = "EV_ABS::REL_Z"   # rotate X
		_controller.values[3] = "EV_ABS::REL_RZ"  # rotate Y
		
		# buttons
		_controller.buttons[0] = "EV_KEY::BTN_BASE6" # start button
		_controller.buttons[1] = "EV_KEY::BTN_TRIGGER" # button 1
		_controller.buttons[2] = "EV_KEY::BTN_THUMB" # button 2 
		_controller.buttons[3] = "EV_KEY::BTN_THUMB2" # button 3
		_controller.buttons[4] = "EV_KEY::BTN_TOP" # button 4
		_controller.buttons[5] = "EV_KEY::BTN_TOP2" # button 5
		_controller.buttons[6] = "EV_KEY::BTN_PINKIE" # button 6
		_controller.buttons[7] = "EV_KEY::BTN_BASE" # button LX
		_controller.buttons[8] = "EV_KEY::BTN_BASE5" # button S    
		
				# =========================================
		# For codes, run 
		# /opt/avango/vr_application_lib/tools/ev_read /dev/input/event5
		# -----------------------------------------
		# For button mappings, see 
		# /opt/svn/avango/current/avango-daemon/src/avango/daemon
		# =========================================
		
		# =========================================
		# INPUT 			| TYPE CODE VALUE
		# -----------------------------------------
		# start-button		| 1 299 1 = 0x12b | BTN_BASE6
		# -----------------------------------------
		# button 1 press	| 1 288 1 = 0x120 | BTN_TRIGGER
		# button 2 press	| 1 289 1 = 0x121 | BTN_THUMB
		# button 3 press	| 1 290 1 = 0x122 | BTN_THUMB2
		# button 4 press	| 1 291 1 = 0x123 | BTN_TOP
		# button 5 press	| 1 292 1 = 0x124 | BTN_TOP2
		# button 6 press	| 1 293 1 = 0x125 | BTN_PINKIE
		# -----------------------------------------
		# button LX			| 1 294 1 = 0x126 | BTN_BASE
		# button RX			| 1 294 1 = 0x126 | BTN_BASE2
		# button S			| 1 295 1 = 0x127 | BTN_BASE5
		# -----------------------------------------
		# d-pad up			| 3 17 -1	| ABS_HAT0Y
		# d-pad down		| 3 17 1	| ABS_HAT0Y
		# d-pad left		| 3 16 -1	| ABS_HAT0X
		# d-pad right		| 3 16 1	| ABS_HAT0X
		# -----------------------------------------
		# joystick 1 up		| 3 1 -128		| REL_Y
		# joystick 1 down	| 3 1 127	| REL_Y
		# joystick 1 left	| 3 0 -128		| REL_X
		# joystick 1 right	| 3 0 127	| REL_X
		# -----------------------------------------
		# joystick 2 up		| 3 2 -128		| REL_Z
		# joystick 2 down	| 3 2 127	| REL_Z
		# joystick 2 left	| 3 5 -128		| REL_RZ
		# joystick 2 right	| 3 5 127	| REL_RZ
		# =========================================

		device_list.append(_controller)
		print "Impact Controller started at:", _string

	else:
		print "Impact Controller NOT found !"

def init_saitek_controller():

	_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Saitek P880\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"SAITEK P880\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
    
	if len(_string) > 0:	
		_string = _string.split()[0]
	
		_controller = avango.daemon.HIDInput()
		_controller.station = avango.daemon.Station('device-saitekcontroller') # create a station to propagate the input events
		_controller.device = _string

		# map incoming spacemouse events to station values
		_controller.values[0] = "EV_ABS::REL_X"   # trans X
		_controller.values[1] = "EV_ABS::REL_Y"   # trans Y
		_controller.values[2] = "EV_ABS::REL_Z"   # rotate X
		_controller.values[3] = "EV_ABS::REL_RZ"  # rotate Y
		
		# buttons
		_controller.buttons[0] = "EV_KEY::BTN_BASE6" # start button
		_controller.buttons[1] = "EV_KEY::BTN_TRIGGER" # button 1
		_controller.buttons[2] = "EV_KEY::BTN_THUMB" # button 2 
		_controller.buttons[3] = "EV_KEY::BTN_THUMB2" # button 3
		_controller.buttons[4] = "EV_KEY::BTN_TOP" # button 4
		_controller.buttons[5] = "EV_KEY::BTN_TOP2" # button 5
		_controller.buttons[6] = "EV_KEY::BTN_PINKIE" # button 6
		_controller.buttons[7] = "EV_KEY::BTN_BASE" # button LX
		_controller.buttons[8] = "EV_KEY::BTN_BASE5" # button S    
		
				# =========================================
		# For codes, run 
		# /opt/avango/vr_application_lib/tools/ev_read /dev/input/event5
		# -----------------------------------------
		# For button mappings, see 
		# /opt/svn/avango/current/avango-daemon/src/avango/daemon
		# =========================================
		
		# =========================================
		# INPUT 			| TYPE CODE VALUE
		# -----------------------------------------
		# start-button		| 1 299 1 = 0x12b | BTN_BASE6
		# -----------------------------------------
		# button 1 press	| 1 288 1 = 0x120 | BTN_TRIGGER
		# button 2 press	| 1 289 1 = 0x121 | BTN_THUMB
		# button 3 press	| 1 290 1 = 0x122 | BTN_THUMB2
		# button 4 press	| 1 291 1 = 0x123 | BTN_TOP
		# button 5 press	| 1 292 1 = 0x124 | BTN_TOP2
		# button 6 press	| 1 293 1 = 0x125 | BTN_PINKIE
		# -----------------------------------------
		# button LX			| 1 294 1 = 0x126 | BTN_BASE
		# button RX			| 1 294 1 = 0x126 | BTN_BASE2
		# button S			| 1 295 1 = 0x127 | BTN_BASE5
		# -----------------------------------------
		# d-pad up			| 3 17 -1	| ABS_HAT0Y
		# d-pad down		| 3 17 1	| ABS_HAT0Y
		# d-pad left		| 3 16 -1	| ABS_HAT0X
		# d-pad right		| 3 16 1	| ABS_HAT0X
		# -----------------------------------------
		# joystick 1 up		| 3 1 -128		| REL_Y
		# joystick 1 down	| 3 1 127	| REL_Y
		# joystick 1 left	| 3 0 -128		| REL_X
		# joystick 1 right	| 3 0 127	| REL_X
		# -----------------------------------------
		# joystick 2 up		| 3 2 -128		| REL_Z
		# joystick 2 down	| 3 2 127	| REL_Z
		# joystick 2 left	| 3 5 -128		| REL_RZ
		# joystick 2 right	| 3 5 127	| REL_RZ
		# =========================================

		device_list.append(_controller)
		print "Saitek Controller started at:", _string

	else:
		print "Saitek Controller NOT found !"


def init_keyboard():

	_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"HID 046a:0011\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Cherry GmbH\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Logitech Logitech USB Keyboard\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) > 0:

		_string = _string.split()[0]

		_keyboard = avango.daemon.HIDInput()
		_keyboard.station = avango.daemon.Station('device-keyboard')
		_keyboard.device = _string

		# map incoming events to station values
		_keyboard.buttons[0] = "EV_KEY::KEY_SPACE"
		_keyboard.buttons[1] = "EV_KEY::KEY_N"
		_keyboard.buttons[2] = "EV_KEY::KEY_C"
		_keyboard.buttons[3] = "EV_KEY::KEY_M"
		_keyboard.buttons[4] = "EV_KEY::KEY_R"
		_keyboard.buttons[5] = "EV_KEY::KEY_G"
		_keyboard.buttons[6] = "EV_KEY::KEY_D"
		_keyboard.buttons[7] = "EV_KEY::KEY_F"
		_keyboard.buttons[8] = "EV_KEY::KEY_LEFT"
		_keyboard.buttons[9] = "EV_KEY::KEY_RIGHT"
		_keyboard.buttons[10] = "EV_KEY::KEY_UP"
		_keyboard.buttons[11] = "EV_KEY::KEY_DOWN"
		
		
		device_list.append(_keyboard)
		print "Keyboard started at:", _string

	else:
		print "Keyboard NOT found !"

def init_spacemouse():

	_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"3Dconnexion SpaceNavigator\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"3Dconnexion SpaceTraveler USB\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()
    
	if len(_string) > 0:	
		_string = _string.split()[0]
	
		_spacemouse = avango.daemon.HIDInput()
		_spacemouse.station = avango.daemon.Station('device-spacemouse') # create a station to propagate the input events
		_spacemouse.device = _string

		# map incoming spacemouse events to station values
		_spacemouse.values[0] = "EV_ABS::ABS_X"   # trans X
		_spacemouse.values[1] = "EV_ABS::ABS_Y"   # trans Y
		_spacemouse.values[2] = "EV_ABS::ABS_Z"   # trans Z
		_spacemouse.values[3] = "EV_ABS::ABS_RX"  # rotate X
		_spacemouse.values[4] = "EV_ABS::ABS_RY"  # rotate Y
		_spacemouse.values[5] = "EV_ABS::ABS_RZ"  # rotate Z

		# buttons
		_spacemouse.buttons[0] = "EV_KEY::BTN_0" # left button
		_spacemouse.buttons[1] = "EV_KEY::BTN_1" # right button

		device_list.append(_spacemouse)
		print "SpaceMouse started at:", _string

	else:
		print "SpaceMouse NOT found !"

def init_mouse():

	_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Logitech USB-PS/2 Optical Mouse\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) == 0:
		_string = os.popen("/opt/avango/vr_application_lib/tools/list-ev -s | grep \"Logitech USB Optical Mouse\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

	if len(_string) > 0:

		_string = _string.split()[0]

		_mouse = avango.daemon.HIDInput()
		_mouse.station = avango.daemon.Station('device-mouse')
		_mouse.device = _string

		# map incoming events to station values
		_mouse.buttons[0] = "EV_KEY::BTN_LEFT"
		_mouse.buttons[1] = "EV_KEY::BTN_RIGHT"

		device_list.append(_mouse)
		print "Mouse started at:", _string

	else:
		print "Mouse NOT found !"


device_list = []

# init respective tracking system
if gl_viewing_setup == "desktop" or gl_viewing_setup == "anaglyph" or gl_viewing_setup == "checkerboard" or gl_viewing_setup == "splitscreen":
	init_pst_tracking()
elif gl_viewing_setup == "lcd" or gl_viewing_setup == "lcd_splitscreen":
	init_art_tracking()
# init input devices
init_spacemouse()
init_keyboard()
init_mouse()
init_impact_controller()
init_saitek_controller()

	
#avango/trunk/avango-daemon/src/avango/daemon/LinuxEvent.cpp

# start daemon (will enter the main loop)
avango.daemon.run(device_list)
