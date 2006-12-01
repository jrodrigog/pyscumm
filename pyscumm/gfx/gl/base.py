from types import NoneType
from OpenGL.GL import *
import pygame
from pyscumm.driver import Display as AbstractDisplay
from pyscumm.gfx import Drawable


class Object( Drawable ):
    """Abstract GL Object; contains the location, insertion,
    rotation and color of the object"""

    def __init__( self ):
        Drawable.__init__( self )

    def clone( self, obj=None, deep=False ):
        """Clone the object"""
        if isinstance( obj, NoneType ): obj = Object()
        Drawable.clone( self, obj, deep )
        return obj

    def draw( self ):
        """Draw the abstract object, position and colorize it"""
        glTranslatef( *self.copy.location )
        glRotatef( *self.copy.rotation )
        glScalef( *self.copy.scale )
        glTranslatef( *self.copy.insertion )
        glColor4f( *self.copy.color )
        for child in self.child: child.draw()

    @classmethod
    def deserialize( cls, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Object()
        return Drawable.deserialize( element, obj )


class Display( AbstractDisplay ):
    """OpenGL Display class."""
    def __init__( self ):
        """Build a GLDisplay object"""
        AbstractDisplay.__init__( self )
        self.open_flags |= pygame.OPENGL

    def open( self ):
        AbstractDisplay.open( self )
        self.reshape()

    def flip( self ):
        AbstractDisplay.flip( self )
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    def reshape( self ):
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        #glViewport( 0, self.size[0], self.size[1], self.size[0] )
        glViewport( 0, 0, self.size[0], self.size[1] )
        glOrtho( 0, self.size[0], 0, self.size[1], -50, 50 )
        glMatrixMode( GL_MODELVIEW )
        glClearColor( 0., 0., 0., 1.0 )
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glLoadIdentity()
        glDisable( GL_LIGHTING )
        #glEnable( GL_DEPTH_TEST )
        #glEnable( GL_TEXTURE_2D )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
        glAlphaFunc( GL_GREATER, 0.01 )

        glEnable( GL_LINE_SMOOTH )
        #glEnable( GL_POINT_SMOOTH )
        glEnable( GL_BLEND )
        #glEnable( GL_ALPHA_TEST )

    def set_icon( self, file, colorkey ):
        image = pygame.image.load( file )
        colorkey = image.get_at( colorkey )
        image.set_colorkey( colorkey, pygame.RLEACCEL )
        self._icon = image
        if not self._opened: return
        pygame.display.set_icon( image )

    def set_size( self, size ):
        AbstractDisplay.set_size( self, size )
        if not self._opened: return
        self.reshape()

    def get_size(self):
        return self._size

    size = property( get_size, set_size )



