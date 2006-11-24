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

class Scene( base.StateMachine, dict ):
    """
    Scene Machine handles SceneStates
    """
    def __init__( self ):
        """Build a Scene object."""
        self._sorted = base.SortedList()

    def mouse_pressed( self, button ):
        self._state = self._state.mouse_pressed( button )

    def mouse_released( self, button ):
        self._state = self._state.mouse_released( button )

    def on_quit( self ):
        """
        Call the "on_quit" method of the active SceneState.
        This method notifies a request to quit
        """
        self._state = self._state.on_quit()

    def on_action_end( self, action ):
        """
        Call the "on_action_end" method of the active SceneState.

        This method notify the conclusion of a action.

        @param action: The action ending
        @type action: Action
        """
        self._state = self._state.on_action_end( action )

    def on_mouse_motion( self, location ):
        """
        Call the "on_mouse_motion" method of the active SceneState.

        This method notify a movement in the mouse cursor.

        @param location: The location of the cursor
        @type location: Vector3D
        """
        self._state = self._state.on_mouse_motion( location )

    def on_mouse_over( self, obj, location ):
        """
        Call the "on_mouse_over" method of the active SceneState.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        """
        self._state = self._state.on_mouse_over( obj, location )

    def on_mouse_out( self, obj, location ):
        """
        Call the "on_mouse_out" method of the active SceneState.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        """
        self._state = self._state.on_mouse_out( obj, location )

    def on_mouse_click( self, obj, location, button ):
        """
        Call the "on_mouse_click" method of the active SceneState.
        This method notifies a mouse click.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        @param button: The name button that did click
        @type button: String
        """
        self._state = self._state.on_mouse_click( obj, location, button )

    def on_mouse_double_click( self, obj, location, button ):
        """
        Call the "on_mouse_double_click" method of the active SceneState.
        This method notify that the mouse did a double click on a object.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        @param button: The name button that did double click
        @type button: String
        """
        self._state = self._state.on_mouse_double_click( obj, location, button )

    def on_mouse_drag_start( self, obj, location, button ):
        """
        Call the "on_mouse_drag_start" method of the active SceneState.
        This method notify that the mouse did start a drag movement.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        @param button: The button name that starts the drag
        @type button: String
        """
        self._state = self._state.on_mouse_drag_start( obj, location, button )

    def on_mouse_drag_end( self, obj, location, button ):
        """
        Call the "on_mouse_drag_end" method of the active SceneState.
        This method notify that the mouse did end a drag movement.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param location: The location of the cursor
        @type location: Vector3D
        @param button: The button that ends the drag
        @type button: String
        """
        self._state = self._state.on_mouse_drag_end( obj, location, button )

    def on_mouse_down( self, event ):
        """
        Receives a mouse pressed event and forwards it.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        self._state = self._state.on_mouse_down( event )

    def on_mouse_up( self, event ):
        """
        Receives a mouse released event and forwards it.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        self._state = self._state.on_mouse_up( event )

    def on_key_up( self, event ):
        """
        Call the "on_key_up" method of the active SceneState.
        This method notify a released key of keyboard.
        @param event: Pygame(Event)
        @type event: String
        """
        self._state = self._state.on_key_up( event.key )

    def on_key_down( self, event ):
        """
        Call the "on_key_down" method of the active SceneState.
        This method notify a pressed key of keyboard.
        @param event: Pygame(Event)
        @type event: String
        """
        self._state = self._state.on_key_down( event.key )

    def draw( self ):
        """
        Draw the Scene, delegate in the state.
        """
        self._state = self._state.draw()

    def update( self ):
        """
        Update the Scene, delegate in the state.
        """
        self._state = self._state.update()

    def sort( self ):
        """Sort the object list."""
        self._sorted.sort()

    def __setitem__( self, key, obj ):
        if self.has_key( key ):
            self._sorted.pop( self._sorted.index( self[ key ] ) )
        dict.__setitem__( self, key, obj )
        self._sorted.insert( obj )

    def __delitem__( self, key ):
        obj = self[ key ]
        dict.__delitem__( self, key )
        self._sorted.pop( self._sorted.index( obj ) )

    def get_sorted( self ):
        """Get the sorted list of objects.
        @return: Sorted list of objects.
        @rtype: SortedList"""
        return self._sorted

    sorted = property( get_sorted )


class SceneState( base.StateMachine ):
    """
    Abstract SceneState.

    You need inherit of this class for make scenes.
    """

    def get_scene( self ):
        """
        Return the scene instance.

        @return: Scene
        """
        return vm.VM().scene

    def get_vm( self ):
        """
        Return the VM instance.

        @return: VM
        """
        return vm.VM()

    def on_quit( self ):
        """
        (See: on_quit() method on scene.Scene class).

        @return: self
        """
        raise vm.StopVM()

    def on_action_end( self, action ):
        """
        (See: on_action_end() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_motion( self, location ):
        """
        (See: on_mouse_motion() method on scene.Scene class).

        @return: self
        """
        #base.Logger().info( "on_mouse_motion(%s)" % location )
        return self

    def on_mouse_click( self, obj, location, button ):
        """
        (See: on_mouse_click() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_double_click( self, obj, location, button ):
        """
        (See: on_mouse_double_click() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_over( self, obj, location ):
        """
        (See: on_mouse_over() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_out( self, obj, location ):
        """
        (See: on_mouse_out() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_drag_start( self, obj, location, button ):
        """
        (See: on_mouse_drag_start() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_drag_end( self, obj, location, button ):
        """
        (See: on_mouse_drag_end() method on scene.Scene class).

        @return: self
        """
        return self

    def on_key_up( self, event ):
        """
        (See: on_key_up() method on scene.Scene class).

        @return: self
        """
        return self

    def on_key_down( self, event ):
        """
        (See: on_key_down() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_down( self, event ):
        """
        Receives a mouse pressed.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        return self

    def on_mouse_up( self, event ):
        """
        Receives a mouse released.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        return self

    def draw( self ):
        """Draws all the scene objects."""
        for obj in self.scene.sorted: obj.draw()
        return self

    def update( self ):
        """Updates all the Scene objects."""
        for obj in self.scene.sorted: obj.update()
        return self

    scene    = property( get_scene )
    vm       = property( get_vm )
