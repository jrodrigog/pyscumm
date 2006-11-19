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

import logger

class Scene( base.StateMachine, dict ):
    """
    Scene Machine handles SceneStates
    """

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

        @param vector: The location of the cursor
        @type vector: Vector3D
        """
        self._state = self._state.on_mouse_motion( location )

    def on_mouse_over( self, obj ):
        """
        Call the "on_mouse_over" method of the active SceneState.
        @param obj: A list of objects under the cursor
        @type obj: list
        """
        self._state = self._state.on_mouse_over( obj )

    def on_mouse_out( self, obj ):
        """
        Call the "on_mouse_out" method of the active SceneState.
        @param obj: A list of objects under the cursor
        @type obj: list
        """
        self._state = self._state.on_mouse_out( obj )

    def on_mouse_click( self, obj, button ):
        """
        Call the "on_mouse_click" method of the active SceneState.
        This method notifies a mouse click.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param button: The name button that did click
        @type button: String
        """
        self._state = self._state.on_mouse_click( obj, button )

    def on_mouse_double_click( self, obj, button ):
        """
        Call the "on_mouse_double_click" method of the active SceneState.
        This method notify that the mouse did a double click on a object.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param button: The name button that did double click
        @type button: String
        """
        self._state = self._state.on_mouse_double_click( obj, button )

    def on_drag_start( self, obj, button ):
        """
        Call the "on_drag_start" method of the active SceneState.
        This method notify that the mouse did start a drag movement.
        @param obj: A list of objects under the cursor
        @type obj: list
        @param button: The button name that starts the drag
        @type button: String
        """
        self._state = self._state.on_drag_start( obj, button )

    def on_drag_end( self, button ):
        """
        Call the "on_drag_end" method of the active SceneState.
        This method notify that the mouse did end a drag movement..
        @param button: The button that ends the drag
        @type button: String
        """
        self._state = self._state.on_drag_end( button )

    def on_key_up( self, key ):
        """
        Call the "on_key_up" method of the active SceneState.
        This method notify a released key of keyboard.
        @param key: The key that has released.
        @type key: String
        """
        self._state = self._state.on_key_up( key )

    def on_key_down( self, key ):
        """
        Call the "on_key_down" method of the active SceneState.
        This method notify a pressed key of keyboard.
        @param key: The key that has pressed.
        @type key: String
        """
        self._state = self._state.on_key_down( key )

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
        logger.Logger().info( "on_quit(%d)" )
        return self

    def on_action_end( self, action ):
        """
        (See: on_action_end() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_action_end(%s)" % action )
        return self

    def on_mouse_motion( self, location ):
        """
        (See: on_mouse_motion() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_mouse_motion(%s)" % location )
        return self

    def on_mouse_click( self, obj, button ):
        """
        (See: on_mouse_click() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_mouse_motion(%s,%s)" % ( obj, button ) )
        return self

    def on_mouse_double_click( self, obj, button ):
        """
        (See: on_mouse_double_click() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_mouse_double_click(%s,%s)" % ( obj, button ) )
        return self

    def on_mouse_over( self, obj ):
        """
        (See: on_mouse_over() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_mouse_over(%s)" % obj )
        return self

    def on_mouse_out( self, obj ):
        """
        (See: on_mouse_out() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_mouse_out(%s)" % obj )
        return self

    def on_drag_start( self, obj, button ):
        """
        (See: on_drag_start() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_drag_start(%s,%s)" % ( obj, button ) )
        return self

    def on_drag_end( self, button ):
        """
        (See: on_drag_end() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_drag_end(%s)" % button )
        return self

    def on_key_up( self, key ):
        """
        (See: on_key_up() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_key_up(%s)" % key )
        return self

    def on_key_down( self, key ):
        """
        (See: on_key_down() method on scene.Scene class).

        @return: self
        """
        logger.Logger().info( "on_key_down(%s)" % key )
        return self

    def draw( self ):
        """
        Draw all the scene objects.
        """
        #for obj in self.scene: obj.draw()
        return self

    def update( self ):
        """
        Update all the Scene objects.
        """
        #for obj in self.scene: obj.update()
        return self

    scene    = property( get_scene )
    vm       = property( get_vm )
