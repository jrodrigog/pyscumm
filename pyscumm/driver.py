#    PySCUMM Engine. SCUMM based engine for Python
#    Copyright (C) 2006  PySCUMM Engine. http://pyscumm.org
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

#!/usr/bin/env python

"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 14/11/2006
"""

import time
import pygame.mouse
from vector import Vector3D
import vm

class Mouse( object ):
    """A Mouse Controller Class."""

    def __init__( self ):
        """Build a Mouse object"""
        self.double_click_time = 200
        self.drag_distance = 0
        self.visible = True

    def get_location( self ):
        """
        Get the current location of the mouse cursor.
        @return: Mouse cursor location
        @rtype: Vector3D
        """
        pos = pygame.mouse.get_pos()
        return Vector3D(
            [ float( pos[0] ), vm.VM().display.size[1] - float( pos[1] ), 0. ] )

    def set_location( self, pos ):
        """
        Set the location of the mouse cursor.
        @param pos: Mouse cursor location
        @type pos: Vector3D
        """
        pygame.mouse.set_pos( location[:2] )

    location = property( get_location, set_location )


class Display( object ):
    """A Display Controller class."""

    def __init__( self ):
        """Build a Display object"""
        self._size = Vector3D( [ 640, 480, 0 ] )
        self.open_flags = pygame.DOUBLEBUF
        self._icon = None
        self._opened = False
        self._title = "pyscumm window"

    def info( self ):
        """
        Get some info of the video system.
        @return: driver, info, window manager
        @rtype: String, Dict, String
        """
        return str( pygame.display.get_driver() ), pygame.display.Info(), str( pygame.display.get_wm_info() )

    def open( self ):
        """
        Open the display window with the size setted.
        @return: None
        """
        self._opened = True
        pygame.init()
        pygame.display.init()
        self._title = self._title
        self.size = self.size

    def close( self ):
        """
        Close que display window.
        @return None
        """
        if not self._opened: return
        pygame.display.quit()

    def get_modes( self ):
        """
        Get a list of possible dimensions to the current/best color depth.
        @return: A list of possible dimensions.
        @rtype: List
        """
        return pygame.display.list_modes()

    def toggle_full_screen( self ):
        """
        Switch between windowed and fullscreen mode.
        @return: if available and successfull, will return True, else return False.
        @rtype: Boolean
        """
        return pygame.display.toggle_fullscreen()

    def get_size( self ):
        """
        Get the current size of the display.
        @return: The current display size.
        @rtype: pygame.vector.Vector3D
        """
        return self._size

    def set_size( self, size ):
        """
        Set a new size to the display.
        @param size: The new size of the display (X,Y,*).
        @type size: pygame.vector.Vector3D
        @return: None
        """
        self._size = size
        if not self._opened: return
        pygame.display.set_mode( self._size[:2], self.open_flags )

    def get_title( self ):
        """
        Get the current title of the display.
        @return: The current title of the new display.
        @rtype: String
        """
        return self._title

    def set_title( self, title ):
        """
        Set the title of the display.
        @param title: The name title of the display
        @type title: string
        @return: None
        """
        self._title = title
        if self._opened: pygame.display.set_caption( self._title )

    def get_icon( self ):
        """
        Get the current image icon setted.
        @return: a icon image that are current setted on a window
        @rtype: Image
        """
        return self._icon

    def set_icon( self, file ):
        """
        Sets the runtime icon that your system uses to decorate the program window.
        It is also used when the application is iconified and in the window frame.
        You likely want this to be a smaller image, a size that your system
        window manager will be able to deal with.
        Some window managers on X11 don't allow you to change the icon
        after the window has been shown the first time.
        @param image: A icon image
        @type image: Image
        @return: None
        """
        self._icon = file
        if not self._opened: return
        pygame.display.set_icon( icon )

    def flip( self ):
        pygame.display.flip()

    modes  = property( get_modes )
    title  = property( get_title, set_title )
    size   = property( get_size, set_size )
    icon   = property( get_icon, set_icon )


MSEC = 1000.

class Clock( object ):

    def __init__( self ):
        """Build a Clock object."""
        # Next frame tick time
        self.time = 0
        # Interval between frame ticks
        self.tick_interval = 0
        # Frame count
        self.frame_count = 0
        # Frame rate limit
        self.limit = 60

    def set_limit( self, fps ):
        """
        Set the frame rate limit.
        @param fps: Maximum fps
        @type fps: float
        """
        self._limit = fps
        self.tick_interval = MSEC / self._limit
        self.tick_interval *= 2. # double speed

    def get_limit( self ):
        """
        Get the frame rate limit
        @return: float
        """
        return self._limit

    def tick( self ):
        """
        Tick a frame and wait till next frame
        if we are drawing too fast.
        @return: None
        """
        self.frame_count += 1
        time.sleep( self._get_raw_time() / MSEC )

    def _get_raw_time( self ):
        """
        Get the raw time, time pending untill the next frame.
        @return: float
        """
        now = pygame.time.get_ticks()
        if self.time <= now:
            self.time = now + self.tick_interval
            return 0.
        return self.time - now

    def get_fps( self ):
        """
        Get the frames per second.
        @return: float
        """
        return self.frame_count / ( pygame.time.get_ticks() / MSEC );

    fps      = property( get_fps )
    limit    = property( get_limit, set_limit )
