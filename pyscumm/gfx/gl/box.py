import pyscumm.box
from pyscumm.gfx.gl import Object

class Box( pyscumm.box.Box, Object ):

    def __init__( self, shadow=1., depth=1. ):
        Object.__init__( self )
        pyscumm.box.Box.__init__( self, shadow, depth  )

    def draw( self ):
        print 'Pintamos con GL las box'

