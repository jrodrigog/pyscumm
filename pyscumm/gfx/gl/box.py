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

from OpenGL.GL import *
from types import NoneType
from pyscumm.gfx.gl import Object
from pyscumm.box import Box as AbstractBox
from pyscumm.vector import Vector3D, Vector4D
import pyscumm.constant
from pyscumm.constant import SIZE_UPDATED
from pyscumm.box import BOX_UPDATED

BORDER_LIGHT = 1.5
BORDER_SIZE = 1.
POINT_SIZE = 5.

SELF_UPDATED = \
      pyscumm.constant.COPY_UPDATED \
    | pyscumm.constant.COLOR_UPDATED \
    | pyscumm.constant.UPDATED

class Box( AbstractBox, Object ):

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        AbstractBox.__init__( self, shadow, depth  )
        self.color = Vector4D( [ 0.2, 0.2, 1., 0.2 ] )
        self.visible = False
        self.solver = None
        self._base = None

    def __del__( self ):
        if not isinstance( self._base, NoneType ):
            glDeleteLists( self._base, 1 )

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Box()
        AbstractBox.clone( self, obj, deep )
        Object.clone( self, obj, deep )
        return obj

    def update( self ):
        if self.copy.frozen \
        or not ( self.copy.updated & BOX_UPDATED \
        or self.updated & SELF_UPDATED ):
            self.updated = 0
            return
        #print "pyscumm.gfx.gl.Box.update()"
        if ( self.copy.updated & SIZE_UPDATED ) and not self.copy.size.is_cero():
            self.box[0] = Vector3D([0.,0.,0.])
            self.box[1] = Vector3D([self.copy.size[0],0.,0.])
            self.box[2] = Vector3D([self.copy.size[0],self.copy.size[1],0.])
            self.box[3] = Vector3D([0.,self.copy.size[1],0.])
        self.box.update()
        Object.update( self )
        if not isinstance( self._base, NoneType ):
            glDeleteLists( self._base, 1 )
        color_border = self.color.scale( BORDER_LIGHT )
        color_border[3] = 1.0
        self._base = glGenLists( 1 )
        glNewList( self._base, GL_COMPILE )
        # Draw the box
        glColor( self.color )
        glBegin( GL_QUADS )
        glVertex2f( *self.box[0][:2] )
        glVertex2f( *self.box[1][:2] )
        glVertex2f( *self.box[2][:2] )
        glVertex2f( *self.box[3][:2] )
        glEnd()
        # Draw the center point
        glEnable( GL_POINT_SMOOTH )
        glPointSize( POINT_SIZE )
        glBegin( GL_POINTS )
        glVertex2f( 0., 0. )
        glVertex2f( *self.insertion[:2] )
        glEnd()
        glDisable( GL_POINT_SMOOTH )
        # Draw the border
        glEnable( GL_LINE_SMOOTH )
        glColor( color_border )
        glLineWidth( BORDER_SIZE )
        glBegin( GL_LINE_STRIP )
        glVertex2f( *self.box[0][:2] )
        glVertex2f( *self.box[1][:2] )
        glVertex2f( *self.box[2][:2] )
        glVertex2f( *self.box[3][:2] )
        glVertex2f( *self.box[0][:2] )
        glEnd()
        glDisable( GL_LINE_SMOOTH )
        glEndList()

    def draw( self ):
        if not self.visible: return
        glPushMatrix()
        Object.draw( self )
        glCallList( self._base )
        glPopMatrix()
