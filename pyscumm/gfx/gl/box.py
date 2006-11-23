import pyscumm.box


class Box( pyscumm.box.Box ):

    def __init__( self ):
        pyscumm.box.Box.__init__( self )

    def draw( self ):
        print 'Pintamos con GL las box'

