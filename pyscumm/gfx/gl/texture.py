from types import NoneType
import re
import pygame, cStringIO, base64
from OpenGL.GL import *
import pyscumm.vector

class Texture:
    _src = re.compile("^((?P<file>file)|(?P<https>https)|(?P<http>http)):(?P<res>.*)",re.I)
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
            self.size  = pyscumm.vector.Vector3D( [ float( img.get_width() ), float( img.get_height() ), 0. ] )
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
            m = cls.src.search( tmp )
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

