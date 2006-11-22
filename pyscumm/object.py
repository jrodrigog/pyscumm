import box

class Object( dict ):

    def __init__(self):
        dict.__init__(self)

    def __cmp__( self ):
        raise NotImplemented

    def action( self, cmd ):
        pass

    def collides( self, obj ):
        return None

    def update( self ):
        pass

    def draw( self ):
        pass
