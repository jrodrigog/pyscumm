from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx import Vector2D
from pyscumm.gfx.gl import GLObject, Texture

class BitmapCallList( GLObject ):
	"""An abstract bitmap calllist, a bitmap is divided into
	sub-bitmaps and they are textured separately; each piece
	is a position in a call list"""
	def __init__( self, texture=None, disp=[], side=Vector2D( [ 16, 16 ] ) ):
		GLObject.__init__( self )
		self._base    = None
		self._call    = []
		self._side    = side
		self._disp    = disp
		self._texture = texture
		self._count   = 0
		if self._texture != None and self._disp != None:
			self.build()
			
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = BitmapCallList()
		GLObject.clone( self, obj, deep )
		self._side.clone( obj.side, deep )
		obj.disp = self._disp[:]
		obj.call = self._call[:]
		# Deep cloning
		if not deep:
			obj.base = self._base
			obj.texture = self._texture
		else:
			obj.texture = self._texture.clone( deep = True )
			if obj.texture and obj.disp:
				obj.build()
		return obj

	def __del__( self ):
		self.clear()
	
	def clear( self ):
		"""Clear the GL call lists"""
		if self._base:
			pass # FIXME
			#glDeleteLists( self._base, self._count );
	
	def build( self ):
		"""Build the GL call list"""
		self.clear()
		assert self._texture.size[0] == self._texture.size[1]
		side_x   = self._texture.size[0] / self._side[0]
		side_y   = self._texture.size[1] / self._side[1]
		tc_w   = 1.0 / self._side[0]
		tc_h   = 1.0 / self._side[1]
		length = self._side[0]*self._side[1]
		self._base = glGenLists( length )
		for i in range( length ):
			tc_x = ( i % self._side[0] ) / float( self._side[0] )
			tc_y = ( i / self._side[1] ) / float( self._side[1] )
			glNewList( self._base + i, GL_COMPILE )
			glBegin( GL_QUADS )
			glTexCoord2f( tc_x       , 1.0 - tc_y - tc_h ); glVertex2f( 0.0   , 0.0  )
			glTexCoord2f( tc_x + tc_w, 1.0 - tc_y - tc_h ); glVertex2f( side_x, 0.0  )
			glTexCoord2f( tc_x + tc_w, 1.0 - tc_y        ); glVertex2f( side_x, side_y )
			glTexCoord2f( tc_x       , 1.0 - tc_y        ); glVertex2f( 0.0   , side_y )
			glEnd()
			glTranslatef( self._disp[ i ], 0.0, 0.0 )
			glEndList()
		self._count = self._side[0]*self._side[1]

	def draw( self ):
		"""Draw the list of call lists"""
		if not self._call: return
		glPushMatrix()
		GLObject.draw( self )
		glEnable( GL_TEXTURE_2D )
		glBindTexture( GL_TEXTURE_2D, self._texture.id )
		glListBase( self._base )
		glCallLists( [ self._call ] )
		glPopMatrix()

	def get_base( self ): return self._base
	def set_base( self, base ): self._base = base
	def get_texture( self ): return self._texture
	def set_texture( self, texture ): self._texture = texture
	def get_disp( self ): return self._disp
	def set_disp( self, disp ): self._disp = disp
	def get_side( self ): return self._side
	def set_side( self, side ): self._side = side
	def get_call( self ): return self._call
	def set_call( self, call ): self._call = call
		
	def deserialize( self, element, obj = None ):
		"""Deserialize from XML"""
		if obj == None: obj = BitmapCallList()
		GLObject.deserialize( element, obj )

		tmp = element.getElementsByTagName("Disp")
		if len( tmp ):
			obj.disp = map( float, tmp.item(0).firstChild.data.split(":") )
	
		tmp = element.getElementsByTagName("Side")
		if len( tmp ):
			obj.side = Vector2D.deserialize( tmp.item( 0 ) )
		
		tmp = element.getElementsByTagName("Texture")
		if len( tmp ):
			obj.texture = Texture.deserialize( tmp.item( 0 ) )
		
		if obj.texture and obj.disp:
			obj.build()
		return obj
	
	deserialize = classmethod( deserialize )
	side        = property( get_side, set_side )
	disp        = property( get_disp, set_disp )
	texture     = property( get_texture, set_texture )
	call        = property( get_call, set_call )
	base        = property( get_base, set_base )
	
