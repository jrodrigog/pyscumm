import math
from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx import Vector2D
from pyscumm.gfx.gl import GLObject, Image

"""
+---+---+
| *-|-* |
+-|-+-|-+
| *-|-* |
+---+---+
"""

class Scroll( GLObject ):
	"""A scroll composed of various images in a grid"""
	def __init__( self, side=Vector2D([0,0]), screen=Vector2D([800,600]), image=[] ):
		GLObject.__init__( self )
		self._side = side
		self._screen = screen
		self._image = image
		if self._image: self.build()
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = Scroll()
		GLObject.clone( self, obj, deep )
		self._side.clone( obj.side, deep )
		self._screen.clone( obj.screen, deep )
		# Deep cloning
		if not deep:
			obj.image = self._image[:]
		else:
			obj.image = [
				i.clone( deep = True ) for i in self._image ]
			obj.build()
		return obj

	def clear( self ): pass
	def build( self ):
		"""Position de images in the given offset, forming a grid."""
		assert len( self._image )\
			and len( self._image ) == ( self._side[0] * self._side[1] )
		self._size = None

		z = int( self._side[0] )
		for i in xrange( int( self._side[1] ) ):
			for j in xrange( int( self._side[0] ) ):
				k = (i*z)+j
				if self._size != None:
					assert self._size == self._image[k].size
				self._size = self._image[k].size
		
		for i in xrange( int( self._side[1] ) ):
			for j in xrange( int( self._side[0] ) ):
				k = (i*z)+j
				self._image[k].location[0] = self._size[0] * j
				self._image[k].location[1] = self._size[1] * i
		
	def get_side( self ): return self._side
	def set_side( self, side ): self._side = side
	def get_size( self ): return self._size
	def get_image( self ): return self._image
	def set_image( self, image ): self._image = image
	def get_screen( self ): return self._screen
	def set_screen( self, screen ): self._screen = screen
	
	def draw( self ):
		"""Draw the scroll, only the focused elements."""
		y = self._insertion[ 1 ] - self._location[ 1 ]
		x = self._insertion[ 0 ] - self._location[ 0 ]
		
		i_s = int( math.floor( y / self._size[ 1 ] ) )
		i_e = int( math.ceil( ( y + self._screen[ 1 ] ) / self._size[ 1 ] ) )
		
		if i_s > self._side[1] or i_e < 0: return
		if i_s < 0: i_s = 0
		if i_e > self._side[1]: i_e = int( self._side[1] )
		
		j_s = int( math.floor( x / self._size[ 0 ] ) )
		j_e = int( math.ceil( ( x + self._screen[ 0 ] ) / self._size[ 0 ] ) )
		
		if j_s > self._side[0] or j_e < 0: return
		if j_s < 0: j_s = 0
		if j_e > self._side[0]: j_e = int( self._side[0] )
				
		glPushMatrix()
		GLObject.draw( self )
		z = int( self._side[0] )
		for i in xrange( i_s, i_e ):
			for j in xrange( j_s, j_e ):
				k = (i*z)+j
				self._image[ k ].draw()
		glPopMatrix()
		
	def update( self ):
		self._insertion += self._speed
	
	def deserialize( self, element, obj=None ):
		"""Deserialize from XML"""
		if obj == None: obj = Scroll()
		GLObject.deserialize( element, obj )
		tmp = element.getElementsByTagName("Side")
		if len( tmp ):
			obj.side = Vector2D.deserialize( tmp.item( 0 ) )
		tmp = element.getElementsByTagName("Screen")
		if len( tmp ):
			obj.screen = Vector2D.deserialize( tmp.item( 0 ) )
		for e in element.getElementsByTagName("Image"):
			obj.image.append( Image.deserialize( e ) )
		if obj.image and obj.side and obj.screen:
			obj.build()
		return obj

	side = property( get_side, set_side )
	size = property( get_size )
	image = property( get_image, set_image )
	screen = property( get_screen, set_screen )
	deserialize = classmethod( deserialize )
