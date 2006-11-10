from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx.gl import GLObject, Image
from pyscumm.gfx.vector import Vector2D

class ImageScroll( Image ):
	def __init__( self,
	texture=None, tex_location=None, tex_speed=None, tex_repeat=None ):
		Image.__init__( self, texture )
		if not tex_location: self._tex_location = Vector2D( [0.,0.] )
		if not tex_speed: self._tex_speed = Vector2D( [0.,0.] )		
		if not tex_repeat: self._tex_repeat = Vector2D( [1.,1.] )
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = ImageScroll()
		Image.clone( self, obj, deep )
		self._tex_location.clone( obj.tex_location, deep )
		self._tex_speed.clone( obj.tex_speed, deep )
		self._tex_repeat.clone( obj.tex_repeat, deep )
		return obj

	def set_tex_repeat( self, repeat ): self._tex_repeat = repeat
	def get_tex_repeat( self ): return self._tex_repeat

	def set_tex_location( self, tex_location ):
		self._tex_location = tex_location
	def get_tex_location( self ):
		return self._tex_location
	
	def set_tex_speed( self, tex_speed ):
		self._tex_speed = tex_speed
	def get_tex_speed( self ):
		return self._tex_speed
	
	def update( self ):
		"""Update the texcoords"""
		Image.update( self )
		self._tex_location += self._tex_speed
		x  = self._tex_location[0]
		y  = self._tex_location[1]
		x_ = ( x + self._tex_repeat[0] )
		y_ = ( y + self._tex_repeat[1] )
		self._tc[0][0] = x
		self._tc[0][1] = y
		self._tc[1][0] = x_
		self._tc[1][1] = y
		self._tc[2][0] = x_
		self._tc[2][1] = y_
		self._tc[3][0] = x
		self._tc[3][1] = y_

	def draw( self ):
		"""Texturize the Image in a quad and 
		apply the texcoords"""
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
		if obj == None: obj = ImageScroll()
		Image.deserialize( element, obj )
		tmp = element.getElementsByTagName("TextureSpeed")
		if len(tmp):
			obj.tex_speed = Vector2D.deserialize( tmp.item( 0 ) )
		tmp = element.getElementsByTagName("TextureLocation")
		if len(tmp):
			obj.tex_location = Vector2D.deserialize( tmp.item( 0 ) )
		tmp = element.getElementsByTagName("TextureRepeat")
		if len(tmp):
			obj.tex_repeat = Vector2D.deserialize( tmp.item( 0 ) )
		return obj
	
	tex_speed = property( get_tex_speed, set_tex_speed )
	tex_location = property( get_tex_location, set_tex_location )
	tex_repeat = property( get_tex_repeat, set_tex_repeat )
	deserialize = classmethod( deserialize )

