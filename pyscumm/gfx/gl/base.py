import types
import OpenGL.GL
from pyscumm.gfx import Drawable

class Object( Drawable ):
    """Abstract GL Object; contains the location, insertion,
    rotation and color of the object"""

    def __init__( self ):
        Drawable.__init__( self )

    def clone( self, obj=None, deep=False ):
        """Clone the object"""
        if isinstance( obj, types.NoneType ): obj = Object()
        Drawable.clone( self, obj, deep )
        return obj

    def draw( self ):
        """Draw the abstract object, position and colorize it"""
        o = self.copy
        OpenGL.GL.glTranslatef( o.location[0], o.location[1], o.location[2] )
        OpenGL.GL.glRotatef( o.rotation[0], o.rotation[1], o.rotation[2], o.rotation[3] )
        OpenGL.GL.glScalef( o.scale[0], o.scale[1], o.scale[2] )
        OpenGL.GL.glTranslatef( -o.insertion[0], -o.insertion[1], -o.insertion[2] )
        OpenGL.GL.glColor4f( o.color[0], o.color[1], o.color[2], o.color[3] )
        for child in self.child: child.draw()

    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Object()
        return Drawable.deserialize( element, obj )

    deserialize = classmethod( deserialize )
