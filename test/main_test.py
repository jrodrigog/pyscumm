import sys
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import random
import pyscumm
from pyscumm.scene import Scene, SceneState
from pyscumm.vm import VM
from pyscumm.vector import *
from pyscumm.constant import B_LEFT, B_CENTER, B_RIGHT
from pyscumm.object import Object
from pyscumm.gfx.gl import Display, Image, Texture, Box, Mouse


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

class MyObject:
    JITTER = 15.
    WIDTH  = 50.
    def __init__( self, img ):
        def jitter( x ):
            return x + ( ( random.random() * self.JITTER * 2. ) - self.JITTER )
        self.img = img
        img.collider.visible = True
        img.collider.box[0][0] = jitter( -self.WIDTH ); img.collider.box[0][1] = jitter( -self.WIDTH )
        img.collider.box[1][0] = jitter(  self.WIDTH ); img.collider.box[1][1] = jitter( -self.WIDTH )
        img.collider.box[2][0] = jitter(  self.WIDTH ); img.collider.box[2][1] = jitter(  self.WIDTH )
        img.collider.box[3][0] = jitter( -self.WIDTH ); img.collider.box[3][1] = jitter(  self.WIDTH )
    def collides( self, obj ):
        return self.img.collides( obj )
    def __cmp__( self, obj ):
        return cmp( self.img.location[2], obj.img.location[2] )
    def update( self ):
        self.img.update()
    def draw( self ):
        self.img.draw()

class Taverna( Scene ):
    N = 4
    def start( self ):
        self.state = Taverna1()
        self.dragging = None
        self.offset = None
        self.save_color = None
        self.colored = None
        img = Image( Texture("logo_quad.png" ), Vector3D( [229.,180.,0.] ) )
        img.insertion[0] = img.size[0] / 2.
        img.insertion[1] = img.size[1] / 2.
        for i in xrange( self.N ):
            x = MyObject( img.clone() )
            x.img.updated &= ~pyscumm.constant.SIZE_UPDATED
            #x[ 'img' ].location[0] = random.random() * 640
            #x[ 'img' ].location[1] = random.random() * 320
            x.img.location[0] = random.random() * VM().display.size[0]
            x.img.location[1] = random.random() * VM().display.size[1]
            x.img.location[2] = float( i ) / self.N
            self[ id(x) ] = x

class Taverna1( SceneState ):
    _shared_state = {} # Singleton

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.img.location = event.location - self.scene.offset
        return self

    def on_mouse_button_down( self, event ):
        if event.button != B_LEFT \
            or not event.object: return self
        self.scene.colored = event.object.pop()
        self.scene.save_color = self.scene.colored.img.color
        self.scene.colored.img.color = Vector4D([ 1., 0., 0., 0.5 ])
        return self

    def on_mouse_button_up( self, event ):
        if not self.scene.colored: return self
        self.scene.colored.img.color = self.scene.save_color
        return self

    def on_mouse_drag_start( self, event ):
        if event.button != B_LEFT \
            or not event.object: return self
        # Use the top object
        self.scene.dragging = event.object.pop()
        self.scene.offset = event.location - self.scene.dragging.img.location
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


pyscumm.vm.boot( Taverna(), Display(), Mouse() )
