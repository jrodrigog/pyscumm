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
@since: 8/11/2006
"""

from types import NoneType
import pygame.event, base, driver, vector

class ChangeScene( Exception ):
    """
    Change the VM's activa escene. You can raise this
    exception anytime and give a new scene to the VM.
    raise ChangeScene( MyScene() ), the VM will take
    care of calling the scene stop and start method's.
    """
    def __init__( self, scene ):
        """
        Init's the ChangeScene exception, takes one
        parameter the new active Scene.
        @param scene: The VM's active scene
        @type scene: Scene
        """
        self._scene = scene

    def get_scene( self ):
        """
        Get the Scene.
        @return: Scene
        """
        return self._scene

    scene = property( get_scene )


class StopVM( Exception ):
    """This exception halts the VM, completely stopping it."""
    pass


class VM( base.StateMachine ):
    """
    VM (Virtual Machine) its a state machine (See state pattern), its the core of pyscumm,
    this haddle PyGame events, draw each drawable object depends of her Zplanes, etc
    This VM  recollect the low-level events (see main() method) and launch it to the active state
    in same method, update and draw each element of the game.

    PySCUMM have built-in some pre-mades VMStates..., the VMStates, are states of VM, these wants
    complex algorithms sometimes are unnecessary depending of the types of events that requires
    in your game on this momment.

    PySCUMM include pre-mades states:

            - vm.PassiveMode: This state ignore all events type.
            - vm.NormalMode: This state launch all events type to Game class.
            - vm.KeyMode: This state only launch keyboard events to Game class.
            - vm.MouseMode: This state only launch mouse events to Game class.
            - vm.DialogMode: This state only launch mouse events to HUD class.
    """
    # Singleton's shared state
    _shared_state = {}
    def __init__( self ):
        """
        Construct the Virtual Machine object saving some instances of components in private attributes.
        this objects are statics, if one of this argument dont is passed, or already exist a instance of this,
        this argument will be a new instance of the object.
        @param scene: a Scene instance.
        @type scene: scene.Scene
        @param clock: a Clock instance.
        @type clock: game.Clock
        @param display: a Display instance.
        @type display: game.Display
        @param mouse: a Mouse instance.
        @type mouse: game.Mouse
        """
        self.__dict__ = self._shared_state
        if self._shared_state: return
        base.StateMachine.__init__( self )
        self._mouse = driver.Mouse()
        self._display = driver.GLDisplay()
        self._clock = driver.Clock()
        self._scene = None

    def quit( self ):
        """Report to the active state a quit event."""
        self._state = self._state.on_quit()

    def keyboard_pressed( self, event ):
        """
        Report to the active state a keyboard key pressed.
        @param event: A Pygame KEYDOWN event
        @type event: Event(PyGame)
        """
        self._state = self._state.keyboard_pressed( event )

    def keyboard_released( self, event ):
        """
        Report to the active state a keyboard key pressed.
        @param event: A Pygame KEYUP event
        @type event: Event(PyGame)
        """
        self._state = self._state.keyboard_released( event )

    def mouse_pressed( self, event ):
        """
        Report to the active state a mouse button pressed.
        @param event: A Pygame MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        self._state = self._state.mouse_pressed( event )

    def mouse_released( self, event ):
        """
        Report to the active state a mouse button released.
        @param event: A Pygame MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        self._state = self._state.mouse_released( event )

    def update( self ):
        """Send an update message to the active scene."""
        self._state.update()

    def draw( self ):
        """Send an update message to the active scene."""
        self._state.draw()

    def start( self ):
        """Reset the VM with the vm.NormalMode state."""
        self._state = NormalMode()

    def main( self ):
        """
        Init the main loop of the engine, open a display window, launch events to the
        active state, update and render the scene each frame. if StopScene exception is launched,
        the VM stop self, and close the window.If however SceneChange exception is launched,
        the VM will reset single with the new scene data without close the window.
        """
        self.start()
        self._display.open()
        self._scene.start()
        leave = False
        while not leave:
            try:
                self._clock.tick()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit()
                    elif event.type == pygame.KEYDOWN:
                        self.keyboard_pressed( event )
                    elif event.type == pygame.KEYUP:
                        self.keyboard_released( event )
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_pressed( event )
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_released( event )
                self.update()
                self.draw()
            except ChangeScene, e:
                self._scene.stop()
                self._scene = e.scene
                self._scene.start()
            except StopVM:
                leave = True
        self._display.close()

    def boot( self, scene, clock=None, display=None, mouse=None  ):
        """
        Boot a scene. Prepare a Virtual Machine and
        start running the main loop.
        """
        if not isinstance( clock, NoneType ): VM().clock = clock
        if not isinstance( display, NoneType ): VM().display = display
        if not isinstance( mouse, NoneType ): VM().mouse = mouse
        VM().scene = scene
        VM().main()

    def get_clock( self ):
        """
        Get the VM's clock.
        @return: A Clock object
        @rtype: Clock
        """
        return self._clock

    def set_clock( self, clock ):
        """
        Set the VM's clock.
        @param clock: A Clock object
        @type clock: Clock
        """
        self._clock = clock

    def get_display( self ):
        """
        Get the VM's display.
        @return: A Display object
        @rtype: Display
        """
        return self._display

    def set_display( self, display ):
        """
        Set the VM's display.
        @param display: A Display object
        @type display: Display
        """
        self._display = display

    def get_mouse( self ):
        """
        Get the VM's mouse.
        @return: A Mouse object
        @rtype: Mouse
        """
        return self._mouse

    def set_mouse( self, mouse ):
        """
        Set the VM's mouse.
        @param mouse: A Mouse object
        @type mouse: Mouse
        """
        self._mouse = mouse

    def get_scene( self ):
        """
        Get the VM's Scene.
        @return: A Scene object
        @rtype: Scene
        """
        return self._scene

    def set_scene( self, scene ):
        """
        Set the VM's Scene.
        @param scene: A Scene object
        @type scene: Scene
        """
        self._scene = scene

    scene   = property( get_scene, set_scene )
    mouse   = property( get_mouse, set_mouse )
    display = property( get_display, set_display )
    clock   = property( get_clock, set_clock )
    boot    = classmethod( boot )


class VMState( base.State ):
    """
    This class is a abstract state of the VM, the pre-mades modes of VM inherit from 
    this class. You can inherit it to write your own modes (states).
    VMState recieves the calls of the VM (Pygame events), transforms and process them to
    check if was a click, a doubleclick, a key pressed, key released, etc..., check if 
    the mouse collides with any object, and depending of the VMState setted on VM, 
    will launch high-level events to the scene instance.
    """

    def __init__( self ):
        base.State.__init__( self )

    def on_quit( self ):
        VM().scene.on_quit()
        return self

    def keyboard_pressed( self, event ):
        raise NotImplementedError

    def keyboard_released( self, event ):
        raise NotImplementedError

    def mouse_pressed( self, event ):
        raise NotImplementedError

    def mouse_released( self, event ):
        raise NotImplementedError

    def update( self ):
        VM().scene.update()
        return self

    def draw( self ):
        VM().scene.draw()
        return self


class NormalMode( VMState ):

    BTN_PRESS_LEFT   = 1<<1
    BTN_PRESS_CENTER = 1<<2
    BTN_PRESS_RIGHT  = 1<<3

    BTN_CLICK_LEFT   = 1<<5
    BTN_CLICK_CENTER = 1<<6
    BTN_CLICK_RIGHT  = 1<<7

    BTN_DRAG_LEFT    = 1<<9
    BTN_DRAG_CENTER  = 1<<10
    BTN_DRAG_RIGHT   = 1<<11

    BTN_LEFT   = 1
    BTN_CENTER = 2
    BTN_RIGHT  = 3

    def __init__( self ):
        VMState.__init__( self )
        self._flag = 0
        self._time = [ None ] * 4
        self._drag = [ None ] * 4
        self._loc  = vector.Vector3D()

    def keyboard_pressed( self, event ):
        VM().scene.on_key_down( event )
        return self

    def keyboard_released( self, event ):
        VM().scene.on_key_up( event )
        return self

    def mouse_pressed( self, event ):
        if event.button == self.BTN_LEFT:
            self._flag |= self.BTN_PRESS_LEFT
            self._drag[ self.BTN_LEFT ] = VM().mouse.location
        elif event.button == self.BTN_CENTER:
            self._flag |= self.BTN_PRESS_CENTER
            self._drag[ self.BTN_CENTER ] = VM().mouse.location
        elif event.button == self.BTN_RIGHT:
            self._flag |= self.BTN_PRESS_RIGHT
            self._drag[ self.BTN_RIGHT ] = VM().mouse.location
        return self

    def mouse_released( self, event ):
        if event.button == self.BTN_LEFT:
            # Unset the pressed bit
            self._flag &= ~self.BTN_PRESS_LEFT
            # Button clicked?
            if ( self._flag & self.BTN_CLICK_LEFT ) == self.BTN_CLICK_LEFT:
                # Then this is a double click
                self._flag &= ~self.BTN_CLICK_LEFT
                # ... send the event
                VM().scene.on_mouse_double_click( None, self.BTN_LEFT )
            elif ( self._flag & self.BTN_DRAG_LEFT ) != self.BTN_DRAG_LEFT:
                # If it is not, the user has clicked one time
                self._flag |= self.BTN_CLICK_LEFT
                # Start the timer
                self._time[ self.BTN_LEFT ] = VM().clock.time
        elif event.button == self.BTN_CENTER:
            self._flag &= ~self.BTN_PRESS_CENTER
            if ( self._flag & self.BTN_CLICK_CENTER ) == self.BTN_CLICK_CENTER:
                self._flag &= ~self.BTN_CLICK_CENTER
                VM().scene.on_mouse_double_click( None, self.BTN_CENTER )
            elif ( self._flag & self.BTN_DRAG_CENTER ) != self.BTN_DRAG_CENTER:
                self._flag |= self.BTN_CLICK_CENTER
                self._time[ self.BTN_CENTER ] = VM().clock.time
        elif event.button == self.BTN_RIGHT:
            self._flag &= ~self.BTN_PRESS_RIGHT
            if ( self._flag & self.BTN_CLICK_RIGHT ) == self.BTN_CLICK_RIGHT:
                self._flag &= ~self.BTN_CLICK_RIGHT
                VM().scene.on_mouse_double_click( None, self.BTN_RIGHT )
            elif ( self._flag & self.BTN_DRAG_RIGHT ) != self.BTN_DRAG_RIGHT:
                self._flag |= self.BTN_CLICK_RIGHT
                self._time[ self.BTN_RIGHT ] = VM().clock.time
        return self

    def update( self ):
        """Update method, generates drag, click and doubleclick events"""
        # Current mouse location
        location = VM().mouse.location
        # Different position?
        if not ( location == self._loc ):
            # Send a mouse motion event
            VM().scene.on_mouse_motion( self._loc.clone() )
        # Update the mouse position
        self._loc = location

        # Left Button
        # Button pressed?
        if ( self._flag & self.BTN_PRESS_LEFT ) == self.BTN_PRESS_LEFT:
            # Mouse not dragging?, Start a drag? Only after distance_drag pixels moved
            if ( ( self._flag & self.BTN_DRAG_LEFT ) != self.BTN_DRAG_LEFT ) \
            and ( ( self._drag[ self.BTN_LEFT ] - location ).length() > VM().mouse.distance_drag ):
                # Start dragging, set the drag bit
                self._flag |= self.BTN_DRAG_LEFT
                # ... launch an event
                VM().scene.on_mouse_drag_start( None, self.BTN_LEFT )
        # There is no button pressed, Is the mouse dragging?
        elif ( self._flag & self.BTN_DRAG_LEFT ) == self.BTN_DRAG_LEFT:
            # If it is stop dragging, unset the bit
            self._flag &= ~self.BTN_DRAG_LEFT
            # ... and send an event
            VM().scene.on_mouse_drag_end( self.BTN_LEFT )
        # There is no button pressed, was the button clicked?
        elif ( ( self._flag & self.BTN_CLICK_LEFT ) == self.BTN_CLICK_LEFT )\
        and ( ( VM().clock.time - self._time[ self.BTN_LEFT ] ) > VM().mouse.time_double_click ):
            # If it is clicked and the double click timeout expired
            # unset the clicked bit
            self._flag &= ~self.BTN_CLICK_LEFT
            # ... and send a clicked event
            VM().scene.on_mouse_click( None, self.BTN_LEFT )

        # Center Button
        if ( self._flag & self.BTN_PRESS_CENTER ) == self.BTN_PRESS_CENTER:
            if ( ( self._flag & self.BTN_DRAG_CENTER ) != self.BTN_DRAG_CENTER )\
            and ( ( self._drag[ self.BTN_CENTER ] - location ).length() > VM().mouse.distance_drag ):
                self._flag |= self.BTN_DRAG_CENTER
                VM().scene.on_mouse_drag_start( None, self.BTN_CENTER )
        elif ( self._flag & self.BTN_DRAG_CENTER ) == self.BTN_DRAG_CENTER:
            self._flag &= ~self.BTN_DRAG_CENTER
            VM().scene.on_mouse_drag_end( self.BTN_CENTER )
        elif ( ( self._flag & self.BTN_CLICK_CENTER ) == self.BTN_CLICK_CENTER )\
        and ( ( VM().clock.time - self._time[ self.BTN_CENTER ] ) > VM().mouse.time_double_click ):
            self._flag &= ~self.BTN_CLICK_CENTER
            VM().scene.on_mouse_click( None, self.BTN_CENTER )

        # Right Button
        if ( self._flag & self.BTN_PRESS_RIGHT ) == self.BTN_PRESS_RIGHT:
            if ( ( self._flag & self.BTN_DRAG_RIGHT ) != self.BTN_DRAG_RIGHT )\
            and ( ( self._drag[ self.BTN_RIGHT ] - location ).length() > VM().mouse.distance_drag ):
                self._flag |= self.BTN_DRAG_RIGHT
                VM().scene.on_mouse_drag_start( None, self.BTN_RIGHT )
        elif ( self._flag & self.BTN_DRAG_RIGHT ) == self.BTN_DRAG_RIGHT:
            self._flag &= ~self.BTN_DRAG_RIGHT
            VM().scene.on_mouse_drag_end( self.BTN_RIGHT )
        elif ( ( self._flag & self.BTN_CLICK_RIGHT ) == self.BTN_CLICK_RIGHT )\
        and ( ( VM().clock.time - self._time[ self.BTN_RIGHT ] ) > VM().mouse.time_double_click ):
            self._flag &= ~self.BTN_CLICK_RIGHT
            VM().scene.on_mouse_click( None, self.BTN_RIGHT )

        return VMState.update( self )

class PassiveMode( VMState ):
    """
    This state of the VM, ignore all PyGame events, it get the events and it does not do anything with them.
    PassiveMode  is the best VMState option, for game-intros, movie-mode,  and other situations where your scene
    wanna ignore mouse or keyboard events.
    """

    def keyboard_pressed( self, event ):
        """
        PassiveMode ignore all PyGame events.
        @param event: a PyGame KEYDOWN event
        @type event: PyGame Event
        @return: self
        """
        return self

    def keyboard_released( self, event ):
        """
        PassiveMode ignore all PyGame events.
        @param event: a PyGame KEYUP event
        @type event: PyGame Event
        @return: self
        """
        return self

    def mouse_pressed( self, event ):
        """
        PassiveMode ignore all PyGame events.
        @param event: a PyGame MOUSEBUTTONDOWN event
        @type event: PyGame Event
        @return: self
        """
        return self

    def mouse_released( self, event ):
        """
        PassiveMode ignore all PyGame events.
        @param event: a PyGame MOUSEBUTTONUP event
        @type event: PyGame Event
        @return: self
        """
        return self


class KeyMode( NormalMode ):
    """
    This state of the VM, ignore PyGame mouse events, he get the PyGame Mouse events and it dont do anything with them.
    if the event come of a keyboard device, it lauch to scene.

    KeyMode  is the best VMState option where your scene wanna ignore mouse events.
    """

    def mouse_pressed( self, event ):
        """
        KeyMode Ignore mouse events.
        @param event: a PyGame MOUSEBUTTONDOWN event
        @type event: PyGame Event
        @return: self
        """
        return self

    def mouse_released( self, event ):
        """
        KeyMode Ignore mouse events.
        @param event: a PyGame MOUSEBUTTONUP event
        @type event: PyGame Event
        @return: self
        """
        return self



class MouseMode( NormalMode ):
    """
    This mode (state) of the VM, ignore PyGame key events, he get the PyGame key events and it dont do anything with them.
    if the event come of a mouse device, it lauch to scene.

    MouseMode  is the best VMState option where your scene wanna ignore keyboard events.
    """

    def keyboard_pressed( self, event ):
        """
        MouseMode ignore keyboard events.
        @param event: a PyGame KEYDOWN event
        @type event: PyGame Event
        @return: self
        """
        return self

    def keyboard_released( self, event ):
        """
        MouseMode ignore keyboard events.
        @param event: a PyGame KEYUP event
        @type event: PyGame Event
        @return: self
        """
        return self


class DialogMode( MouseMode ):
    """
    This state of the VM, its a little more different that the rest of pre-made states,
    this only capture mouse events, but dont launch it to scene instance, if not to the HUD.

    On this state, the mouse only collide with the visual elements of the dialog interface,
    and ignore collides with actors, objects, etc... only with phrases and other elements of
    the dialog interface.

    The HUD is the class that handdle the visual interface of the dialogs, (see: HUD class)

    MouseMode  is the best VMState option where your scene wanna ignore keyboard events
    and the mouse only must be collide with dialog interface and nots in other objects of the scene.
    """

    def mouse_pressed( self, event ):
        """
        Detect the pressed mouse button,check if collide with any object of the HUD
        and send all info to Dialog.
        @param event: a PyGame MOUSEBUTTONDOWN event
        @type event: PyGame Event
        @return: self
        """
        return self

    def mouse_released( self, event ):
        """
        Detect the released mouse button,check if collide with any object of the HUD
        and send all info to Dialog.
        @param event: a PyGame MOUSEBUTTONUP event
        @type event: PyGame Event
        @return: self
        """
        return self
