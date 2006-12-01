import sys
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import random
import pyscumm
from pyscumm.scene import Scene, SceneState
from pyscumm.vm import VM
from pyscumm.vector import *
from pyscumm.constant import B_LEFT, B_CENTER, B_RIGHT
from pyscumm.gfx.gl import Display, Image, Texture, Mouse

class Taverna( Scene ):
    N = 4
    def start( self ):
        VM().display.set_icon("icon.png", (5,75) )
        self.state = Taverna1()
        self.dragging = None
        self.offset = None
        self.save_color = None
        self.colored = None
        self[ "logobig" ] = Image( Texture("logo_quad.png" ), Vector3D( [229.,180.,0.] ) )
        self[ "logobig" ].collider.visible = True
        self[ "logobig" ].location[0] = VM().display.size[0]/2.
        self[ "logobig" ].location[1] = VM().display.size[1]/2.
        self[ "logobig" ].insertion[0] = -self[ "logobig" ].size[0]/2.
        self[ "logobig" ].insertion[1] = -self[ "logobig" ].size[1]/2.
        print self[ "logobig" ].collider.box
        for i in xrange( self.N ):
            n = "logo%d" % i
            self[ n ] = self[ "logobig" ].clone()
            self[ n ].collider.visible = True
            print self[ n ].collider.box
            #self[ n ].scale[0] *= 0.5
            #self[ n ].scale[1] *= 0.5

class Taverna1( SceneState ):
    _shared_state = {} # Singleton

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.location = event.location - self.scene.offset
        self.scene.dragging.update()
        return self

    def on_mouse_button_down( self, event ):
        if event.button != B_LEFT \
            or not event.object: return self
        print VM().clock.fps
        self.scene.colored = event.object.pop()
        self.scene.save_color = self.scene.colored.collider.color
        self.scene.colored.collider.color = Vector4D([ 1., 0., 0., 0.5 ])
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
        if event.key == pyscumm.K_SPACE: VM().display.toggle_full_screen()
        return self

    def update( self ):
        pyscumm.scene.SceneState.update(self)
        for obj in self.scene:
            self.scene[obj].rotate( 0.1 )
        return self

pyscumm.vm.boot( Taverna(), Display(), Mouse() )
