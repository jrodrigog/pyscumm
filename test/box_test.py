import sys, math
sys.path[len(sys.path):len(sys.path)+1] = ('.', '..')

import pyscumm, random, pyscumm.gfx.gl

class MyObject( pyscumm.object.Object ):
    count  = 0
    JITTER = 15.
    WIDTH  = 50.
    def __init__( self ):
        def jitter( x ):
            return x + ( ( random.random() * self.JITTER * 2. ) - self.JITTER )
        self._box = pyscumm.gfx.gl.Box()
        self._box.box[0][0] = jitter( -self.WIDTH ); self._box.box[0][1] = jitter( -self.WIDTH )
        self._box.box[1][0] = jitter(  self.WIDTH ); self._box.box[1][1] = jitter( -self.WIDTH )
        self._box.box[2][0] = jitter(  self.WIDTH ); self._box.box[2][1] = jitter(  self.WIDTH )
        self._box.box[3][0] = jitter( -self.WIDTH ); self._box.box[3][1] = jitter(  self.WIDTH )
        self["id"] = self.__class__.count
        self.__class__.count += 1
    def draw( self ):
        self._box.draw()
    def collides( self, obj ):
        return self._box.collides( obj )
    def __cmp__( self, obj ):
        return cmp( self._box.location[2], obj.box.location[2] )
    def get_box( self ): return self._box
    box = property( get_box )

class Taverna( pyscumm.scene.Scene ):
    def __init__( self ):
        pyscumm.scene.Scene.__init__( self )
    N = 16
    def start( self ):
        self._state = Taverna1()
        self._dragging = None
        self._offset = None
        self._save_color = None
        self._colored = None
        self._rotation = 0.
        for i in xrange( self.N ):
            x = MyObject()
            #x[ 'box' ].location[0] = random.random() * 640
            #x[ 'box' ].location[1] = random.random() * 320
            x.box.location[0] = random.random() * pyscumm.vm.VM().display.size[0]
            x.box.location[1] = random.random() * pyscumm.vm.VM().display.size[1]
            x.box.location[2] = float( i ) / self.N
            x.box.update()
            self[ id(x) ] = x
    def get_save_color( self ): return self._save_color
    def set_save_color( self, save_color ): self._save_color = save_color
    def get_dragging( self ): return self._dragging
    def set_dragging( self, dragging ): self._dragging = dragging
    def get_offset( self ): return self._offset
    def set_offset( self, offset ): self._offset = offset
    def get_colored( self ): return self._colored
    def set_colored( self, colored ): self._colored = colored
    def get_rotation( self ): return self._rotation
    def set_rotation( self, rotation ): self._rotation = rotation

    save_color = property( get_save_color, set_save_color )
    dragging   = property( get_dragging, set_dragging )
    offset     = property( get_offset, set_offset )
    colored    = property( get_colored, set_colored )
    rotation   = property( get_rotation, set_rotation )

class Taverna1( pyscumm.scene.SceneState ):
    _shared_state = {} # Singleton
    ROT_SPEED = 1.
    MAX_INSERTION = 30.
    MAX_SCALE = 1.
    def __init__( self ):
        self.__dict__ = self._shared_state
        if self.__dict__: return
        pyscumm.scene.SceneState.__init__( self )

    def on_mouse_motion( self, event ):
        if not self.scene.dragging: return self
        self.scene.dragging.box.location = event.location - self.scene.offset
        self.scene.dragging.box.update()
        return self

    def on_mouse_button_down( self, event ):
        if event.button != pyscumm.B_LEFT \
            or not event.object: return self
        self.scene.colored = event.object.pop()
        self.scene.save_color = self.scene.colored.box.color
        self.scene.colored.box.color = pyscumm.vector.Vector4D([ 1., 0., 0., 0.5 ])
        self.scene.colored.box.update()
        return self

    def on_mouse_button_up( self, event ):
        if not self.scene.colored: return self
        self.scene.colored.box.color = self.scene.save_color
        self.scene.colored.box.update()
        return self

    def on_mouse_drag_start( self, event ):
        if event.button != pyscumm.B_LEFT \
            or not event.object: return self
        # Use the top object
        self.scene.dragging = event.object.pop()
        self.scene.offset = event.location - self.scene.dragging.box.location
        #pyscumm.base.Logger().info( "fps: %.2f" % self.vm.clock.fps )
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

    def update( self ):
        t = self.vm.clock.time / 1000.
        cos = math.cos( t )
        sin = math.sin( t )
        insertion = pyscumm.vector.Vector3D( [
            cos * self.MAX_INSERTION,
            sin * self.MAX_INSERTION,
            0. ] )
        scale = pyscumm.vector.Vector3D( [
            (((cos+1.)/2.)+1.) * self.MAX_SCALE,
            (((sin+1.)/2.)+1.) * self.MAX_SCALE,
            0. ] )
        for obj in self.scene.sorted:
            obj.box.insertion = insertion
            obj.box.scale = scale
            obj.box.rotation[0] += self.ROT_SPEED
            obj.box.update()
        #pyscumm.scene.SceneState.update( self )
        return self


pyscumm.vm.VM.boot( Taverna(), pyscumm.gfx.gl.Display() )
