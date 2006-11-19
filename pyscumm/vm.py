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
import pygame.event
import base, driver, exception

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
        """
        Report to the active state a quit event.
        @return: None
        """
        self._state = self._state.on_quit()

    def keyboard_pressed( self, event ):
        """
        Report to the active state a keyboard key pressed.

        @param event: a PyGame KEYDOWN event
        @type event: PyGame Event
        @return: None
        """
        self._state = self._state.keyboard_pressed( event )

    def keyboard_released( self, event ):
        """
        Report to the active state a keyboard key pressed.

        @param event: a PyGame KEYUP event
        @type event: PyGame Event
        @return: None
        """
        self._state = self._state.keyboard_released( event )

    def mouse_pressed( self, event ):
        """
        Report to the active state a mouse button pressed.
        @param event: a PyGame MOUSEBUTTONDOWN event
        @type event: PyGame Event
        @return: None
        """
        self._state = self._state.mouse_pressed( event )

    def mouse_released( self, event ):
        """
        Report to the active state a mouse button released.
        @param event: a PyGame MOUSEBUTTONUP event
        @type event: PyGame Event
        @return: None
        """
        self._state = self._state.mouse_released( event )

    def update( self ):
        """
        Send an update message to the active scene.
        @return: None
        """
        self._state.update()

    def draw( self ):
        """
        Send an update message to the active scene.
        @return: None
        """
        self._state.draw()

    def start( self ):
        """
        Reset the VM with the vm.NormalMode state.

        @return: None
        """
        self._state = NormalMode()

    def main( self ):
        """
        Init the main loop of the engine, open a display window, launch events to the
        active state, update and render the scene each frame. if StopScene exception is launched,
        the VM stop self, and close the window.If however SceneChange exception is launched,
        the VM will reset single with the new scene data without close the window.

        @return: None
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
                self._state.update()
                self._state.draw()
            except exception.ChangeScene, e:
                self._scene.stop()
                self._scene = e.scene
                self._scene.start()
            except exception.StopVM:
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
        @return: driver.Clock
        """
        return self._clock

    def set_clock( self, clock ):
        """
        Set the VM's clock.
        @param mouse: a Clock object
        @type mouse: driver.Clock
        """
        self._clock = clock

    def get_display( self ):
        """
        Get the VM's display.
        @return: driver.Display
        """
        return self._display

    def set_display( self, display ):
        """
        Set the VM's display.
        @param mouse: a Display object
        @type mouse: driver.Display
        """
        self._display = display

    def get_mouse( self ):
        """
        Get the VM's mouse.
        @return: driver.Mouse
        """
        return self._mouse

    def set_mouse( self, mouse ):
        """
        Set the VM's mouse.
        @param mouse: a Mouse object
        @type mouse: driver.Mouse
        """
        self._mouse = mouse

    def get_scene( self ):
        """
        Get the VM's Scene.
        @return: scene.Scene
        """
        return self._scene

    def set_scene( self, scene ):
        """
        Set the VM's Scene.
        @param scene: a Scene object
        @type scene: scene.Scene
        """
        self._scene = scene

    scene   = property( get_scene, set_scene )
    mouse   = property( get_mouse, set_mouse )
    display = property( get_display, set_display )
    clock   = property( get_clock, set_clock )
    boot    = classmethod( boot )


class VMState( base.State ):
    """
    This class is a abstract state of the VM, the pre-mades  modes of VM inherit of this class.
    You can inherit to write your owns modes (states).

    VMState recieve the calls of VM with PyGame events, transform the PyGame Event object and process it to
    check if was a click, a doubleclick, a key pressed, key released, etc..., check if the coordenate collide with any,
    and depending of the VMState setted on VM, will launch the hight-level event to scene instance, the HUD, etc.
    """

    def __init__( self ):
        base.State.__init__( self )

    def on_quit( self ):
        raise NotImplementedError

    def keyboard_pressed( self, event ):
        raise NotImplementedError

    def keyboard_released( self, event ):
        raise NotImplementedError

    def mouse_pressed( self, event ):
        raise NotImplementedError

    def mouse_released( self, event ):
        raise NotImplementedError

    def update( self ):
        raise NotImplementedError

    def draw( self ):
        raise NotImplementedError


class NormalMode( VMState ):

    MASK_BTN_LEFT = 1<<0
    MASK_BTN_CENTER = 1<<1
    MASK_BTN_RIGHT = 1<<2

    BTN_LEFT = 0
    BTN_CENTER = 1
    BTN_RIGHT = 2

    def __init__( self ):
        VMState.__init__( self )
        self._pressed = 000
        self._time = [ None, None, None ]

    def on_quit( self ):
        VM().scene.on_quit()
        return self

    def keyboard_pressed( self, event ):
        VM().scene.on_key_down( event.key )
        return self

    def keyboard_released( self, event ):
        VM().scene.on_key_up( event.key )
        return self

    def mouse_pressed( self, event ):
        if event.button == 1:
            self._pressed |= self.MASK_BTN_LEFT
            self._time[ self.BTN_LEFT ] = VM().clock.time
        elif event.button == 2:
            self._pressed |= self.MASK_BTN_CENTER
            self._time[ self.BTN_CENTER ] = VM().clock.time
        elif event.button == 3:
            self._pressed |= self.MASK_BTN_RIGHT
            self._time[ self.BTN_RIGHT ] = VM().clock.time
        return self

    def mouse_released( self, event ):
        if event.button == 1:
            self._pressed &= ~self.MASK_BTN_LEFT
            self._time[ self.BTN_LEFT ] = VM().clock.time
        elif event.button == 2:
            self._pressed &= ~self.MASK_BTN_CENTER
            self._time[ self.BTN_CENTER ] = VM().clock.time
        elif event.button == 3:
            self._pressed &= ~self.MASK_BTN_RIGHT
            self._time[ self.BTN_RIGHT ] = VM().clock.time
        return self

    def update( self ):
        if (self._pressed & self.MASK_BTN_LEFT) == self.MASK_BTN_LEFT:
            pass
        print VM().clock.time
        return self

    def draw( self ):
        return self


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
