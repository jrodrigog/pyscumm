import sys
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import pyscumm, random, pyscumm.gfx.gl

class Taverna( pyscumm.scene.Scene ):
    N = 8
    def start( self ):
        self._state = Taverna1()
        self._dragging = None
        self._offset = None
        self._save_color = None
        self._colored = None
        self[ "wally" ] = pyscumm.gfx.gl.Image(
            pyscumm.gfx.gl.Texture( "wally.png") )
        for i in xrange( self.N ):
            self[ "wally%d" % i ] = self[ "wally" ].clone()

    def get_save_color( self ): return self._save_color
    def set_save_color( self, save_color ): self._save_color = save_color
    def get_dragging( self ): return self._dragging
    def set_dragging( self, dragging ): self._dragging = dragging
    def get_offset( self ): return self._offset
    def set_offset( self, offset ): self._offset = offset
    def get_colored( self ): return self._colored
    def set_colored( self, colored ): self._colored = colored

    save_color = property( get_save_color, set_save_color )
    dragging = property( get_dragging, set_dragging )
    offset = property( get_offset, set_offset )
    colored = property( get_colored, set_colored )

class Taverna1( pyscumm.scene.SceneState ):
    _shared_state = {} # Singleton

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        pyscumm.scene.SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.location = event.location - self.scene.offset
        self.scene.dragging.update()
        return self

    def on_mouse_button_down( self, event ):
        if event.button != pyscumm.B_LEFT \
            or not event.object: return self
        self.scene.colored = event.object.pop()
        self.scene.save_color = self.scene.colored.collider.color
        self.scene.colored.collider.color = pyscumm.vector.Vector4D([ 1., 0., 0., 0.5 ])
        return self

    def on_mouse_button_up( self, event ):
        if not self.scene.colored: return self
        self.scene.colored.collider.color = self.scene.save_color
        self.scene.colored.update()
        return self

    def on_mouse_drag_start( self, event ):
        if event.button != pyscumm.B_LEFT \
            or not event.object: return self
        # Use the top object
        self.scene.dragging = event.object.pop()
        self.scene.offset = event.location - self.scene.dragging.location
        return self

    def on_mouse_drag_end( self, event ):
        if event.button != pyscumm.B_LEFT \
            or not self.scene.dragging: return self
        self.scene.dragging = None
        return self

    def on_mouse_click( self, event ):
        if event.button != pyscumm.B_RIGHT: return self
        raise pyscumm.vm.StopVM()
        return self

pyscumm.vm.VM.boot( Taverna(), pyscumm.gfx.gl.Display() )
