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

import pygame, os.path
import base, vm



class Game( base.StateMachine ):
    """
    A Game Machine for handle GameStates
    """

    def on_action_end( self, action ):
        """
        Call the "on_action_end" method of the active GameState.
        
        This method notify the conclusion of a action.
        
        @param action: the action that you wish to notify its aim
        @type action: Action
        """
        print "[Game] 'on_action_end' event launched"
        self._state = self._state.on_action_end( action )

    def on_mouse_over( self, obj ):
        """
        Call the "on_mouse_over" method of the active GameState.
        
        This method notify that the mouse cursor position it start collision with an object.
        
        @param obj: The object that are colliding
        @type obj: Object
        @return: None
        """
        print "[Game] 'on_mouse_over' event launched (%s)" % ( obj )
        self._state = self._state.on_mouse_over( obj )

    def mouse_out( self, obj ):
        """
        Call the "on_mouse_out" method of the active GameState.
        
        This method notify that the mouse cursor position it quit collision with an object.
        
        @param obj: The object that are quit colliding
        @type obj: Object
        @return: None
        """
        print "[Game] 'on_mouse_out' event launched (%s)" % ( obj )
        self._state = self._state.on_mouse_out( obj )

    def on_mouse_click( self, obj, button ):
        """
        Call the "on_mouse_click" method of the active GameState
        
        This method notify that the mouse did a single click on a object.
        
        @param obj: The object where did click
        @type obj: Object
        @param button: The name button that did click
        @type button: String
        """
        print "[Game] 'mouse_click' event launched (%s, %s)" % ( obj, button )
        self._state = self._state.on_mouse_click( obj, button )

    def on_mouse_doubleclick( self, obj, button ):
        """
        Call the "on_mouse_doubleclick" method of the active GameState
        
        This method notify that the mouse did a double click on a object.
        
        @param obj: The object where did double click
        @type obj: Object
        @param button: The name button that did double click
        @type button: String
        """
        print "[Game] 'mouse_doubleclick' event launched (%s, %s)" % ( obj, button )
        self._state = self._state.on_mouse_doubleclick( obj, button )

    def on_drag_start( self, obj, button ):
        """
        Call the "on_drag_start" method of the active GameState
        
        This method notify that the mouse did start a drag movement.
        
        @param obj: The object where start the drag
        @type obj: Object
        @param button: The button name that drag start
        @type button: String
        """
        print "[Game] 'on_drag_start' event launched (%s, %s)" % ( obj, button )
        self._state = self._state.on_drag_start( obj, button )

    def on_drag_end( self, obj, button ):
        """
        Call the "on_drag_end" method of the active GameState
        
        This method notify that the mouse did end a drag movement..
        
        @param obj: The object where end the drag
        @type obj: Object
        @param button: The button name that start the drag
        @type button: String
        """
        print "[Game] 'on_drag_end' event launched (%s, %s)" % ( obj, button )
        self._state = self._state.on_drag_end( obj, button )
        
    def key_up( self, key ):
        """
        Call the "on_key_up" method of the active GameState
        
        This method notify a released key of keyboard.
        
        @param key: The key that has released.
        @type key: String
        """
        print "[Game] 'key_up' event launched (%s)" % ( key )
        self._state = self._state.on_key_up( key )

    def key_down( self, key ):
        """
        Call the "on_key_down" method of the active GameState
        
        This method notify a pressed key of keyboard.
        
        @param key: The key that has pressed.
        @type key: String
        """
        print "[Game] 'key_down' event launched (%s)" % ( key )
        self._state = self._state.on_key_down( key )

    def draw( self ):
        self._state = self._state.draw()

    def update( self ):
        self._state = self._state.update()
    
    

class GameState( base.StateMachine, dict ):
    """
    Abstract GameState
    
    You need inherit of this class for make rooms
    """
    
    def get_game( self ):
        """
        Return the game instance.
        
        @return: Game
        """
        return vm.VM.instance.game
      
    def get_vm( self ):
        """
        Return the VM instance.
        
        @return: VM
        """
        return vm.VM.instance
    
    def on_action_end( self, action ):
        """
        (See: on_action_end() method on game.Game class)
        
        @return: self
        """
        return self
        
    def on_mouse_click( self, obj, button ):
        """
        (See: on_mouse_click() method on game.Game class)
        
        @return: self
        """
        return self

    def on_mouse_doubleclick( self, obj, button ):
        """
        (See: on_mouse_doubleclick() method on game.Game class)
        
        @return: self
        """
        return self

    def on_mouse_over( self, obj ):
        """
        (See: on_mouse_over() method on game.Game class)
        
        @return: self
        """
        return self

    def on_mouse_out( self, obj ):
        """
        (See: on_mouse_out() method on game.Game class)
        
        @return: self
        """
        return self

    def on_drag_start( self, obj, button ):
        """
        (See: on_drag_start() method on game.Game class)
        
        @return: self
        """
        return self

    def on_drag_end( self, obj, button ):
        """
        (See: on_drag_end() method on game.Game class)
        
        @return: self
        """
        return self

    def on_key_up( self, key ):
        """
        (See: on_key_up() method on game.Game class)
        
        @return: self
        """
        return self

    def on_key_down( self, key ):
        """
        (See: on_key_down() method on game.Game class)
        
        @return: self
        """
        return self

    def draw( self ):
        """
        (See: draw() method on game.Game class)
        
        @return: self
        """
        return self

    def update( self ):
        """
        (See: update() method on game.Game class)
        
        @return: self
        """
        return self

    game    = property( get_game )
    vm      = property( get_vm )

    
