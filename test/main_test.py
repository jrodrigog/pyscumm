import sys
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import random
import pyscumm
from pyscumm.scene import Scene, SceneState
from pyscumm.gfx.gl import Display, Image, Texture
from pyscumm.vm import VM
from pyscumm.vector import *
from pyscumm.constant import B_LEFT, B_CENTER, B_RIGHT
from pyscumm.object import Object
from pyscumm.gfx.gl import Box


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

class MyObject( Object ):
    count  = 0
    JITTER = 15.
    WIDTH  = 50.
    def __init__( self ):
        def jitter( x ):
            return x + ( ( random.random() * self.JITTER * 2. ) - self.JITTER )
        self.box = Box()
        self.box.box[0][0] = jitter( -self.WIDTH ); self.box.box[0][1] = jitter( -self.WIDTH )
        self.box.box[1][0] = jitter(  self.WIDTH ); self.box.box[1][1] = jitter( -self.WIDTH )
        self.box.box[2][0] = jitter(  self.WIDTH ); self.box.box[2][1] = jitter(  self.WIDTH )
        self.box.box[3][0] = jitter( -self.WIDTH ); self.box.box[3][1] = jitter(  self.WIDTH )
        self["id"] = self.__class__.count
        self.__class__.count += 1
    def draw( self ):
        self.box.draw()
    def collides( self, obj ):
        return self.box.collides( obj )
    def __cmp__( self, obj ):
        return cmp( self.box.location[2], obj.box.location[2] )

class Taverna( Scene ):
    N = 16
    def start( self ):
        self.state = Taverna1()
        self.dragging = None
        self.offset = None
        self.save_color = None
        self.colored = None
        for i in xrange( self.N ):
            x = MyObject()
            #x[ 'box' ].location[0] = random.random() * 640
            #x[ 'box' ].location[1] = random.random() * 320
            x.box.location[0] = random.random() * VM().display.size[0]
            x.box.location[1] = random.random() * VM().display.size[1]
            x.box.location[2] = float( i ) / self.N
            x.box.update()
            self[ id(x) ] = x

class Taverna1( SceneState ):
    _shared_state = {} # Singleton

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.box.location = event.location - self.scene.offset
        self.scene.dragging.box.update()
        return self

    def on_mouse_button_down( self, event ):
        if event.button != B_LEFT \
            or not event.object: return self
        self.scene.colored = event.object.pop()
        self.scene.save_color = self.scene.colored.box.color
        self.scene.colored.box.color = Vector4D([ 1., 0., 0., 0.5 ])
        self.scene.colored.box.update()
        return self

    def on_mouse_button_up( self, event ):
        if not self.scene.colored: return self
        self.scene.colored.box.color = self.scene.save_color
        self.scene.colored.box.update()
        return self

    def on_mouse_drag_start( self, event ):
        if event.button != B_LEFT \
            or not event.object: return self
        # Use the top object
        self.scene.dragging = event.object.pop()
        self.scene.offset = event.location - self.scene.dragging.box.location
        return self

    def on_mouse_drag_end( self, event ):
        print VM().clock.fps
        if event.button != B_LEFT \
            or not self.scene.dragging: return self
        self.scene.dragging = None
        return self

    def on_mouse_click( self, event ):
        if event.button != B_RIGHT: return self
        raise pyscumm.vm.StopVM()
        return self


pyscumm.vm.boot( Taverna(), Display() )
