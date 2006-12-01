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
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 20/11/2006
"""

from types import NoneType
from OpenGL.GL import *
import pygame
from pyscumm.driver import Display as AbstractDisplay
from pyscumm.driver import Mouse as AbstractMouse
from pyscumm.gfx import Drawable
from pyscumm.vector import Vector3D

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

class Mouse( AbstractMouse ):
    """A GL Mouse, taking care of the axis conversions."""
    def __init__( self, display=None ):
        AbstractMouse.__init__( self, display )

    def get_location( self ):
        return self._location

    def set_location( self, location ):
        """
        Set the location of the mouse cursor.
        @param location: Mouse cursor location
        @type location: Vector3D
        """
        self._location = location
        pygame.mouse.set_pos(
            [ round( int( location[0] ) ), round( int( self.display.size[1] + location[1] ) ) ] )

    def update( self ):
        """
        Updates the mouse location for this frame
        based on the display.
        """
        AbstractMouse.update( self )
        self._location[1] = self.display.size[1] - self._location[1]

    location = property( get_location, set_location )

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



