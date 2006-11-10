from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx import Vector2D
from pyscumm.gfx.gl import GLObject, Texture

class Image( GLObject ):
	"""A Image encapsulates a Texture and 
	texturizes it in a quad"""
	def __init__( self, texture = None ):
		GLObject.__init__( self )
		self._size = Vector2D()
		self._tc = [
			Vector2D([ 0.0, 0.0 ]),
			Vector2D([ 1.0, 0.0 ]),
			Vector2D([ 1.0, 1.0 ]),
			Vector2D([ 0.0, 1.0 ]) ]
		self.texture = texture
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = Image()
		GLObject.clone( self, obj, deep )
		# Deep cloning
		if not deep:
			obj.texture = self._texture
			obj.tc = self._tc[:]
		else:
			obj.tc = [ i.clone( deep = True ) for i in self._tc ]
			obj.texture = self._texture.clone( deep = True )
		return obj
	
	def get_tc( self ): return self._tc
	def set_tc( self, tc_ld ): self._tc = tc

	def get_size( self ): return self._size
	def set_size( self, size ): self._size
	
	def get_texture( self ): return self._texture
	def set_texture( self, texture ):
		self._texture = texture
		if self._texture:
			self._size = texture.size.clone()
		
	def draw( self ):
		"""Texturize the Image in a quad"""
		glPushMatrix()
		GLObject.draw( self )
		glEnable( GL_TEXTURE_2D )
		glBindTexture( GL_TEXTURE_2D, self._texture.id )
		glBegin( GL_QUADS )
		glTexCoord2f( *self._tc[0] ); glVertex2f( 0            , 0             )
		glTexCoord2f( *self._tc[1] ); glVertex2f( self._size[0], 0             )
		glTexCoord2f( *self._tc[2] ); glVertex2f( self._size[0], self._size[1] )
		glTexCoord2f( *self._tc[3] ); glVertex2f( 0            , self._size[1] )
		glEnd()
		glPopMatrix()
		
	def deserialize( self, element, obj = None ):
		"""Deserialize from XML"""
		if obj == None: obj = Image()
		GLObject.deserialize( element, obj )
		tmp = element.getElementsByTagName("Texture")
		if len(tmp):
			obj.texture = Texture.deserialize( tmp.item( 0 ) )
		obj.size = obj.texture.size
		return obj
	
	deserialize = classmethod( deserialize )
	size    = property( get_size, set_size )
	texture = property( get_texture, set_texture )
	tc      = property( get_tc, set_tc )

