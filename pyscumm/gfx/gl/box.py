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
            1., 0.25, 0.25, 0.3 ] )
        self._base = None
        self.update()

    def draw( self ):
        OpenGL.GL.glPushMatrix()
        Object.draw( self )
        OpenGL.GL.glListBase( self._base )
        OpenGL.GL.glCallLists( [ 0 ] )
        OpenGL.GL.glPopMatrix()

    def update( self ):
        Object.update( self )
        pyscumm.box.Box.update( self )
        color_border = self._copy.color.scale( self.BORDER_LIGHT )
        color_border[3] = 1.0
        if self._base: OpenGL.GL.glDeleteLists( self._base, 1 )
        self._base = OpenGL.GL.glGenLists(1)

        OpenGL.GL.glNewList( self._base, OpenGL.GL.GL_COMPILE )
        # Draw the box
        OpenGL.GL.glBegin( OpenGL.GL.GL_QUADS )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glVertex3f( *self._box[1] )
        OpenGL.GL.glVertex3f( *self._box[2] )
        OpenGL.GL.glVertex3f( *self._box[3] )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glEnd()
        # Draw the box border
        OpenGL.GL.glEnable( OpenGL.GL.GL_LINE_SMOOTH )
        OpenGL.GL.glColor( color_border )
        OpenGL.GL.glLineWidth( self.BORDER_SIZE )
        OpenGL.GL.glBegin( OpenGL.GL.GL_LINE_STRIP )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glVertex3f( *self._box[1] )
        OpenGL.GL.glVertex3f( *self._box[2] )
        OpenGL.GL.glVertex3f( *self._box[3] )
        OpenGL.GL.glVertex3f( *self._box[0] )
        OpenGL.GL.glEnd()
        OpenGL.GL.glDisable( OpenGL.GL.GL_LINE_SMOOTH )
        # Draw the center point
        OpenGL.GL.glEnable( OpenGL.GL.GL_POINT_SMOOTH )
        OpenGL.GL.glPointSize( self.POINT_SIZE )
        OpenGL.GL.glBegin( OpenGL.GL.GL_POINTS )
        OpenGL.GL.glVertex3f( 0., 0., 0. )
        OpenGL.GL.glEnd()
        OpenGL.GL.glDisable( OpenGL.GL.GL_POINT_SMOOTH )
        OpenGL.GL.glEndList()




