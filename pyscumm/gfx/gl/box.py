import OpenGL.GL
import pyscumm.box
import pyscumm.vector
from pyscumm.gfx.gl import Object

class Box( pyscumm.box.Box, Object ):

    BORDER_LIGHT = 1.5
    BORDER_SIZE = 1.
    POINT_SIZE = 5.

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        pyscumm.box.Box.__init__( self, shadow, depth  )
        self._color = pyscumm.vector.Vector4D( [
            0.2, 0.2, 1., 0.4 ] )
        self._base = None
        self.update()

    def draw( self ):
        color_border = self._copy.color.scale( self.BORDER_LIGHT )
        color_border[3] = 1.0
        OpenGL.GL.glPushMatrix()
        Object.draw( self )
        # Draw the box
        OpenGL.GL.glBegin( OpenGL.GL.GL_QUADS )
        OpenGL.GL.glVertex2f( *self._box[0][:2] )
        OpenGL.GL.glVertex2f( *self._box[1][:2] )
        OpenGL.GL.glVertex2f( *self._box[2][:2] )
        OpenGL.GL.glVertex2f( *self._box[3][:2] )
        OpenGL.GL.glEnd()
        # Draw the center point
        OpenGL.GL.glPointSize( self.POINT_SIZE )
        OpenGL.GL.glBegin( OpenGL.GL.GL_POINTS )
        OpenGL.GL.glVertex2f( 0., 0. )
        OpenGL.GL.glVertex2f( *self._insertion[:2] )
        OpenGL.GL.glEnd()
        # Draw the border
        OpenGL.GL.glColor( color_border )
        OpenGL.GL.glLineWidth( self.BORDER_SIZE )
        OpenGL.GL.glBegin( OpenGL.GL.GL_LINE_STRIP )
        OpenGL.GL.glVertex2f( *self._box[0][:2] )
        OpenGL.GL.glVertex2f( *self._box[1][:2] )
        OpenGL.GL.glVertex2f( *self._box[2][:2] )
        OpenGL.GL.glVertex2f( *self._box[3][:2] )
        OpenGL.GL.glVertex2f( *self._box[0][:2] )
        OpenGL.GL.glEnd()
        OpenGL.GL.glPopMatrix()




