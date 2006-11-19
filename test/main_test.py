import pyscumm, sys

class Taverna( pyscumm.scene.Scene ):
    def start( self ):
        self._state = Taverna1()

class Taverna1( pyscumm.scene.SceneState ):
    pass

pyscumm.vm.VM.boot( Taverna() )
