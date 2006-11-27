import sys
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import pyscumm, random, pyscumm.gfx.gl

class Taverna( pyscumm.scene.Scene ):
    N = 3
    def start( self ):
        pyscumm.vm.VM().display.set_icon("icon.png", (5,75) )
        self._state = Taverna1()
        self._dragging = None
        self._offset = None
        self._save_color = None
        self._colored = None
        self[ "logobig" ] = pyscumm.gfx.gl.Image( pyscumm.gfx.gl.Texture("logo_quad.png", pyscumm.Vector2D([229.,180.]) ))
        self[ "logobig" ].location[0] = pyscumm.vm.VM().display.size[0]/2
        self[ "logobig" ].location[1] = pyscumm.vm.VM().display.size[1]/2
        print pyscumm.vm.VM().display.size[0]
        for i in xrange( self.N ):
            self[ "logo%d" % i ] = self[ "logobig" ].clone()
            self[ "logo%d" % i ].scale *= pyscumm.vector.Vector3D([0.5,0.5,1.])

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
        print pyscumm.vm.VM().clock.fps
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

    def key_down( self, event ):
        if event.key == pyscumm.K_SPACE: pyscumm.vm.VM().display.toggle_full_screen()
        return self

    def update( self ):
        pyscumm.scene.SceneState.update(self)
        for obj in self.scene:
            self.scene[obj].rotate( 0.1 )
        return self

pyscumm.vm.VM.boot( Taverna(), pyscumm.gfx.gl.Display() )
