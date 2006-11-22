import pyscumm, sys, random, pyscumm.box

"""
class MyObject( pyscumm.object.Object ):

    def __init__( self ):
        self[ 'box' ] = pyscumm.box.Box()
        self[ 'box' ].location[0] = 320.; self[ 'box' ].location[1] = 240.
        self[ 'box' ].box[0][0] = -200.; self[ 'box' ].box[0][1] = -200.
        self[ 'box' ].box[1][0] =  200.; self[ 'box' ].box[1][1] = -200.
        self[ 'box' ].box[2][0] =  200.; self[ 'box' ].box[2][1] =  200.
        self[ 'box' ].box[3][0] = -200.; self[ 'box' ].box[3][1] =  200.

    def collides( self, obj ):
        return self['box'].collides( obj )
"""

class MyObject( pyscumm.object.Object ):
    count = 0
    def __init__( self ):
        self._box = pyscumm.box.Box()
        self._box.location[0] = 320.; self._box.location[1] = 240.;
        self._box.box[0][0] = -50.; self._box.box[0][1] = -50.
        self._box.box[1][0] =  50.; self._box.box[1][1] = -50.
        self._box.box[2][0] =  50.; self._box.box[2][1] =  50.
        self._box.box[3][0] = -50.; self._box.box[3][1] =  50.
        self["id"] = self.__class__.count
        self.__class__.count += 1

    def collides( self, obj ):
        return self._box.collides( obj )
    def __cmp__( self, obj ):
        return cmp( self._box.location[2], obj.box.location[2] )
    def get_box( self ): return self._box
    box = property( get_box )

class Taverna( pyscumm.scene.Scene ):
    def start( self ):
        self._state = Taverna1()

        for i in xrange( 64 ):
            x = MyObject()
            #x[ 'box' ].location[0] = random.random() * 640
            #x[ 'box' ].location[1] = random.random() * 320
            x.box.location[0] = random.random() * 640
            x.box.location[1] = random.random() * 320
            x.box.location[2] = random.random()
            x.box.update()
            self[ id(x) ] = x

class Taverna1( pyscumm.scene.SceneState ):
    pass

pyscumm.vm.VM().state = pyscumm.vm.NormalMode()
pyscumm.vm.VM.boot( Taverna() )
