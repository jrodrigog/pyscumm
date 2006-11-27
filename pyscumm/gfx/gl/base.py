import types
import OpenGL.GL
import pygame.display
import pyscumm.driver
from pyscumm.gfx import Drawable


class Object( Drawable ):
    """Abstract GL Object; contains the location, insertion,
    rotation and color of the object"""

    def __init__( self ):
        Drawable.__init__( self )

    def clone( self, obj=None, deep=False ):
        """Clone the object"""
        if isinstance( obj, types.NoneType ): obj = Object()
        Drawable.clone( self, obj, deep )
        return obj

    def draw( self ):
        """Draw the abstract object, position and colorize it"""
        OpenGL.GL.glTranslatef( *self._copy.location )
        OpenGL.GL.glRotatef( *self._copy.rotation )
        OpenGL.GL.glScalef( *self._copy.scale )
        OpenGL.GL.glTranslatef( *self._copy.insertion )
        OpenGL.GL.glColor4f( *self._copy.color )
        for child in self.child: child.draw()

    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Object()
        return Drawable.deserialize( element, obj )

    deserialize = classmethod( deserialize )


class Display( pyscumm.driver.Display ):
    """OpenGL Display class."""
    def __init__( self ):
        """Build a GLDisplay object"""
        pyscumm.driver.Display.__init__( self )
        self._open_flags |= pygame.OPENGL

    def open( self ):
        pyscumm.driver.Display.open( self )
        self.reshape()

    def flip( self ):
        pyscumm.driver.Display.flip( self )
        OpenGL.GL.glClear( OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT )

    def reshape( self ):
        OpenGL.GL.glMatrixMode( OpenGL.GL.GL_PROJECTION )
        OpenGL.GL.glLoadIdentity()
        #OpenGL.GL.glViewport( 0, self._size[0], self._size[1], self._size[0] )
        OpenGL.GL.glViewport( 0, 0, self._size[0], self._size[1] )
        OpenGL.GL.glOrtho( 0, self._size[0], 0, self._size[1], -50, 50 )
        OpenGL.GL.glMatrixMode( OpenGL.GL.GL_MODELVIEW )
        OpenGL.GL.glClearColor( 0., 0., 0., 1.0 )
        OpenGL.GL.glClear( OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT )
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glDisable( OpenGL.GL.GL_LIGHTING )
        #glEnable( GL_DEPTH_TEST )
        #OpenGL.GL.glEnable( OpenGL.GL.GL_TEXTURE_2D )
        OpenGL.GL.glBlendFunc( OpenGL.GL.GL_SRC_ALPHA, OpenGL.GL.GL_ONE_MINUS_SRC_ALPHA )
        OpenGL.GL.glAlphaFunc( OpenGL.GL.GL_GREATER, 0.01 )

        OpenGL.GL.glEnable( OpenGL.GL.GL_LINE_SMOOTH )
        #OpenGL.GL.glEnable( OpenGL.GL.GL_POINT_SMOOTH )
        OpenGL.GL.glEnable( OpenGL.GL.GL_BLEND )
        #OpenGL.GL.glEnable( OpenGL.GL.GL_ALPHA_TEST )

    def set_icon( self, file, colorkey ):
        self._icon = file
        image = pygame.image.load(file)
        colorkey = image.get_at(colorkey)
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        if self._opened: pygame.display.set_icon( image )

    def set_size(self, size ):
        pyscumm.driver.Display.set_size( self, size )
        self.reshape()


    def get_size(self):
        return pyscumm.driver.Display.get_size(self)

    size = property( get_size, set_size )



