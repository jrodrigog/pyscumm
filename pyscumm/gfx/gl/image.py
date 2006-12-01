import types
from OpenGL.GL import *
from pyscumm.vector import Vector2D, Vector3D
from pyscumm.gfx.gl import Object, Texture, Box

class Image( Object ):
    """A Image encapsulates a Texture and
    texturizes it in a quad"""
    def __init__( self, texture = None ):
        Object.__init__( self )
        self._texture = texture
        self.collider = Box()
        self.collider.copy = self
        self._tc = [
            Vector2D( [ 0.0, 0.0 ] ),
            Vector2D( [ 1.0, 0.0 ] ),
            Vector2D( [ 1.0, 1.0 ] ),
            Vector2D( [ 0.0, 1.0 ] ) ]
        self._init_collider()

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = Image()
        Object.clone( self, obj, deep )
        if self._texture:
            obj.texture = self._texture.clone( deep )
        return obj

    def _init_collider( self ):
        if not self._texture: return
        t_size = self._texture.size
        self.collider.box[0] = Vector3D([0.,0.,0.])
        self.collider.box[1] = Vector3D([t_size[0],0.,0.])
        self.collider.box[2] = Vector3D([t_size[0],t_size[1],0.])
        self.collider.box[3] = Vector3D([0.,t_size[1],0.])

    def get_size( self ):
        try: return self._texture.size
        except AttributeError: return None
    def set_size( self, size ):
        try: self._texture.size
        except AttributeError: pass

    def get_texture( self ): return self._texture
    def set_texture( self, texture ):
        self._texture = texture
        self._init_collider()

    def draw( self ):
        """Texturize the Image in a quad"""
        t_size = self._texture.size
        glPushMatrix()
        self.collider.draw()
        Object.draw( self )
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, self._texture.id )
        glBegin( GL_QUADS )
        glTexCoord2f( *self._tc[0] ); glVertex2f( 0        , 0         )
        glTexCoord2f( *self._tc[1] ); glVertex2f( t_size[0], 0         )
        glTexCoord2f( *self._tc[2] ); glVertex2f( t_size[0], t_size[1] )
        glTexCoord2f( *self._tc[3] ); glVertex2f( 0        , t_size[1] )
        glEnd()
        glDisable( GL_TEXTURE_2D )
        glPopMatrix()

    def update( self ):
        """Update the Image and the collider"""
        Object.update( self )
        self.collider.update()

    @classmethod
    def deserialize( cls, element, obj = None ):
        """Deserialize from XML"""
        if obj == None: obj = Image()
        Object.deserialize( element, obj )
        obj.texture = Texture.deserialize(
            element.getElementsByTagName("Texture").item( 0 ) )
        obj.size = obj.texture.size
        return obj

    size    = property( get_size, set_size )
    texture = property( get_texture, set_texture )

