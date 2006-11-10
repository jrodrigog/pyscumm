from types import NoneType
from pyscumm.gfx import Animation, Vector2D
from pyscumm.gfx.gl import BitmapCallList

class BitmapAnimation( Animation, BitmapCallList ):

	def __init__( self, reset=0, end=0, fps=30., texture=None, disp=None, side=Vector2D([16,16]) ):
		BitmapCallList.__init__( self, texture, disp, side )
		Animation.__init__( self, reset, end, fps )
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = BitmapAnimation()
		BitmapCallList.clone( self, obj, deep )
		Animation.clone( self, obj, deep )
		return obj
	
	def update( self ):
		BitmapCallList.update( self )
		Animation.update( self )
		self._call = [ self._frame ]
	
	def deserialize( self, element, obj = None ):
		if obj == None: obj = BitmapAnimation()
		Animation.deserialize( element, obj )
		BitmapCallList.deserialize( element, obj )
		return obj
	
	deserialize = classmethod( deserialize )
