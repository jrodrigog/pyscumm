from types import NoneType
from pyscumm.gfx import Animation
from pyscumm.gfx.gl import GLObject, Image

class ImageAnimation( GLObject, Animation ):
	"""A animation composed of various images"""
	def __init__( self, reset=0, end=0, fps=30., image=[] ):
		GLObject.__init__( self )
		Animation.__init__( self, reset, end, fps )
		self._image = image
		
	def clone( self, obj=None, deep=False ):
		if isinstance( obj, NoneType ): obj = ImageAnimation()
		# Clone via the parents
		GLObject.clone( self, obj, deep )
		Animation.clone( self, obj, deep )
		# Deep cloning
		if not deep: obj.image = self._image[:]
		else: obj.image = [
			i.clone( deep = True ) for i in self._image ]
	
	def get_image( self ): return self._image
	def set_image( self, image ): self._image = image
	
	def draw( self ):
		"""Draw the current frame Image"""
		self._image[ self._frame ].draw()
	
	def deserialize( self, element, obj = None ):
		"""Deserialize from XML"""
		if obj == None: obj = ImageAnimation()
		GLObject.deserialize( element, obj )
		Animation.deserialize( element, obj )
		for e in element.getElementsByTagName("Image"):
			image = Image.deserialize( e )
			image.copy = obj
			obj.image.append( image )
		return obj
		
	def update( self ):
		Animation.update( self )
		GLObject.update( self )
	
	image = property( get_image, set_image )
	deserialize = classmethod( deserialize )
