import box

class Object( dict ):

    def __init__(self):
        dict.__init__(self)
        self._box = box.Box()
        self._box.location[0] = 320.; self._box.location[1] = 240.
        self._box.box[0][0] = -200.; self._box.box[0][1] = 200.
        self._box.box[1][0] =  200.; self._box.box[1][1] = 200.
        self._box.box[2][0] =  200.; self._box.box[2][1] =  -200.
        self._box.box[3][0] = -200.; self._box.box[3][1] =  -200.

    def get_box( self ):
        return self._box

    def __cmp__( self ):
        pass

    def action( self, cmd ):
        pass

    def collides( self, obj ):
        self._box.collides( obj )

    def update( self ):
        pass

    def draw( self ):
        pass

    box = property( get_box )


