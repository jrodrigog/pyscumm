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

#!/usr/bin/env python

"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 20/11/2006
"""

import pygame.time, pyscumm.vector
from types import NoneType

class SpeedSolver:
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
        self._location  = pyscumm.vector.Vector3D( [0.,0.,0.] )
        self._insertion = pyscumm.vector.Vector3D( [0.,0.,0.] )
        self._rotation  = pyscumm.vector.Vector4D( [0.,0.,0.,1.] )
        self._color     = pyscumm.vector.Vector4D( [1.,1.,1.,1.] )
        self._scale     = pyscumm.vector.Vector3D( [1.,1.,1.] )
        self._speed     = pyscumm.vector.Vector3D( [0.,0.,0.] )
        self._size      = pyscumm.vector.Vector3D( [0.,0.,0.] )
        self._copy      = self
        self._name      = None
        self._visible   = True
        self._solver    = SpeedSolver()
        self._child     = []

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Drawable()
        # Clone always
        self._location.clone( obj.location, deep )
        self._insertion.clone( obj.insertion, deep )
        self._rotation.clone( obj.rotation, deep )
        self._color.clone( obj.color, deep )
        self._scale.clone( obj.scale, deep )
        self._speed.clone( obj.speed, deep )
        self._size.clone( obj.size, deep )
        # Set
        obj.visible   = self._visible
        if self._copy != self: obj.copy = self._copy
        obj.name      = self.name
        # Deep cloning
        if not deep: obj.child = self._child[:]
        else: obj.child = [
            i.clone( deep = True ) for i in self._child ]
        return obj

    def get_visible( self ): return self._visible
    def set_visible( self, visible ): self._visible = visible
    def get_name( self ): return self._name
    def set_name( self, name ): self._name = name
    def get_color( self ): return self._color
    def set_color( self, color ): self._color = color
    def get_rotation( self ): return self._rotation
    def set_rotation( self, rotation ): self._rotation = rotation        
    def get_insertion( self ): return self._insertion
    def set_insertion( self, insertion ): self._insertion = insertion
    def get_location( self ): return self._location
    def set_location( self, location ): self._location = location
    def get_scale( self ): return self._scale
    def set_scale( self, scale ): self._scale = scale
    def get_speed( self ): return self._speed
    def set_speed( self, speed ): self._speed = speed
    def get_solver( self ): return self._solver
    def set_solver( self, solver ): self._solver = solver
    def get_size( self ): return self._size
    def set_size( self, size ): self._size = size

    def set_child( self, child ): self._child = child
    def get_child( self ): return self._child
    def set_copy( self, copy ): self._copy = copy
    def get_copy( self ): return self._copy
    def clear_copy( self ): self._copy = self

    def set_rgb( self, rgb ):
        self._color[0] = rgb[0]
        self._color[1] = rgb[1]
        self._color[2] = rgb[2]
    def get_rgb( self ):
        return self._color[:-1]

    def get_alpha( self ): return self._color[3]
    def set_alpha( self, alpha ): self._color[3] = alpha

    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Drawable()
        obj.name = element.getAttribute("name")
        tmp = element.getElementsByTagName( "Location" )
        if len( tmp ): obj.location = pyscumm.vector.Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Insertion" )
        if len( tmp ): obj.insertion = pyscumm.vector.Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Color" )
        if len( tmp ): obj.color = pyscumm.vector.Vector4D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Rotation" )
        if len( tmp ): obj.rotation = pyscumm.vector.Vector4D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Scale" )
        if len( tmp ): obj.scale = pyscumm.vector.Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Speed" )
        if len( tmp ): obj.speed = pyscumm.vector.Vector3D.deserialize( tmp.item( 0 ) )
        tmp = element.getElementsByTagName( "Size" )
        if len( tmp ): obj.size = pyscumm.vector.Vector3D.deserialize( tmp.item( 0 ) )
        return obj

    def draw( self ):
        """Draw the object"""
        raise NotImplementedError

    def update( self ):
        """Update the object"""
        self._solver.solve( self )
        for child in self._child: child.update()

    child     = property( get_child, set_child )
    name      = property( get_name, set_name )
    speed     = property( get_speed, set_speed )
    copy      = property( get_copy, set_copy )
    color     = property( get_color, set_color )
    rotation  = property( get_rotation, set_rotation )
    scale     = property( get_scale, set_scale )
    insertion = property( get_insertion, set_insertion )
    location  = property( get_location, set_location )
    rgb       = property( get_rgb, set_rgb )
    alpha     = property( get_alpha, set_alpha )
    visible   = property( get_visible, set_visible )
    solver    = property( get_solver, set_solver )
    size      = property( get_size, set_size )
    deserialize = classmethod( deserialize )

class Cycle( object ):
    """An abstract Cycle"""
    def __init__( self ):
        """Build the object"""
        # Start time of the cycle
        self._start_time = 0
        # Is the cycle started?
        self._started = False
        # Time span of the cycle
        self._time = 1000
        # Is the cycle looping?
        self._loop = False
        # Is the cycle a ping pong?
        self._ping_pong = True
        # Cycle direction
        self._direction = False
        # Is it Paused
        self._paused = False
        # Elapsed time since the start
        self._elapsed_time = 0
        # Las modulo time
        self._last_modulo = -1

    def clone( self, obj=None, deep=False ):
        """Clone this object, create a new one if required"""
        if isinstance( obj, NoneType ): obj = Cycle() 
        obj.started      = self._started
        obj.time         = self._time
        obj.loop         = self._loop
        obj.ping_pong    = self._ping_pong
        obj.direction    = self._direction
        obj.paused       = self._paused
        obj.start_time   = self._start_time
        obj.elapsed_time = self._elapsed_time
        obj.last_modulo  = self._last_modulo
        return obj

    def get_last_modulo( self ): return self._last_modulo
    def set_last_modulo( self, last_modulo ): self._last_modulo = last_modulo
    def get_started( self ): return self._started
    def set_started( self, started ): self._started = started
    def get_time( self ): return self._time
    def get_paused( self ): return self._paused
    def set_paused( self, paused ): self._paused = paused
    def get_start_time( self ): return self._start_time
    def set_start_time( self, start_time ): self._start_time = start_time
    def get_elapsed_time( self ): return self._elapsed_time
    def set_elapsed_time( self, elapsed_time ): self._elapsed_time = elapsed_time
    def get_loop( self ): return self._loop
    def set_loop( self, loop ): self._loop = loop
    def get_ping_pong( self ): return self._ping_pong
    def set_ping_pong( self, ping_pong ): self._ping_pong = ping_pong
    def get_direction( self ): return self._direction
    def set_direction( self, direction ): self._direction = direction
    def get_time( self ): return self._time
    def set_time( self, time ): self._time = time

    def pause( self ):
        """Pause the cycle"""
        self._paused = True

    def resume( self ):
        """Resume the cycle"""
        self._start_time = pygame.time.get_ticks()
        self._paused = False

    def update( self ):
        """Update the cycle"""
        if self._paused or not self._started: return
        self._elapsed_time = pygame.time.get_ticks() - self._start_time
        m = ( self._elapsed_time % self._time )
        if m < self._last_modulo:
            self.ending()
        self._last_modulo = m

    def start( self ):
        """Start the cycle"""
        self._started = True
        self._start_time = pygame.time.get_ticks()
        self._last_modulo = -1
        self.update()
        Cycle.update( self )

    def stop( self ):
        """Stop the cycle"""
        self._started = False
        self._start_time = 0

    def get_elapsed_time( self ):
        """Get the cycling elapsed_time time"""
        return self._elapsed_time

    def ending( self ):
        """The cycle ended, reset it"""
        if self._ping_pong: self.reverse()
        elif self._loop: pass
        else: self.stop()

    def reverse( self ):
        """Reverse the cycle direction"""
        self._direction = not self._direction

    def forward( self ):
        """Reset the cycle direction to normal"""
        direction = False

    def backwards( self ):
        """Reset the cycle direction to normal"""
        direction = True

    def deserialize( self, element, obj=None ):
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

    time      = property( get_time, set_time )
    loop      = property( get_loop, set_loop )
    ping_pong = property( get_ping_pong, set_ping_pong )
    direction = property( get_direction, set_direction )
    started   = property( get_started, set_started )
    paused    = property( get_paused, set_paused )

    last_modulo  = property( get_last_modulo, set_last_modulo )
    elapsed_time = property( get_elapsed_time, set_elapsed_time )
    start_time   = property( get_start_time, set_start_time )

    deserialize = classmethod( deserialize )


class Animation( Cycle ):
    """An abstract Animation that provides a frame counter"""
    def __init__( self, reset=0, end=0, fps=30. ):
        Cycle.__init__( self )
        self._frame = 0
        self._reset = reset
        self._end   = end
        self.fps    = fps
        self._last_frame = 0
        self.build()

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Animation()
        Cycle.clone( self, obj, deep )
        obj.reset = self._reset
        obj.end   = self._end
        obj.fps   = self._fps
        obj.frame = self._frame
        obj.last_frame = self._last_frame
        obj.build()
        return obj

    def clear( self ): pass
    def build( self ):
        self._length = self._end - self._reset
        self._time = self._ani_speed * ( self._length + 1 )

    def get_length( self ): return self._length
    def get_frame( self ): return self._frame

    def get_fps( self ): return self._fps
    def set_fps( self, fps ):
        self._fps = fps
        self._ani_speed = 1000. / fps

    def get_ani_speed( self ): return self._ani_speed
    def set_ani_speed( self, speed ): self._ani_speed = ani_speed

    def get_last_frame( self ): return self._last_frame
    def set_last_frame( self, speed ): self._last_frame = last_frame    

    def get_reset( self ): return self._reset
    def set_reset( self, reset ):
        self._reset = reset
        self.build()
    def get_end( self ): return self._end
    def set_end( self, end ):
        self._end = end
        self.build()

    def start( self ):
        """Start the animation"""
        Cycle.start( self )
        self._last_frame = 0

    def get_frame( self ): return self._frame

    def update( self ):
        """Update the frame here"""
        Cycle.update( self )
        t = self.elapsed_time
        if ( t - self._last_frame ) >= self._ani_speed:
            self._last_frame = t
            self._frame = ( self._frame + 1 ) % self._length
        if self.direction: self._frame = self._reset + self._frame
        else: self._frame = self._end - self._frame

    def deserialize( self, element, obj=None ):
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
    length = property( get_length )
    last_frame = property( get_last_frame, set_last_frame )
    deserialize = classmethod( deserialize )

