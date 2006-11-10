import cStringIO, base64, re, pygame
from types import NoneType
from OpenGL.GL import *
from pyscumm.gfx import Vector2D

class Texture:
	_src = re.compile("^((?P<file>file)|(?P<https>https)|(?P<http>http)):(?P<res>.*)",re.I)
	def __init__( self, file = None, name = None ):
		self._id = None
		self._name = name
		if file: self.load( file )
		
	def __del__( self ):
		if self._id:
			pass
			#glDeleteTextures( self._id ) FIXME
	
	def clone( self, obj=None, deep=False ):
		"""Clone the object, the texture is always shared"""
		if isinstance( obj, NoneType ): obj = Texture()
		obj.id   = self._id
		obj.name = self._name
		obj.size = self._size.clone()
		return obj
			
	def get_id( self ): return self._id
	def set_id( self, id ): self._id = id
	
	def get_name( self ): return self._name
	def set_name( self, name ): self._name = name

	def load( self, file ):
		img         = pygame.image.load( file )
		self._size  = Vector2D( [ float( img.get_width() ), float( img.get_height() ) ] )
		img_buf     = pygame.image.tostring( img, "RGBA", 1 )
		
		self._id    = glGenTextures( 1 )

		glBindTexture( GL_TEXTURE_2D, self._id )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexImage2D(
			GL_TEXTURE_2D,
			0,
			GL_RGBA,
			int( img.get_width() ),
			int( img.get_height() ),
			0,
			GL_RGBA,
			GL_UNSIGNED_BYTE,
			img_buf
		)
	def get_size( self ): return self._size
	def set_size( self, size ): self._size = size
	def deserialize( self, element, obj=None ):
		if obj == None: obj = Texture()
		obj.name = element.getAttribute("name")
		tmp = element.getAttribute("src")
		if tmp:
			# Read from source
			m = self._src.search( tmp )
			if m.group( "file" ):
				f = file( m.group("res"), "rb" )
			elif m.group( "http" ):
				raise NotImplemented
			elif m.group( "https" ):
				raise NotImplemented
		else:
			# Read from XML
			f = cStringIO.StringIO(
				base64.decodestring( element.firstChild.nodeValue ) )
			
		obj.load( f )
		return obj

	id          = property( get_id, set_id )
	size        = property( get_size, set_size )
	name        = property( get_name, set_name )
	deserialize = classmethod( deserialize )
