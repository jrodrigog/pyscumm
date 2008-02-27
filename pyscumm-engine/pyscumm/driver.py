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

"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@since: 18/02/2007
"""

from euclid import Vector2
from base import debugger
from sdl import Drawable
import pygame.mouse, time



class Cursor(Drawable):

    def __init__(self):
        Drawable.__init__(self)
        self.offset = Vector2(0, 0)

    def draw(self):
        pygame.display.get_surface().blit(self._image, self.screen_position - self.offset)



class DefaultCursor(Cursor):
    def __init__(self):
        Cursor.__init__(self)
        self.image = pygame.image.load('pyscumm/artwork/cursor.png')



class Mouse( object ):
    """A Mouse Controller Class."""

    def __init__( self, display=None ):
        """Build a Mouse object"""
        self.doubleclick_time = 200
        self.drag_time = 150
        self.cursor = None

    def get_position( self ):
        """
        Get the current location of the mouse cursor.
        @return: Mouse cursor location
        @rtype: list
        """
        return Vector2(*pygame.mouse.get_pos())

    def set_position( self, pos ):
        """
        Set the location of the mouse cursor.
        @param location: Mouse cursor location
        @type location: list
        """
        pygame.mouse.set_pos( pos )

    def update( self ):
        """
        Updates the mouse location for this frame
        based on the display.
        """
        if self.cursor:
            self.cursor.screen_position = self.get_position()

    def draw(self):
        if not self.cursor:
            self.cursor = DefaultCursor()
        self.cursor.draw()

    position = property(get_position, set_position)



class Display( object ):
    """pyscumm Display object"""

    def __init__(self):
        """Build a Display object"""
        self._title = "pyscumm display"
        self._size = Vector2(640, 480)
        self._icon = None
        self._opened = False

    def open(self):
        """
        Open the display window with the setted size.
        @return: None
        """
        self._opened = True
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.init()
        self._set_title(self._title)
        self._set_size(self._size)
        debugger.info("display openned")

    def close(self):
        """
        Close que display window.
        @return None
        """
        if not self._opened:
            return
        pygame.display.quit()
        debugger.info("display closed")


    def get_modes(self):
        """
        Get a list of possible dimensions to the current/best color depth.
        @return: A list of possible dimensions.
        @rtype: List
        """
        return pygame.display.list_modes()

    def toggle_fullscreen(self):
        """
        Swith between fullscreen or windowed mode.
        @return: if available and successfull, will return True, else return False.
        @rtype: Boolean
        """
        pygame.display.toggle_fullscreen()
        debugger.info("toggling fullscreen mode")

    def _get_size(self):
        """
        Get current display size.
        @return: The current display size.
        @rtype: pygame.base.Vector3D
        """
        return self._size

    def _set_size(self, size):
        """
        Set a new display size.
        @param size: The new size of the display (X,Y,*).
        @type size: pygame.base.Vector3D
        @return: None
        """
        self._size = size
        if not self._opened: return
        screen = pygame.display.set_mode(self._size, pygame.HWSURFACE)
        screen.set_clip(pygame.Rect((0, 0), self._size))
        debugger.info("display size setted [%s]" % (str(self._size)))

    def _get_title(self):
        """
        Get the current display title.
        @return: The current title of the new display.
        @rtype: String
        """
        return self._title

    def _set_title(self, title):
        """
        Set the display title.
        @param title: The name title of the display
        @type title: string
        @return: None
        """
        self._title = title
        pygame.display.set_caption(title)

    def _get_icon(self):
        """
        Get the current image icon setted.
        @return: a icon image that are current setted on a window
        @rtype: pygame.Surface
        """
        return self._icon

    def _set_icon(self, image):
        """
        Set the display icon.
        Some window managers on X11 don't allow you to change the icon
        after the window has been shown the first time.
        @param image: A icon image
        @type image: pygame.Surface
        @return: None
        """
        self._icon = image
        if not self._opened: return
        pygame.display.set_icon(image)

    def flip(self):
        """
        Update the screen
        """
        pygame.display.flip()

    size = property(_get_size, _set_size)
    title = property(_get_title, _set_title)
    icon = property(_get_icon, _set_icon)



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
        self.tick_interval = round( MSEC / self._limit )
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
