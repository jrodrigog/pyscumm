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
JITTER = 50.
class MyObject:
    def __init__( self, img ):
        def jitter():
            return ( random.random() * JITTER * 2. ) - JITTER
        self.img = img
        img.collider.visible = True
        img.collider.init()
        img.collider.box[0][0] += jitter(); img.collider.box[0][1] += jitter()
        img.collider.box[1][0] += jitter(); img.collider.box[1][1] += jitter()
        img.collider.box[2][0] += jitter(); img.collider.box[2][1] += jitter()
        img.collider.box[3][0] += jitter(); img.collider.box[3][1] += jitter()
        img.location[0] = random.random() * VM().display.size[0]
        img.location[1] = random.random() * VM().display.size[1]
        # Mid point, add all the vectors and divide by n
        img.insertion = reduce( lambda x,y: x+y, img.collider.box, Vector3D() ).scale( -1. / 4. )

        img.updated &= ~pyscumm.SIZE_UPDATED
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
        self.rot_dir = -1.
        self.button = 0
        img = Image( Texture("logo_quad.png" ), Vector3D( [229.,180.,0.] ) )
        #img.insertion[0] = -img.size[0] / 2.
        #img.insertion[1] = -img.size[1] / 2.
        for i in xrange( self.N ):
            x = MyObject( img.clone() )
            #x.img.updated &= ~pyscumm.constant.SIZE_UPDATED
            #x[ 'img' ].location[0] = random.random() * 640
            #x[ 'img' ].location[1] = random.random() * 320
            x.img.location[2] = float( i ) / self.N
            self[ id(x) ] = x

ROT_SPEED = 2.0
class Taverna1( SceneState ):
    _shared_state = {} # Singleton

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.location = event.location - self.scene.offset
        return self

    def on_mouse_button_down( self, event ):
        if event.button == B_CENTER \
            or not event.object or self.scene.dragging: return self
        if event.button == B_LEFT: self.scene.rot_dir = -1.
        elif event.button == B_RIGHT: self.scene.rot_dir = +1.
        self.scene.dragging = event.object.pop().img
        self.scene.offset = event.location - self.scene.dragging.location
        self.scene.colored = self.scene.dragging.collider
        self.scene.save_color = self.scene.colored.color
        self.scene.colored.color = Vector4D([ 1., 0., 0., 0.5 ])
        self.button = event.button 
        return self

    def on_mouse_button_up( self, event ):
        if not self.scene.colored or event.button != self.button: return self
        self.scene.colored.color = self.scene.save_color
        self.scene.dragging = None
        return self

    def on_mouse_drag_start( self, event ):
        if event.button == B_CENTER \
            or not event.object: return self
        # Use the top object
        self.scene.offset = event.location - self.scene.dragging.location
        return self

    def on_mouse_drag_end( self, event ):
        print VM().clock.fps
        return self

    def update( self ):
        if self.scene.dragging: 
            self.scene.dragging.rotation[0] += ( self.scene.rot_dir * ROT_SPEED )
        SceneState.update( self )
        return self


pyscumm.vm.boot( Taverna(), Display(), Mouse() )
