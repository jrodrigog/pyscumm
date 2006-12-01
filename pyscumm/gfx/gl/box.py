from OpenGL.GL import *
from types import NoneType
from pyscumm.gfx.gl import Object
from pyscumm.box import Box as AbstractBox
from pyscumm.vector import Vector4D

BORDER_LIGHT = 1.5
BORDER_SIZE = 1.
POINT_SIZE = 5.

class Box( AbstractBox, Object ):

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        AbstractBox.__init__( self, shadow, depth  )
        self.color = Vector4D( [ 0.2, 0.2, 1., 0.2 ] )
        self.update()

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Box()
        AbstractBox.clone( self, obj, deep )
        Object.clone( self, obj, deep )
        return obj

    def draw( self ):
        glPushMatrix()
        glTranslatef( *self.copy.location )
        glRotatef( *self.copy.rotation )
        glScalef( *self.copy.scale )
        glTranslatef( *self.copy.insertion )
        glColor4f( *self.color )
        for child in self.child: child.draw()

        color_border = self.color.scale( BORDER_LIGHT )
        color_border[3] = 1.0
        # Draw the box
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
        glPopMatrix()




