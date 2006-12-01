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
from pyscumm.vector import ProxyVector2D
from pyscumm.gfx.gl import Object, Texture, Box
from pyscumm.constant import SIZE_UPDATED, UPDATED

SELF_UPDATED = \
      SIZE_UPDATED \
    | UPDATED

class Image( Object ):
    """A Image encapsulates a Texture and
    texturizes it in a quad"""
    def __init__( self, texture = None, size = None ):
        Object.__init__( self )
        self._texture = None
        self._base = None
        self.collider = Box()
        self.collider.copy = self
        self._tc = [
            ProxyVector2D( [ 0.0, 0.0 ], self, UPDATED ),
            ProxyVector2D( [ 1.0, 0.0 ], self, UPDATED ),
            ProxyVector2D( [ 1.0, 1.0 ], self, UPDATED ),
            ProxyVector2D( [ 0.0, 1.0 ], self, UPDATED ) ]

        if not isinstance( size, NoneType ):
            self.size = size
        if not isinstance( texture, NoneType ):
            self.texture = texture

    def __del__( self ):
        if not isinstance( self._base, NoneType ):
            glDeleteLists( self._base, 1 )

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Image()
        Object.clone( self, obj, deep )
        if self._texture:
            obj.texture = self._texture.clone( deep )
        return obj

    def get_texture( self ): return self._texture
    def set_texture( self, texture ):
        self._texture = texture
        if not isinstance( texture, NoneType ) and self.size.is_cero():
            self.size = texture.size.clone()

    def update( self ):
        if self.collider: self.collider.update()
        if self.copy.frozen \
        or not ( self.copy.updated & SELF_UPDATED ): return
        Object.update( self )
        print "pyscumm.gfx.gl.Image.update()"
        if not isinstance( self._base, NoneType ):
            glDeleteLists( self._base, 1 )
        self._base = glGenLists( 1 )
        glNewList( self._base, GL_COMPILE )
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, self._texture.id )
        glBegin( GL_QUADS )
        glTexCoord2f( *self._tc[0] ); glVertex2f( 0.          , 0.           )
        glTexCoord2f( *self._tc[1] ); glVertex2f( self.size[0], 0.           )
        glTexCoord2f( *self._tc[2] ); glVertex2f( self.size[0], self.size[1] )
        glTexCoord2f( *self._tc[3] ); glVertex2f( 0.          , self.size[1] )
        glEnd()
        glDisable( GL_TEXTURE_2D )
        glEndList()

    def draw( self ):
        """Texturize the Image in a quad"""
        self.collider.draw()
        if not self.copy.visible: return
        glPushMatrix()
        Object.draw( self )
        glCallList( self._base )
        glPopMatrix()

    @classmethod
    def deserialize( cls, element, obj = None ):
        """Deserialize from XML"""
        if obj == None: obj = Image()
        Object.deserialize( element, obj )
        obj.texture = Texture.deserialize(
            element.getElementsByTagName("Texture").item( 0 ) )
        obj.size = obj.texture.size
        return obj

    texture = property( get_texture, set_texture )

