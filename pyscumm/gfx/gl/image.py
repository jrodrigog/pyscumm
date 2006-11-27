import types
import OpenGL.GL
import pyscumm.vector
from pyscumm.gfx.gl import Object
from pyscumm.gfx.gl import Texture

class Image( Object ):
    """A Image encapsulates a Texture and
    texturizes it in a quad"""
    def __init__( self, texture = None ):
        Object.__init__( self )
        self._texture = texture
        self._collider = pyscumm.gfx.gl.Box()
        self._collider.copy = self
        self._tc = [
            [ 0.0, 0.0 ],
            [ 1.0, 0.0 ],
            [ 1.0, 1.0 ],
            [ 0.0, 1.0 ] ]
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
        self._collider.box[0] = pyscumm.vector.Vector3D([0.,0.,0.])
        self._collider.box[1] = pyscumm.vector.Vector3D([t_size[0],0.,0.])
        self._collider.box[2] = pyscumm.vector.Vector3D([t_size[0],t_size[1],0.])
        self._collider.box[3] = pyscumm.vector.Vector3D([0.,t_size[1],0.])

    def get_tc( self ): return self._tc
    def set_tc( self, tc_ld ): self._tc = tc

    def get_size( self ): return self._texture._size
    def set_size( self, size ): self._texture._size

    def get_texture( self ): return self._texture
    def set_texture( self, texture ):
        self._texture = texture
        self._init_collider()

    def draw( self ):
        """Texturize the Image in a quad"""
        t_size = self._texture.size
        OpenGL.GL.glPushMatrix()
        self._collider.draw()
        Object.draw( self )
        OpenGL.GL.glEnable( OpenGL.GL.GL_TEXTURE_2D )
        OpenGL.GL.glBindTexture( OpenGL.GL.GL_TEXTURE_2D, self._texture.id )
        OpenGL.GL.glBegin( OpenGL.GL.GL_QUADS )
        OpenGL.GL.glTexCoord2f( *self._tc[0] ); OpenGL.GL.glVertex2f( 0        , 0         )
        OpenGL.GL.glTexCoord2f( *self._tc[1] ); OpenGL.GL.glVertex2f( t_size[0], 0         )
        OpenGL.GL.glTexCoord2f( *self._tc[2] ); OpenGL.GL.glVertex2f( t_size[0], t_size[1] )
        OpenGL.GL.glTexCoord2f( *self._tc[3] ); OpenGL.GL.glVertex2f( 0        , t_size[1] )
        OpenGL.GL.glEnd()
        OpenGL.GL.glDisable( OpenGL.GL.GL_TEXTURE_2D )
        OpenGL.GL.glPopMatrix()


    def update( self ):
        """Update the Image and the collider"""
        Object.update( self )
        self._collider.update()

    def deserialize( self, element, obj = None ):
        """Deserialize from XML"""
        if obj == None: obj = Image()
        Object.deserialize( element, obj )
        obj.texture = Texture.deserialize(
            element.getElementsByTagName("Texture").item( 0 ) )
        obj.size = obj.texture.size
        return obj

    deserialize = classmethod( deserialize )
    size    = property( get_size, set_size )
    texture = property( get_texture, set_texture )
    tc      = property( get_tc, set_tc )

