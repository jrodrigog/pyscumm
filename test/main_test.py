import pyscumm, sys

class MyObject( pyscumm.object.Object ):
    pass

class Taverna( pyscumm.scene.Scene ):
    def start( self ):
        self._state = Taverna1()
        self[ 'obj' ] = MyObject()

class Taverna1( pyscumm.scene.SceneState ):
    pass




pyscumm.vm.VM().state = pyscumm.vm.NormalMode()
pyscumm.vm.VM.boot( Taverna() )
