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
    A scene Machine for handle SceneStates
    """

    def on_quit( self ):
        """
        Call the "on_quit" method of the active SceneState.

        This method notify a user request of close the display.
        """
        self._state = self._state.on_quit()

    def on_action_end( self, action ):
        """
        Call the "on_action_end" method of the active SceneState.

        This method notify the conclusion of a action.

        @param action: the action that you wish to notify its aim
        @type action: Action
        """
        print "[Scene::%s] 'on_action_end' event launched (%s)" % ( self._state.__class__.__name__, action )
        self._state = self._state.on_action_end( action )

    def on_mouse_motion( self, vector ):
        """
        Call the "on_mouse_motion" method of the active SceneState.

        This method notify a movement in the mouse cursor.

        @param vector: The vector position after movement
        @type vector: Vector2D
        @return: None
        """
        print "[Scene::%s] 'on_mouse_motion' event launched (%s)" % ( self._state.__class__.__name__, vector)
        self._state = self._state.on_mouse_motion( vector )

    def on_mouse_over( self, obj ):
        """
        Call the "on_mouse_over" method of the active SceneState.

        This method notify that the mouse cursor position it start collision with an object.

        @param obj: The object that are colliding
        @type obj: Object
        @return: None
        """
        print "[Scene::%s] 'on_mouse_over' event launched (%s)" % ( self._state.__class__.__name__, obj )
        self._state = self._state.on_mouse_over( obj )

    def on_mouse_out( self, obj ):
        """
        Call the "on_mouse_out" method of the active SceneState.

        This method notify that the mouse cursor position it quit collision with an object.

        @param obj: The object that are quit colliding
        @type obj: Object
        @return: None
        """
        print "[Scene::%s] 'on_mouse_out' event launched (%s)" % ( self._state.__class__.__name__, obj )
        self._state = self._state.on_mouse_out( obj )

    def on_mouse_click( self, obj, button ):
        """
        Call the "on_mouse_click" method of the active SceneState.

        This method notify that the mouse did a single click on a object.

        @param obj: The object where did click
        @type obj: Object
        @param button: The name button that did click
        @type button: String
        """
        print "[Scene::%s] 'mouse_click' event launched (%s, %s)" % ( self._state.__class__.__name__, obj, button )
        self._state = self._state.on_mouse_click( obj, button )

    def on_mouse_doubleclick( self, obj, button ):
        """
        Call the "on_mouse_doubleclick" method of the active SceneState.

        This method notify that the mouse did a double click on a object.

        @param obj: The object where did double click
        @type obj: Object
        @param button: The name button that did double click
        @type button: String
        """
        print "[Scene::%s] 'mouse_doubleclick' event launched (%s, %s)" % ( self._state.__class__.__name__, obj, button )
        self._state = self._state.on_mouse_doubleclick( obj, button )

    def on_drag_start( self, obj, button ):
        """
        Call the "on_drag_start" method of the active SceneState.

        This method notify that the mouse did start a drag movement.

        @param obj: The object where start the drag
        @type obj: Object
        @param button: The button name that drag start
        @type button: String
        """
        print "[Scene::%s] 'on_drag_start' event launched (%s, %s)" % ( self._state.__class__.__name__, obj, button )
        self._state = self._state.on_drag_start( obj, button )

    def on_drag_end( self, obj, button ):
        """
        Call the "on_drag_end" method of the active SceneState.

        This method notify that the mouse did end a drag movement..

        @param obj: The object where end the drag
        @type obj: Object
        @param button: The button name that start the drag
        @type button: String
        """
        print "[Scene::%s] 'on_drag_end' event launched (%s, %s)" % ( self._state.__class__.__name__, obj, button )
        self._state = self._state.on_drag_end( obj, button )

    def on_key_up( self, key ):
        """
        Call the "on_key_up" method of the active SceneState.

        This method notify a released key of keyboard.

        @param key: The key that has released.
        @type key: String
        """
        print "[Scene::%s] 'key_up' event launched (%s)" % ( self._state.__class__.__name__, key )
        self._state = self._state.on_key_up( key )

    def on_key_down( self, key ):
        """
        Call the "on_key_down" method of the active SceneState.

        This method notify a pressed key of keyboard.

        @param key: The key that has pressed.
        @type key: String
        """
        print "[Scene::%s] 'key_down' event launched (%s)" % ( self._state.__class__.__name__, key )
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
        return self

    def on_action_end( self, action ):
        """
        (See: on_action_end() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_motion( self, vector ):
        """
        (See: on_mouse_motion() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_click( self, obj, button ):
        """
        (See: on_mouse_click() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_doubleclick( self, obj, button ):
        """
        (See: on_mouse_doubleclick() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_over( self, obj ):
        """
        (See: on_mouse_over() method on scene.Scene class).

        @return: self
        """
        return self

    def on_mouse_out( self, obj ):
        """
        (See: on_mouse_out() method on scene.Scene class).

        @return: self
        """
        return self

    def on_drag_start( self, obj, button ):
        """
        (See: on_drag_start() method on scene.Scene class).

        @return: self
        """
        return self

    def on_drag_end( self, obj, button ):
        """
        (See: on_drag_end() method on scene.Scene class).

        @return: self
        """
        return self

    def on_key_up( self, key ):
        """
        (See: on_key_up() method on scene.Scene class).

        @return: self
        """
        return self

    def on_key_down( self, key ):
        """
        (See: on_key_down() method on scene.Scene class).

        @return: self
        """
        return self

    def draw( self ):
        """
        Draw all the scene objects.
        """
        for obj in self.scene: obj.draw()
        return self

    def update( self ):
        """
        Update all the Scene objects.
        """
        for obj in self.scene: obj.update()
        return self

    scene    = property( get_scene )
    vm       = property( get_vm )
