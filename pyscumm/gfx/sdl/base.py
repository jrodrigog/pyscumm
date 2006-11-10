from gfx import Drawable
from types import NoneType

class SDLObject( Drawable ):
	"""Abstract SDL Object; extends drawable"""	
	def __init__( self ):
		Drawable.__init__( self )
		
	def clone( self, obj=None, deep=False ):
		"""Clone the object"""
		if isinstance( obj, NoneType ): obj = SDLObject()
		Drawable.clone( self, obj, deep )
		return obj

	def draw( self ):
		"""Draw the abstract object, position and colorize it"""
		raise NotImplemented

	def deserialize( self, element, obj=None ):
		"""Deserialize from XML"""
		raise NotImplemented

	deserialize = classmethod( deserialize )
