from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx import Vector2D
from pyscumm.gfx.gl import GLObject, Image

class FastImage( Image ):
	"""A Image encapsulates a Texture and 
	texturizes it in a quad, this implementation is based
	on a Call List"""
	def __init__( self, texture = None ):
		Image.__init__( self )
		self._size    = Vector2D()
		if texture:
			self._texture = texture
			self._size    = texture.size
		self._tc = [
			[ 0.0, 0.0 ],
			[ 1.0, 0.0 ],
			[ 1.0, 1.0 ],
			[ 0.0, 1.0 ] ]
		self._base = None
		if texture != None: self.build()
		
	def __del__( self ):
		self.clear()
	
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = FastImage()
		Image.clone( self, obj, deep )
		# Deep cloning
		if not deep: obj.base = self._base
		elif obj.texture: obj.build()
		return obj
	
	def clear( self ):
		"""Clear the GL call lists"""
		if self._base:
			pass # FIXME
			#glDeleteLists( self._base, self._count );
			
	def build( self ):
		self._base = glGenLists( 1 )
		glNewList( self._base, GL_COMPILE )
		glBegin( GL_QUADS )
		glTexCoord2f( *self._tc[0] ); glVertex2f( 0            , 0             )
		glTexCoord2f( *self._tc[1] ); glVertex2f( self._size[0], 0             )
		glTexCoord2f( *self._tc[2] ); glVertex2f( self._size[0], self._size[1] )
		glTexCoord2f( *self._tc[3] ); glVertex2f( 0            , self._size[1] )
		glEnd()
		glEndList()
		
	def get_base( self ): return self._base
	def set_base( self, base ): self._base = base
			
	def draw( self ):
		"""Texturize the Image in a quad"""
		glPushMatrix()
		GLObject.draw( self )
		glEnable( GL_TEXTURE_2D )
		glBindTexture( GL_TEXTURE_2D, self._texture.id )
		glListBase( self._base )
		glCallLists( [ 0 ] )
		glPopMatrix()
		
	def deserialize( self, element, obj = None ):
		"""Deserialize from XML"""
		if obj == None: obj = FastImage()
		Image.deserialize( element, obj )
		if obj.texture != None: obj.build()
		return obj
	
	deserialize = classmethod( deserialize )

