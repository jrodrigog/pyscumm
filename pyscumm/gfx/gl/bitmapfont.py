from types import NoneType
from pyscumm.gfx import Vector2D
from pyscumm.gfx.gl import BitmapCallList

class BitmapFont( BitmapCallList ):
	LEFT   = 1
	CENTER = 1<<1
	RIGHT  = 1<<2
	TOP    = 1<<4
	MIDDLE = 1<<5
	BOTTOM = 1<<6
	
	def __init__( self, texture=None, disp=None ):
		BitmapCallList.__init__( self, texture, disp )
		self._align = self.BOTTOM | self.LEFT
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = BitmapFont()
		BitmapCallList.clone( self, obj, deep )
		obj.align = self._align
		return obj

	def write( self, text ):
		"""Write this text on the next draw()"""
		self._call = map( ord, text )
		
		size = self.size
		if self._align & self.LEFT:
			self._insertion[0] = 0.
		elif self._align & self.CENTER:
			self._insertion[0] = size[0]/2.
		elif self._align & self.RIGHT:
			self._insertion[0] = size[0]

		if self._align & self.TOP:
			self._insertion[1] = size[1]
		elif self._align & self.MIDDLE:
			self._insertion[1] = size[1]/2.
		elif self._align & self.BOTTOM:
			self._insertion[1] = 0.

	def get_size( self ):
		"""Computes the width and height of the text"""
		return Vector2D( [
			reduce(
				lambda x,y: x+y,
				map( lambda i: self._disp[i], self._call ),
				0. ), self._texture.size[1] / self._side[1] ] )
	
	def get_align( self ): return self._align
	def set_align( self, align ): self._align = align
	
	def deserialize( self, element, obj = None ):
		"""Deserialize from XML"""
		if obj == None: obj = BitmapFont()
		BitmapCallList.deserialize( element, obj )
		return obj
	
	size  = property( get_size )
	align = property( get_align, set_align )	
	deserialize = classmethod( deserialize )
