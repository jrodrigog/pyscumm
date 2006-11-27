from types import NoneType
import re
import OpenGL.GL
import pyscumm.vector
import pygame, cStringIO, base64

class Texture:
    _src = re.compile("^((?P<file>file)|(?P<https>https)|(?P<http>http)):(?P<res>.*)",re.I)
    def __init__( self, file = None, size = None, name = None ):
        self._id = None
        self._name = name
        if file: self.load( file, size )
    def get_id( self ):
        return self._id
    def __del__( self ):
        if not self._id: return
        OpenGL.GL.glDeleteTextures( self._id )

    def clone( self, obj=None, deep=False ):
        return self

    def get_name( self ): return self._name
    def set_name( self, name ): self._name = name

    def load( self, file, size = None ):
        img         = pygame.image.load( file )
        img_buf     = pygame.image.tostring( img, "RGBA", 1 )
        self._id    = OpenGL.GL.glGenTextures( 1 )
        if isinstance( size, NoneType ):
            self._size  = pyscumm.vector.Vector3D( [ float( img.get_width() ), float( img.get_height() ), 0. ] )
        else:
            self._size = size

        OpenGL.GL.glBindTexture( OpenGL.GL.GL_TEXTURE_2D, self._id )
        OpenGL.GL.glTexParameteri( OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MAG_FILTER, OpenGL.GL.GL_LINEAR )
        OpenGL.GL.glTexParameteri( OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MIN_FILTER, OpenGL.GL.GL_LINEAR )
        OpenGL.GL.glTexImage2D(
            OpenGL.GL.GL_TEXTURE_2D,
            0,
            OpenGL.GL.GL_RGBA,
            int( img.get_width() ),
            int( img.get_height() ),
            0,
            OpenGL.GL.GL_RGBA,
            OpenGL.GL.GL_UNSIGNED_BYTE,
            img_buf
        )
    def get_size( self ): return self._size
    def set_size( self, size ): self._size = size
    def deserialize( self, element, obj=None ):
        if obj == None: obj = Texture()
        obj.name = element.getAttribute("name")
        tmp = element.getAttribute("src")
        if tmp:
            # Read from source
            m = self._src.search( tmp )
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

    id          = property( get_id )
    size        = property( get_size )
    deserialize = classmethod( deserialize )
