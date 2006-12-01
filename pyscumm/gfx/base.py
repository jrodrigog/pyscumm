#    PySCUMM Engine. SCUMM based engine for Python
#    Copyright (C) 2006  PySCUMM Engine. http://pyscumm.org
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 20/11/2006
"""

from types import NoneType
import pygame.time
from pyscumm.vector import Vector3D, Vector4D
from pyscumm.box import Collider

class SpeedSolver( object ):
    """A Singleton Speed Solver"""

    _shared_state = {}

    def __init__( self ):
        self.__dict__ = self._shared_state

    def solve( self, obj ):
        """Solve the object's location based on its speed."""
        obj.location += obj.speed


class Drawable( object ):
    """Abstract Drawable object; contains the location,
    insertion, rotation, color and scale of the object"""

    def __init__( self ):
        self.location  = Vector3D( [0.,0.,0.] )
        self.insertion = Vector3D( [0.,0.,0.] )
        self.rotation  = Vector4D( [0.,0.,0.,1.] )
        self.color     = Vector4D( [1.,1.,1.,1.] )
        self.scale     = Vector3D( [1.,1.,1.] )
        self.speed     = Vector3D( [0.,0.,0.] )
        self.size      = None
        self.collider  = None
        self.copy      = self
        self.name      = None
        self.visible   = True
        self.solver    = SpeedSolver()
        self.child     = []

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Drawable()
        # Clone always
        self.location.clone( obj.location, deep )
        self.insertion.clone( obj.insertion, deep )
        self.rotation.clone( obj.rotation, deep )
        self.color.clone( obj.color, deep )
        self.scale.clone( obj.scale, deep )
        self.speed.clone( obj.speed, deep )
        if not isinstance( self.size, NoneType ):
            self.size.clone( obj.size, deep )
        if not isinstance( self.collider, NoneType ):
            obj.collider = self.collider.clone( deep=deep )
            obj.collider.copy = obj
        # Set
        obj.visible   = self.visible
        if self.copy != self: obj.copy = self.copy
        obj.name      = self.name
        # Deep cloning
        if not deep: obj.child = self.child[:]
        else: obj.child = [
            i.clone( deep = True ) for i in self.child ]
        return obj

    def rotate(self, angle):
        self.rotation[0] += angle
    def flip( self, axis ):
        if axis == "x" or axis == 0: self.scale[0] *= -1
        elif axis == "y" or axis == 1: self.scale[1] *= -1
        elif axis == "z" or axis == 2: self.scale[2] *= -1

    def clear_copy( self ): self.copy = self

    def set_rgb( self, rgb ):
        self.color[0] = rgb[0]
        self.color[1] = rgb[1]
        self.color[2] = rgb[2]
    def get_rgb( self ):
        return self.color[:-1]

    def get_alpha( self ): return self.color[3]
    def set_alpha( self, alpha ): self.color[3] = alpha

    @classmethod
    def deserialize( cls, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Drawable()
        obj.name = element.getAttribute("name")
        tmp = element.getElementsByTagName( "Location" )
        if len( tmp ): obj.location = Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Insertion" )
        if len( tmp ): obj.insertion = Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Color" )
        if len( tmp ): obj.color = Vector4D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Rotation" )
        if len( tmp ): obj.rotation = Vector4D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Scale" )
        if len( tmp ): obj.scale = Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Speed" )
        if len( tmp ): obj.speed = Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Size" )
        if len( tmp ): obj.size = Vector3D.deserialize( tmp.item( 0 ) )
        return obj

    def collides( self, obj ):
        if isinstance( obj, Collider ):
            return self.collider.collides( obj )
        elif self.collider:
            return self.collider.collides( obj.collider )
        return None

    def draw( self ):
        """Draw the object"""
        raise NotImplementedError

    def update( self ):
        """Update the object"""
        self.solver.solve( self )
        for child in self.child: child.update()

    rgb       = property( get_rgb, set_rgb )
    alpha     = property( get_alpha, set_alpha )

class Cycle( object ):
    """An abstract Cycle"""

    def __init__( self ):
        """Build the object"""
        # Start time of the cycle
        self.start_time = 0
        # Is the cycle started?
        self.started = False
        # Time span of the cycle
        self.time = 1000
        # Is the cycle looping?
        self.loop = False
        # Is the cycle a ping pong?
        self.ping_pong = True
        # Cycle direction
        self.direction = False
        # Is it Paused
        self.paused = False
        # Elapsed time since the start
        self.elapsed_time = 0
        # Las modulo time
        self.last_modulo = -1

    def clone( self, obj=None, deep=False ):
        """Clone this object, create a new one if required"""
        if isinstance( obj, NoneType ): obj = Cycle()
        obj.started      = self.started
        obj.time         = self.time
        obj.loop         = self.loop
        obj.ping_pong    = self.ping_pong
        obj.direction    = self.direction
        obj.paused       = self.paused
        obj.start_time   = self.start_time
        obj.elapsed_time = self.elapsed_time
        obj.last_modulo  = self.last_modulo
        return obj

    def pause( self ):
        """Pause the cycle"""
        self.paused = True

    def resume( self ):
        """Resume the cycle"""
        self.start_time = pygame.time.get_ticks()
        self.paused = False

    def update( self ):
        """Update the cycle"""
        if self.paused or not self.started: return
        self.elapsed_time = pygame.time.get_ticks() - self.start_time
        m = ( self.elapsed_time % self.time )
        if m < self.last_modulo:
            self.ending()
        self.last_modulo = m

    def start( self ):
        """Start the cycle"""
        self.started = True
        self.start_time = pygame.time.get_ticks()
        self.last_modulo = -1
        self.update()
        Cycle.update( self )

    def stop( self ):
        """Stop the cycle"""
        self.started = False
        self.start_time = 0

    def ending( self ):
        """The cycle ended, reset it"""
        if self.ping_pong: self.reverse()
        elif self.loop: pass
        else: self.stop()

    def reverse( self ):
        """Reverse the cycle direction"""
        self.direction = not self.direction

    def forward( self ):
        """Reset the cycle direction to normal"""
        direction = False

    def backwards( self ):
        """Reset the cycle direction to normal"""
        direction = True

    @classmethod
    def deserialize( cls, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Cycle()
        tmp = element.getAttribute("time")
        if tmp: obj.time = float( tmp )
        tmp = element.getAttribute("loop")
        if tmp: obj.loop = bool( int( tmp ) )
        tmp = element.getAttribute("ping_pong")
        if tmp: obj.ping_pong = bool( int( tmp ) )
        tmp = element.getAttribute("direction")
        if tmp: obj.direction = bool( int( tmp ) )
        return obj


class Animation( Cycle ):
    """An abstract Animation that provides a frame counter"""
    def __init__( self, reset=0, end=0, fps=30. ):
        Cycle.__init__( self )
        self.frame = 0
        self.reset = reset
        self.end   = end
        self.fps    = fps
        self.last_frame = 0
        self.build()

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Animation()
        Cycle.clone( self, obj, deep )
        obj.reset = self.reset
        obj.end   = self.end
        obj.fps   = self.fps
        obj.frame = self.frame
        obj.last_frame = self.last_frame
        obj.build()
        return obj

    def clear( self ): pass
    def build( self ):
        self.length = self.end - self.reset
        self.time = self.ani_speed * ( self.length + 1 )

    def get_fps( self ): return self.fps
    def set_fps( self, fps ):
        self.fps = fps
        self.ani_speed = 1000. / fps

    def get_reset( self ): return self.reset
    def set_reset( self, reset ):
        self.reset = reset
        self.build()
    def get_end( self ): return self.end
    def set_end( self, end ):
        self.end = end
        self.build()

    def start( self ):
        """Start the animation"""
        Cycle.start( self )
        self.last_frame = 0

    def get_frame( self ): return self.frame

    def update( self ):
        """Update the frame here"""
        Cycle.update( self )
        t = self.elapsed_time
        if ( t - self.last_frame ) >= self.ani_speed:
            self.last_frame = t
            self.frame = ( self.frame + 1 ) % self.length
        if self.direction: self.frame = self.reset + self.frame
        else: self.frame = self.end - self.frame

    @classmethod
    def deserialize( cls, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Animation()
        Cycle.deserialize( element, obj )
        tmp = element.getAttribute("reset")
        if tmp: obj.reset = int( tmp )
        tmp = element.getAttribute("end")
        if tmp: obj.end = int( tmp )
        tmp = element.getAttribute("fps")
        if tmp: obj.fps = float( tmp )
        obj.build()
        return obj

    reset  = property( get_reset, set_reset )
    end    = property( get_end, set_end )
    fps    = property( get_fps, set_fps )
    frame  = property( get_frame )

