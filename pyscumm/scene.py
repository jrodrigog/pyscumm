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
    """This is a Scene. It is an state machine so it only
    delivers events to it's active state. It does keep track
    of the objects in the scene in its own dictionary. When
    drawing objects the scene will draw them ordered."""

    def __init__( self ):
        """Build a Scene object."""
        self._sorted = base.SortedList()

    def quit( self ):
        """Reports a Pygame's quit event to the active state."""
        self._state = self._state.quit()

    def active_event( self, event ):
        """
        Reports a Pygame's active event to the active state.
        @param event: A Pygame's ACTIVEEVENT event
        @type event: Event(Pygame)
        """
        self._state = self._state.active_event( event )

    def key_down( self, event ):
        """
        Reports a Pygame's key down event to the active state.
        @param event: A Pygame's KEYDOWN event
        @type event: Event(Pygame)
        """
        self._state = self._state.key_down( event )

    def key_up( self, event ):
        """
        Reports a Pygame's key up event to the active state.
        @param event: A Pygame's KEYUP event
        @type event: Event(Pygame)
        """
        self._state = self._state.key_up( event )

    def mouse_motion( self, event ):
        """
        Reports a Pygame's mouse motion event to the active state.
        @param event: A Pygame's MOUSEMOTION event
        @type event: Event(Pygame)
        """
        self._state = self._state.mouse_motion( event )

    def mouse_button_up( self, event ):
        """
        Reports a Pygame's mouse button up event to the active state.
        @param event: A Pygame's MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        self._state = self._state.mouse_button_up( event )

    def mouse_button_down( self, event ):
        """
        Reports a Pygame's mouse button down event to the active state.
        @param event: A Pygame's MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        self._state = self._state.mouse_button_down( event )

    def joy_axis_motion( self, event ):
        """
        Reports a Pygame's joy axis motion event to the active state.
        @param event: A Pygame's JOYAXISMOTION event
        @type event: Event(Pygame)
        """
        self._state = self._state.joy_axis_motion( event )

    def joy_ball_motion( self, event ):
        """
        Reports a Pygame's joy ball motion event to the active state.
        @param event: A Pygame's JOYBALLMOTION event
        @type event: Event(Pygame)
        """
        self._state = self._state.joy_ball_motion( event )

    def joy_hat_motion( self, event ):
        """
        Reports a Pygame's joy hay motion event to the active state.
        @param event: A Pygame's JOYHATMOTION event
        @type event: Event(Pygame)
        """
        self._state = self._state.joy_hat_motion( event )

    def joy_button_up( self, event ):
        """
        Reports a Pygame's joy button up event to the active state.
        @param event: A Pygame's JOYBUTTONUP event
        @type event: Event(Pygame)
        """
        self._state = self._state.joy_button_up( event )

    def joy_button_down( self, event ):
        """
        Reports a Pygame's joy button down event to the active state.
        @param event: A Pygame's JOYBUTTONDOWN event
        @type event: Event(Pygame)
        """
        self._state = self._state.joy_button_down( event )

    def video_resize( self, event ):
        """
        Reports a Pygame's video resize event to the active state.
        @param event: A Pygame's VIDEORESIZE event
        @type event: Event(Pygame)
        """
        self._state = self._state.video_resize( event )

    def video_expose( self, event ):
        """
        Reports a Pygame's video expose event to the active state.
        @param event: A Pygame's VIDEOEXPOSE event
        @type event: Event(Pygame)
        """
        self._state = self._state.video_expose( event )

    def user_event( self, event ):
        """
        Reports a Pygame's user event to the active state.
        @param event: A Pygame's USEREVENT event
        @type event: Event(Pygame)
        """
        self._state = self._state.user_event( event )

    def on_action_end( self, event ):
        """
        Reports an action end event to the active state.
        @param event: A Pyscumm ACTIONEND event
        @type event: Event
        """
        self._state = self._state.on_action_end( event )

    def on_mouse_motion( self, event ):
        """
        Reports a mouse motion event to the active state.
        @param event: A Pyscumm MOUSEMOTION event
        @type event: Event
        """
        self._state = self._state.on_mouse_motion( event )

    def on_mouse_in( self, event ):
        """
        Reports a mouse in event to the active state.
        @param event: A Pyscumm MOUSEIN event
        @type event: Event
        """
        self._state = self._state.on_mouse_in( event )

    def on_mouse_out( self, event ):
        """
        Reports a mouse out event to the active state.
        @param event: A Pyscumm MOUSEOUT event
        @type event: Event
        """
        self._state = self._state.on_mouse_out( event )

    def on_mouse_click( self, event ):
        """
        Reports a mouse click event to the active state.
        @param event: A Pyscumm MOUSECLICK event
        @type event: Event
        """
        self._state = self._state.on_mouse_click( event )

    def on_mouse_double_click( self, event ):
        """
        Reports a mouse double click event to the active state.
        @param event: A Pyscumm MOUSEDOUBLECLICK event
        @type event: Event
        """
        self._state = self._state.on_mouse_double_click( event )

    def on_mouse_drag_start( self, event ):
        """
        Reports a mouse drag start event to the active state.
        @param event: A Pyscumm MOUSEDRAGSTART event
        @type event: Event
        """
        self._state = self._state.on_mouse_drag_start( event )

    def on_mouse_drag_end( self, event ):
        """
        Reports a mouse drag end event to the active state.
        @param event: A Pyscumm MOUSEDRAGENG event
        @type event: Event
        """
        self._state = self._state.on_mouse_drag_end( event )

    def on_mouse_button_down( self, event ):
        """
        Reports a mouse down event to the active state.
        @param event: A Pyscumm MOUSEDOWN event
        @type event: Event
        """
        self._state = self._state.on_mouse_button_down( event )

    def on_mouse_button_up( self, event ):
        """
        Reports a mouse up event to the active state.
        @param event: A Pyscumm MOUSEUP event
        @type event: Event
        """
        self._state = self._state.on_mouse_button_up( event )

    def draw( self ):
        """Reports a draw event to the active state."""
        self._state = self._state.draw()

    def update( self ):
        """Reports an update event to the active state."""
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
    This is an Abstract Scene State.
    By subclassing this class you cand override all the
    methods and start receiving events.
    """

    def get_scene( self ):
        """Returns the scene instance.
        @return: Active Scene object
        @rtype: Scene
        """
        return vm.VM().scene

    def get_vm( self ):
        """Returns the VM object.
        @return: VM object
        @rtype: VM"""
        return vm.VM()

    def quit( self ):
        """Receives a Pygame's quit event.
        Override this method in your subclass to handle this event."""
        raise vm.StopVM()

    def active_event( self, event ):
        """
        Receives a Pygame's active event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's ACTIVEEVENT event
        @type event: Event(Pygame)
        """
        return self

    def key_down( self, event ):
        """
        Receives a Pygame's key down event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's KEYDOWN event
        @type event: Event(Pygame)
        """
        return self

    def key_up( self, event ):
        """
        Receives a Pygame's key up event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's KEYUP event
        @type event: Event(Pygame)
        """
        return self

    def mouse_motion( self, event ):
        """
        Receives a Pygame's mouse motion event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's MOUSEMOTION event
        @type event: Event(Pygame)
        """
        return self

    def mouse_button_up( self, event ):
        """
        Receives a Pygame's mouse button up event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        return self

    def mouse_button_down( self, event ):
        """
        Receives a Pygame's mouse button down event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        return self

    def joy_axis_motion( self, event ):
        """
        Receives a Pygame's joy axis motion event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's JOYAXISMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_ball_motion( self, event ):
        """
        Receives a Pygame's joy ball motion event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's JOYBALLMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_hat_motion( self, event ):
        """
        Receives a Pygame's joy hay motion event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's JOYHATMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_button_up( self, event ):
        """
        Receives a Pygame's joy button up event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's JOYBUTTONUP event
        @type event: Event(Pygame)
        """
        return self

    def joy_button_down( self, event ):
        """
        Receives a Pygame's joy button down event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's JOYBUTTONDOWN event
        @type event: Event(Pygame)
        """
        return self

    def video_resize( self, event ):
        """
        Receives a Pygame's video resize event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's VIDEORESIZE event
        @type event: Event(Pygame)
        """
        return self

    def video_expose( self, event ):
        """
        Receives a Pygame's video expose event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's VIDEOEXPOSE event
        @type event: Event(Pygame)
        """
        return self

    def user_event( self, event ):
        """
        Receives a Pygame's user event.
        Override this method in your subclass to handle this event.
        @param event: A Pygame's USEREVENT event
        @type event: Event(Pygame)
        """
        return self

    def on_action_end( self, event ):
        """
        Receives an action end event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm ACTIONEND event
        @type event: Event
        """
        return self

    def on_mouse_motion( self, event ):
        """
        Receives a mouse motion event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEMOTION event
        @type event: Event
        """
        return self

    def on_mouse_in( self, event ):
        """
        Receives a mouse in event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEIN event
        @type event: Event
        """
        return self

    def on_mouse_out( self, event ):
        """
        Receives a mouse out event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEOUT event
        @type event: Event
        """
        return self

    def on_mouse_click( self, event ):
        """
        Receives a mouse click event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSECLICK event
        @type event: Event
        """
        return self

    def on_mouse_double_click( self, event ):
        """
        Receives a mouse double click event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEDOUBLECLICK event
        @type event: Event
        """
        return self

    def on_mouse_drag_start( self, event ):
        """
        Receives a mouse drag start event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEDRAGSTART event
        @type event: Event
        """
        return self

    def on_mouse_drag_end( self, event ):
        """
        Receives a mouse drag end event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEDRAGENG event
        @type event: Event
        """
        return self

    def on_mouse_button_down( self, event ):
        """
        Receives a mouse down event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEDOWN event
        @type event: Event
        """
        return self

    def on_mouse_button_up( self, event ):
        """
        Receives a mouse up event.
        Override this method in your subclass to handle this event.
        @param event: A Pyscumm MOUSEUP event
        @type event: Event
        """
        return self

    def draw( self ):
        """Receives a draw event and draws all the scene objects."""
        for obj in self.scene.sorted: obj.draw()
        return self

    def update( self ):
        """Receives and update event and updates all the Scene objects."""
        for obj in self.scene.sorted: obj.update()
        return self

    scene    = property( get_scene )
    vm       = property( get_vm )
