import OpenGL.GL
import pyscumm.box
from pyscumm.gfx.gl import Object

class Box( pyscumm.box.Box, Object ):

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        pyscumm.box.Box.__init__( self, shadow, depth  )

    def draw( self ):
        OpenGL.GL.glPushMatrix()
        Object.draw( self )
        OpenGL.GL.glBegin( OpenGL.GL.GL_LINE_STRIP )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glVertex3f( *self._box[1] )
        OpenGL.GL.glVertex3f( *self._box[2] )
        OpenGL.GL.glVertex3f( *self._box[3] )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glEnd()
        OpenGL.GL.glBegin( OpenGL.GL.GL_QUADS )
        OpenGL.GL.glVertex3f( -5.,-5., 0. )
        OpenGL.GL.glVertex3f(  5.,-5., 0. )
        OpenGL.GL.glVertex3f(  5., 5., 0. )
        OpenGL.GL.glVertex3f( -5., 5., 0. )
        OpenGL.GL.glEnd()
        OpenGL.GL.glPopMatrix()
