import pyscumm, sys

class MyObject( pyscumm.object.Object ):
    def __init__( self ):
        box = pyscumm.box.Box()
        box.location[0] = 320.; box.location[1] = 240.
        box.box[0][0] = -200.; box.box[0][1] = -200.
        box.box[1][0] =  200.; box.box[1][1] = -200.
        box.box[2][0] =  200.; box.box[2][1] =  200.
        box.box[3][0] = -200.; box.box[3][1] =  200.
        self[ "box" ] = box
    def collides( self, obj ):
        return self["box"].collides( obj )

class Taverna( pyscumm.scene.Scene ):
    def start( self ):
        self._state = Taverna1()
        self[ "obj" ] = MyObject()

class Taverna1( pyscumm.scene.SceneState ):
    pass

pyscumm.vm.VM().state = pyscumm.vm.NormalMode()
pyscumm.vm.VM.boot( Taverna() )
