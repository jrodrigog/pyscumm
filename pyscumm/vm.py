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

from types import *
import base



"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 8/11/2006
"""



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

    def __init__( self, game, clock=None, display=None, mouse=None ):
        """
        Construct the Virtual Machine object saving some instances of components in private attributes.
        this objects are statics, if one of this argument dont is passed, or already exist a instance of this,
        this argument will be a new instance of the object.
    
        @param game: a Game instance.
        @type game: game.Game
        @param clock: a Clock instance.
        @type clock: game.Clock
        @param display: a Display instance.
        @type display: game.Display
        @param mouse: a Mouse instance.
        @type mouse: game.Mouse
        """
        base.StateMachine.__init__( self )
        if isinstance( mouse, NoneType ):
            self._mouse = driver.Mouse()
        if isinstance( display, NoneType ):
            self._display = driver.Display()
        if isinstance( clock, NoneType ):
            self._clock = driver.Clock()

    def on_quit( self ):
        """
        Report to the active state a quit event.
        
        @return: None
        """
        self._state = self._state.on_quit()

    def get_game( self ):
        """
        Return the game instance.
    
        @return: Game instance
        @rtype: Game
        """
        return self._game

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
        
    def on_update( self ):
        # ToDo
        pass
    
    def on_draw( self ):
        #ToDo
        pass
    
    def start( self ):
        """
        Reset the VM with the vm.NormalMode state.
    
        @return: None
        """
        self._state = NormalMode()
        
    def main( self ):
        """
        Init the main loop of the engine, open a display window, launch events to the
        active state, update and render the scene each frame. if StopGame exception is launched,
        the VM stop self, and close the window.If however GameChange exception is launched,
        the VM will reset single with the new game data without close the window.
    
        @return: None
        """
        self.start()
        self._display.open()
        self._game.start()
        leave = False
        while not leave:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.on_quit()
                    elif event.type == pygame.KEYDOWN:
                        self.keyboard_pressed( event )
                    elif event.type == pygame.KEYUP:
                        self.keyboard_released( event )
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_pressed( event )
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_released( event )
                self._game.update()
                self._game.draw()
                self._clock.tick()
            except GameChange, e:
                self._game.stop()
                self._game = e.game
                self._game.start()
            except StopGame:
                leave = True
                self._display.close()

    def boot( self, game ):
        vm = self( game )
        vm.main()

    boot    = classmethod( boot )
    game    = property( get_game )
    
    

class VMState( base.State ):
    """    
    This class is a abstract state of the VM, the pre-mades  modes of VM inherit of this class.
    You can inherit to write your owns modes (states).
    
    VMState recieve the calls of VM with PyGame events, transform the PyGame Event object and process it to
    check if was a click, a doubleclick, a key pressed, key released, etc..., check if the coordenate collide with any,
    and depending of the VMState setted on VM, will launch the hight-level event to Game instance, the HUD, etc.
    """

    def keyboard_pressed( self, event ):
        # Detect key
        # Detect if collide with any object
        # Send all info to game instance
        return self

    def keyboard_released( self, event ):
        # Detect key
        # Detect if collide with any object
        # Send all info to game instance
        return self

    def mouse_pressed( self, event ):
        # Detect button
        # Detect if collide with any object
        # Send all info to game instance
        return self

    def mouse_released( self, event ):
        # Detect button
        # Detect if collide with any object
        # Send all info to game instance
        return self
    
    
    
class PassiveMode( VMState ):
    """
    This state of the VM, ignore all PyGame events, it get the events and it does not do anything with them.
    PassiveMode  is the best VMState option, for game-intros, movie-mode,  and other situations where your game
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



class KeyMode( VMState ):
    """
    This state of the VM, ignore PyGame mouse events, he get the PyGame Mouse events and it dont do anything with them.
    if the event come of a keyboard device, it lauch to Game.
    
    KeyMode  is the best VMState option where your game wanna ignore mouse events.
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



class MouseMode( VMState ):
    """
    This mode (state) of the VM, ignore PyGame key events, he get the PyGame key events and it dont do anything with them.
    if the event come of a mouse device, it lauch to Game.
    
    MouseMode  is the best VMState option where your game wanna ignore keyboard events.
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
    this only capture mouse events, but dont launch it to Game instance, if not to the HUD.

    On this state, the mouse only collide with the visual elements of the dialog interface,
    and ignore collides with actors, objects, etc... only with phrases and other elements of
    the dialog interface.
    
    The HUD is the class that handdle the visual interface of the dialogs, (see: HUD class)
    
    MouseMode  is the best VMState option where your game wanna ignore keyboard events
    and the mouse only must be collide with dialog interface and nots in other objects of the game.
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