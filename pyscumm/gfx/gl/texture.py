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
import pygame, re, cStringIO, base64
from OpenGL.GL import *
from pyscumm.vector import Vector3D

METHOD = re.compile("^((?P<file>file)|(?P<https>https)|(?P<http>http)):(?P<res>.*)",re.I)
class Texture:
    def __init__( self, file = None, size = None, name = None ):
        self.id = None
        self.name = name
        if file: self.load( file, size )
    def __del__( self ):
        if not self.id: return
        glDeleteTextures( self.id )

    def clone( self, obj=None, deep=False ):
        return self

    def load( self, file, size = None ):
        img         = pygame.image.load( file )
        img_buf     = pygame.image.tostring( img, "RGBA", 1 )
        self.id    = glGenTextures( 1 )
        if isinstance( size, NoneType ):
            self.size  = Vector3D( [ float( img.get_width() ), float( img.get_height() ), 0. ] )
        else:
            self.size = size

        glBindTexture( GL_TEXTURE_2D, self.id )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            int( img.get_width() ),
            int( img.get_height() ),
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_buf
        )

    @classmethod
    def deserialize( cls, element, obj=None ):
        if obj == None: obj = Texture()
        obj.name = element.getAttribute("name")
        tmp = element.getAttribute("src")
        if tmp:
            # Read from source
            m = METHOD.search( tmp )
            if m.group( "file" ):
                f = file( m.group("res"), "rb" )
            elif m.group( "http" ):
                raise NotImplemented
            elif m.group( "https" ):
                raise NotImplemented
        else:
            # Read from XML
            f = cStringIO.StringIO(
                base64.decodestring( element.firstChild.nodeValue ) )

        obj.load( f )
        return obj

