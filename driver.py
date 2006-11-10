
import pygame, time



class Mouse( object ):
    """Mouse Controller"""

    _instance = None
    
    def __init__( self ):
        pos = None
        time_click = 0.100
        time_doubleclick = 0.300
        distance_drag = 8
        self._visible = True
    
    def set_visible( self, visible ):
        self._visible = visible
        pygame.mouse.set_visible ( self._visible )
        
    def get_visible( self ):
        return self._visible
        
    def instance( self ):
        """Singleton pattern"""
        if not self._instance:
            self._instance = self()
        return self._instance

    instance    = classmethod( instance )
    visible     = property( get_visible, set_visible )



class Display( object ):
    """Display controller"""

    _instance = None
    
    def __init__( self ):
        self._size = None
        self._title = None
        self._fps = None

    def get_info( self ):
        return pygame.display.Info()

    def get_driver( self ):
        return pygame.display.get_driver()

    def open( self, size, framerate, iconfile=None ):
    	if not iconfile:
            iconfile = Picture.Picture( os.path.join(os.path.abspath(''),'PySCUMM/scummart/pyscumm_ico.png') )
    	pygame.display.set_icon( iconfile.surface )
    	self._size = size
    	self.set_title( 'PySCUMM Engine Display' )
    	pygame.display.set_mode( size, pygame.DOUBLEBUF | pygame.OPENGL )

    def list_modes( self ):
        return pygame.display.list_modes()

    def toggle_fullscreen( self ):
        return pygame.display.toggle_fullscreen()

    def get_fps( self ):
        return self._fps
            
    def set_fps( self, fps ):
        self._fps = fps
        
    def get_size( self ):
        return self._size

    def set_size( self, size ):
        self._size = size
        pygame.display.set_mode( (self._size[0], self._size[1]), pygame.DOUBLEBUF | pygame.OPENGL )

    def get_title( self ):
        return self._title

    def set_title( self, title ):
        self._title = title
        pygame.display.set_caption( self._title )
        
    def instance( self ):
        """Singleton pattern"""
        if not self._instance:
            self._instance = self()
        return self._instance

    instance    = classmethod( instance )
    title           = property( get_title, set_title )
    size            = property( get_size, set_size )



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

	# Get the frame rate limit
	def get_limit( self ): return self._limit
	
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
		
	fps = property( get_fps )
	time = property( get_time )
	limit = property( get_limit, set_limit )
