
import pygame.display, pygame.mouse, time
import gfx.vector.Vector2D



class Mouse( object ):
    """Mouse Controller"""

    def __init__( self ):
        self._time_doubleclick = 0.300
        self._distance_drag = 8
        self._visible = True

    def get_position( self ):
        """
        Get the current X,Y position of the mouse cursor.

        @return: the cursor position
        @rtype: Vector2D
        """
        return gfx.vector.Vector2D( pygame.mouse.get_pos )

    def set_position( self, position ):
        """
        Set a new X,Y position of the mouse cursor.

        @param pos: The new position of mouse cursor
        @type pos: Vector2D
        @return: None
        """
        pygame.mouse.set_pos( position )

    def get_time_doubleclick( self ):
        """
        Get the current minimal time needed for wait 2 click and consider him a double click.

        @return: The current time for a doubleclick
        @rtype: Float
        """
        return self._time_doubleclick

    def set_time_doubleclick( self, value ):
        """
        Set the minimal time needed for wait 2 click and consider him a double click.

        @param value: The new minimal time nedeed.
        @type value: Float
        @return: None
        """
        self._time_doubleclick = value

    def get_distance_drag( self ):
        """
        Get the minimal distance in pixels to condisider a gragging with the mouse.

        @return: The distance in pixels
        @rtype: Integer
        """
        return self._distance_drag

    def set_distance_drag( self, value ):
        """
        Set the minimal distance in pixel to consider a dragging with the mouse.

        @param value: The new distance nedeed in pixels
        @type value: Integer
        """
        self._distance_drag = value

    def get_visible( self ):
        """
        Get if the mouse its visible.

        @return: The mouse visible value
        @rtype: Boolean
        """
        return self._visible

    def set_visible( self, value ):
        """
        Set cursor visibility

        @param value: the visibility state
        @type value: Boolean
        @return: None
        """
        self._visible = value

    time_doubleclick    = property( get_time_doubleclick, set_time_doubleclick )
    distance_drag       = property( get_distance_drag, set_distance_drag )
    visible             = property( get_visible, set_visible )


class Display( object ):
    """Display controller"""

    def __init__( self ):
        self._size = None
        self._icon = None
        self.__isopen__ = False

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
        if not self.__isopen__:
            self.__isopen__ = True
            pygame.display.init()
            pygame.display.set_mode( self._size, pygame.DOUBLEBUF | pygame.OPENGL )

    def close( self ):
        """
        Close que display window.

        @return None
        """
        if __isopen__:
            __isopen__ = False
            pygame.display.quit()

    def list_modes( self ):
        """
        Get a list of possible dimensions to the current/best color depth.

        @return: A list of possible dimensions.
        @rtype: List
        """
        return pygame.display.list_modes()

    def toggle_fullscreen( self ):
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
        @rtype: Tuple
        """
        return self._size

    def set_size( self, size ):
        """
        Set a new size to the display.

        @param size: The new size of the display (X,Y).
        @type size: 2-integer tuple
        @return: None
        """
        self._size = size
        if __isopen__:
            pygame.display.set_mode( (self._size[0], self._size[1]), pygame.DOUBLEBUF | pygame.OPENGL )

    def get_title( self ):
        """
        Get the current title of the display.

        @return: The current title of the new display.
        @rtype: String
        """
        return pygame.display.get_caption()

    def set_title( self, title ):
        """
        Set the title of the display.

        @param title: The name title of the display
        @type title: string
        @return: None
        """
        pygame.display.set_caption( title )

    def get_icon( self ):
        """
        Get the current image icon setted.

        @return: a icon image that are current setted on a window
        @rtype: Image
        """
        return self._icon

    def set_icon( self, icon ):
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
        self._icon = icon
        pygame.display.set_icon( icon )

    size        = property( get_size, set_size )
    icon        = property( get_icon, set_icon )


class Clock( object ):
    sec_to_msec = 1000.

    def __init__( self ):
        # Next frame tick time
        self._next_time = 0
        # Interval between frame ticks */
        self._tick_interval = 0
        # Frame count
        self._frame_count = 0
        # Frame rate limit
        self._limit = 60

    def set_limit( self, fps ):
        # Set the frame rate limit
        self._limit = fps
        self._tick_interval = self.sec_to_msec / self._limit
        self._tick_interval *= 2 # double speed

    def get_limit( self ):
        # Get the frame rate limit
        return self._limit

    def tick( self ):
        # Tick a frame and wait till next frame */
        self._frame_count += 1
        time.sleep( self._get_raw_time() / self.sec_to_msec )

    def _get_raw_time( self ):
        # Get the raw time, time pending untill the next frame
        now = pygame.time.get_ticks()
        if self._next_time <= now:
            self._next_time = now + self._tick_interval
            return 0
        return self._next_time - now

    def get_time( self ):
        # Get the next frame time
        return self._next_time

    def get_fps( self ):
        # Get the frames per second
        return self._frame_count / ( pygame.time.get_ticks() / self.sec_to_msec );

    fps        = property( get_fps )
    time    = property( get_time )
    limit    = property( get_limit, set_limit )
