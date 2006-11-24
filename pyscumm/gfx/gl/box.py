import OpenGL.GL
import pyscumm.box
from pyscumm.gfx.gl import Object

class Box( pyscumm.box.Box, Object ):

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        pyscumm.box.Box.__init__( self, shadow, depth  )
        self._base = None
        self.update()

    def draw( self ):
        OpenGL.GL.glPushMatrix()
        Object.draw( self )
        OpenGL.GL.glListBase( self._base )
        OpenGL.GL.glCallLists( 0 )
        OpenGL.GL.glPopMatrix()

    def update( self ):
        pyscumm.box.Box.update( self )
        if self._base:
            OpenGL.GL.glDeleteLists( self._base, 1 )
        self._base = OpenGL.GL.glGenLists(1)
        OpenGL.GL.glNewList( self._base, OpenGL.GL.GL_COMPILE )
        OpenGL.GL.glBegin( OpenGL.GL.GL_LINE_STRIP )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glVertex3f( *self._box[1] )
        OpenGL.GL.glVertex3f( *self._box[2] )
        OpenGL.GL.glVertex3f( *self._box[3] )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glEnd()
        OpenGL.GL.glPointSize( 4. )
        OpenGL.GL.glBegin( OpenGL.GL.GL_POINTS )
        OpenGL.GL.glVertex3f( 0., 0., 0. )
        OpenGL.GL.glEnd()
        OpenGL.GL.glEndList()




