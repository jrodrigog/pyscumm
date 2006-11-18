import pyscumm, sys

class Taverna( pyscumm.scene.Scene ):
    def start( self ):
        self._state = Taverna1()

class Taverna1( pyscumm.scene.SceneState ):

    def on_quit( self ):
        pyscumm.vm.VM().display.close()
        sys.exit()
        return self

    def on_key_down( self, key ):
        print 'WAU!, se ha pulsado en mi juego la tecla', key
        return self

    def on_key_up( self, key ):
        print 'WAU!, se ha soltado en mi juego la tecla', key
        return self

    def on_mouse_click( self, button, obj ):
        print 'WAU!, se ha pulsado en mi juego el botoon', button
        return self


pyscumm.vm.VM.boot( Taverna() )
