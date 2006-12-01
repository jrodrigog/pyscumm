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
import driver
from base import Logger, StateMachine, State
from constant import B_LEFT, B_CENTER, B_RIGHT
from box import Point

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
        self.scene = scene


class StopVM( Exception ):
    """This exception halts the VM, completely stopping it."""
    pass

class Event( dict ):
    """This is a VM Event, it works as a dictionary
    and you can access its attributes too.
    You can create your own events very easily:
    evt = Event({"foo":1,"var":2})
    print evt.foo, evt.var
    print evt["foo"], evt["bar"]
    """
    def __getattr__( self, attr ):
        """Returns the required attribute by name.
        It picks the attribute from the dictionary.
        @param attr: Attribute name
        @type attr: string
        @return: The attribute's Python object
        @rtype: object
        """
        return self[ attr ]


class VM( StateMachine ):
    """
    VM (Virtual Machine) its a state machine (See state pattern), its the core of pyscumm,
    this haddle Pygame events, draw each drawable object depends of her Zplanes, etc
    This VM  recollect the low-level events (see main() method) and launch it to the active state
    in same method, update and draw each element of the game.

    PySCUMM have built-in some pre-mades VMStates..., the VMStates, are states of VM, these wants
    complex algorithms sometimes are unnecessary depending of the types of events that requires
    in your game on this momment.

    PySCUMM include pre-mades states:

            - vm.Passive: This state ignores all events.
            - vm.Mouse: This state launchs all events.
            - vm.Conversation: This state only reports object clicked in the HUD.
    """

    # Singleton's shared state
    _shared_state = {}

    def __init__( self ):
        """Singletonize a VM object. Construct a Virtual Machine
        with it's default components."""
        self.__dict__ = self._shared_state
        if self._shared_state: return
        StateMachine.__init__( self )
        self.display = None
        self.mouse = driver.Mouse()
        self.clock = driver.Clock()
        self.scene = None
        self.event = {
            pygame.QUIT            : self.quit,
            pygame.ACTIVEEVENT     : self.active_event,
            pygame.KEYDOWN         : self.key_down,
            pygame.KEYUP           : self.key_up,
            pygame.MOUSEMOTION     : self.mouse_motion,
            pygame.MOUSEBUTTONDOWN : self.mouse_button_down,
            pygame.MOUSEBUTTONUP   : self.mouse_button_up,
            pygame.JOYAXISMOTION   : self.joy_axis_motion,
            pygame.JOYBALLMOTION   : self.joy_ball_motion,
            pygame.JOYHATMOTION    : self.joy_hat_motion,
            pygame.JOYBUTTONDOWN   : self.joy_button_up,
            pygame.JOYBUTTONDOWN   : self.joy_button_up,
            pygame.VIDEORESIZE     : self.video_resize,
            pygame.VIDEOEXPOSE     : self.video_expose,
            pygame.USEREVENT       : self.user_event }

    def quit( self, event=None ):
        """Reports a Pygame's quit event to the active state."""
        self.state = self.state.quit()

    def active_event( self, event ):
        """
        Reports a Pygame's active event to the active state.
        @param event: A Pygame ACTIVEEVENT event
        @type event: Event(Pygame)
        """
        self.state = self.state.active_event( event )

    def key_down( self, event ):
        """
        Reports a Pygame's key down event to the active state.
        @param event: A Pygame KEYDOWN event
        @type event: Event(Pygame)
        """
        self.state = self.state.key_down( event )

    def key_up( self, event ):
        """
        Reports a Pygame's key up event to the active state.
        @param event: A Pygame KEYUP event
        @type event: Event(Pygame)
        """
        self.state = self.state.key_up( event )

    def mouse_motion( self, event ):
        """
        Reports a Pygame's mouse motion event to the active state.
        @param event: A Pygame MOUSEMOTION event
        @type event: Event(Pygame)
        """
        self.state = self.state.mouse_motion( event )

    def mouse_button_up( self, event ):
        """
        Reports a Pygame's mouse button up event to the active state.
        @param event: A Pygame MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        self.state = self.state.mouse_button_up( event )

    def mouse_button_down( self, event ):
        """
        Reports a Pygame's mouse button down event to the active state.
        @param event: A Pygame MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        self.state = self.state.mouse_button_down( event )

    def joy_axis_motion( self, event ):
        """
        Reports a Pygame's joy axis motion event to the active state.
        @param event: A Pygame JOYAXISMOTION event
        @type event: Event(Pygame)
        """
        self.state = self.state.joy_axis_motion( event )

    def joy_ball_motion( self, event ):
        """
        Reports a Pygame's joy ball motion event to the active state.
        @param event: A Pygame JOYBALLMOTION event
        @type event: Event(Pygame)
        """
        self.state = self.state.joy_ball_motion( event )

    def joy_hat_motion( self, event ):
        """
        Reports a Pygame's joy hay motion event to the active state.
        @param event: A Pygame JOYHATMOTION event
        @type event: Event(Pygame)
        """
        self.state = self.state.joy_hat_motion( event )

    def joy_button_up( self, event ):
        """
        Reports a Pygame's joy button up event to the active state.
        @param event: A Pygame JOYBUTTONUP event
        @type event: Event(Pygame)
        """
        self.state = self.state.joy_button_up( event )

    def joy_button_down( self, event ):
        """
        Reports a Pygame's joy button down event to the active state.
        @param event: A Pygame JOYBUTTONDOWN event
        @type event: Event(Pygame)
        """
        self.state = self.state.joy_button_down( event )

    def video_resize( self, event ):
        """
        Reports a Pygame's video resize event to the active state.
        @param event: A Pygame VIDEORESIZE event
        @type event: Event(Pygame)
        """
        self.state = self.state.video_resize( event )

    def video_expose( self, event ):
        """
        Reports a Pygame's video expose event to the active state.
        @param event: A Pygame VIDEOEXPOSE event
        @type event: Event(Pygame)
        """
        self.state = self.state.video_expose( event )

    def user_event( self, event ):
        """
        Reports a Pygame's user event to the active state.
        @param event: A Pygame USEREVENT event
        @type event: Event(Pygame)
        """
        self.state = self.state.user_event( event )

    def update( self ):
        """Reports an update event to the active state."""
        self.state.update()

    def draw( self ):
        """Reports a draw event to the active state."""
        self.state.draw()

    def start( self ):
        """Reset the VM to the Mouse state."""
        self.state = Mouse()

    def main( self ):
        """
        Init the main loop of the engine, open a display window, launch events to the
        active state, update and render the scene each frame. if StopScene exception is launched,
        the VM stop self, and close the window.If however SceneChange exception is launched,
        the VM will reset single with the new scene data without close the window.
        """
        self.start()
        self.display.open()
        self.scene.start()
        leave = False
        while not leave:
            try:
                self.clock.tick()
                for event in pygame.event.get():
                    self.event[ event.type ]( event )
                self.state.update()
                self.state.draw()
                self.display.flip()
            except ChangeScene, e:
                self.scene.stop()
                self.scene = e.scene
                self.scene.start()
            except StopVM:
                leave = True
        self.display.close()

def boot( scene, display, clock=None, mouse=None  ):
    """
    Boot a scene. Prepare a Virtual Machine and
    start running the main loop.
    @param scene: A Scene object
    @type scene: Scene
    @param clock: A Clock object
    @type clock: Clock
    @param display: A Display object
    @type display: Display
    @param mouse: A Mouse object
    @type mouse: Mouse
    """
    try:
        import psyco
        psyco.full()
        Logger().info("Psyco enabled")
    except ImportError:
        pass
    if not isinstance( clock, NoneType ): VM().clock = clock
    if not isinstance( mouse, NoneType ): VM().mouse = mouse
    VM().scene = scene
    VM().display = display
    VM().main()


class VMState( State ):
    """
    This class is a abstract state of the VM, the pre-mades modes of VM inherit from
    this class. You can inherit it to write your own modes (states).
    VMState recieves the calls of the VM (Pygame events), transforms and process them to
    check if was a click, a doubleclick, a key pressed, key released, etc..., check if
    the mouse collides with any object, and depending of the VMState setted on VM,
    will launch high-level events to the scene instance.
    """

    def __init__( self ):
        """Build a VMState object."""
        State.__init__( self )


    def quit( self ):
        """Reports a Pygame's quit event to the Scene."""
        VM().scene.quit()
        return self

    def active_event( self, event ):
        """
        Reports a Pygame's active event to the Scene.
        @param event: A Pygame's ACTIVEEVENT event
        @type event: Event(Pygame)
        """
        VM().scene.active_event( event )
        return self

    def key_down( self, event ):
        """
        Reports a Pygame's key down event to the Scene.
        @param event: A Pygame's KEYDOWN event
        @type event: Event(Pygame)
        """
        VM().scene.key_down( event )
        return self

    def key_up( self, event ):
        """
        Reports a Pygame's key up event to the Scene.
        @param event: A Pygame's KEYUP event
        @type event: Event(Pygame)
        """
        VM().scene.key_up( event )
        return self

    def mouse_motion( self, event ):
        """
        Reports a Pygame's mouse motion event to the Scene.
        @param event: A Pygame's MOUSEMOTION event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_motion( event )
        return self

    def mouse_button_up( self, event ):
        """
        Reports a Pygame's mouse button up event to the Scene.
        @param event: A Pygame's MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_button_up( event )
        return self

    def mouse_button_down( self, event ):
        """
        Reports a Pygame's mouse button down event to the Scene.
        @param event: A Pygame's MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_button_down( event )
        return self

    def joy_axis_motion( self, event ):
        """
        Reports a Pygame's joy axis motion event to the Scene.
        @param event: A Pygame's JOYAXISMOTION event
        @type event: Event(Pygame)
        """
        VM().scene.joy_axis_motion( event )
        return self

    def joy_ball_motion( self, event ):
        """
        Reports a Pygame's joy ball motion event to the Scene.
        @param event: A Pygame's JOYBALLMOTION event
        @type event: Event(Pygame)
        """
        VM().scene.joy_ball_motion( event )
        return self

    def joy_hat_motion( self, event ):
        """
        Reports a Pygame's joy hay motion event to the Scene.
        @param event: A Pygame's JOYHATMOTION event
        @type event: Event(Pygame)
        """
        VM().scene.joy_hat_motion( event )
        return self

    def joy_button_up( self, event ):
        """
        Reports a Pygame's joy button up event to the Scene.
        @param event: A Pygame's JOYBUTTONUP event
        @type event: Event(Pygame)
        """
        VM().scene.joy_button_up( event )
        return self

    def joy_button_down( self, event ):
        """
        Reports a Pygame's joy button down event to the Scene.
        @param event: A Pygame's JOYBUTTONDOWN event
        @type event: Event(Pygame)
        """
        VM().scene.joy_button_down( event )
        return self

    def video_resize( self, event ):
        """
        Reports a Pygame's video resize event to the Scene.
        @param event: A Pygame's VIDEORESIZE event
        @type event: Event(Pygame)
        """
        VM().scene.video_resize( event )
        return self

    def video_expose( self, event ):
        """
        Reports a Pygame's video expose event to the Scene.
        @param event: A Pygame's VIDEOEXPOSE event
        @type event: Event(Pygame)
        """
        VM().scene.video_expose( event )
        return self

    def user_event( self, event ):
        """
        Reports a Pygame's user event to the Scene.
        @param event: A Pygame's USEREVENT event
        @type event: Event(Pygame)
        """
        VM().scene.user_event( event )
        return self

    def update( self ):
        """Forwards the update event to the Scene."""
        VM().scene.update()
        return self

    def draw( self ):
        """Forwards the draw event to the Scene."""
        VM().scene.draw()
        return self


class Mouse( VMState ):
    """
    Mouse is a VM State that does picking and mouse related operations.
    It generates mouse_click, mouse_double_click, mouse_start_drag,
    mouse_end_drag and mouse_motion events.
    This class is a Singleton, so when setting the VM's active state you
    can program it like this:
        VM().state = Mouse()
    """

    # Bit Flags
    BTN_PRESS_LEFT       = 1
    BTN_PRESS_CENTER     = 1<<1
    BTN_PRESS_RIGHT      = 1<<2
    BTN_CLICK_LEFT       = 1<<4
    BTN_CLICK_CENTER     = 1<<5
    BTN_CLICK_RIGHT      = 1<<6
    BTN_DBL_CLICK_LEFT   = 1<<8
    BTN_DBL_CLICK_CENTER = 1<<9
    BTN_DBL_CLICK_RIGHT  = 1<<10
    BTN_DRAG_LEFT        = 1<<12
    BTN_DRAG_CENTER      = 1<<13
    BTN_DRAG_RIGHT       = 1<<14

    # Button index, numbered as in Pygame's Events


    # Singleton's shared state
    _shared_state = {}

    def __init__( self ):
        """Singletonize a NormalMode object."""
        self.__dict__ = self._shared_state
        if self.__dict__: return
        VMState.__init__( self )
        # Button flags
        self._flag = 0
        # Button click time
        self._time = [ None ] * 4
        # Button down position
        self._location = [ None ] * 4
        # Mouse is over this objects
        self._over = []
        # Collided objects by button pressed
        self._btn_collided = [ [] ] * 4
        # Collided objects list
        self._last_collided = []
        # Mouse goes into this objects
        self._mouse_in = []
        # Mouse goes out of this objects
        self._mouse_out = []

    def mouse_motion( self, event ):
        """
        Report a mouse motion event to the Scene.
        @param event: A Pygame KEYDOWN event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_motion( event )
        location = VM().mouse.location.clone()
        self._process_mouse_collision( location )
        VM().scene.on_mouse_motion( Event( {
            "location" : location,
            "object"   : self._over[:] } ) )
        return self

    def mouse_button_down( self, event ):
        """
        Receives a mouse pressed from Pygame and activates the
        flag bits and sets the drag start locations if required.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_button_down( event )
        if event.button == B_LEFT:
            self._process_mouse_button_down(
                B_LEFT, self.BTN_PRESS_LEFT )
        elif event.button == B_CENTER:
            self._process_mouse_button_down(
                B_CENTER, self.BTN_PRESS_CENTER )
        elif event.button == B_RIGHT:
            self._process_mouse_button_down(
                B_RIGHT, self.BTN_PRESS_RIGHT )
        return self

    def mouse_button_up( self, event ):
        """
        Receives a mouse release from Pygame and deactivates the
        flag bits and resets the clicked timers if required.
        @param event: A Pygame event
        @type event: Event(Pygame)
        """
        VM().scene.mouse_button_up( event )
        if event.button == B_LEFT:
            self._process_mouse_button_up(
                B_LEFT,
                self.BTN_PRESS_LEFT,
                self.BTN_CLICK_LEFT,
                self.BTN_DBL_CLICK_LEFT,
                self.BTN_DRAG_LEFT )
        elif event.button == B_CENTER:
            self._process_mouse_button_up(
                B_CENTER,
                self.BTN_PRESS_CENTER,
                self.BTN_CLICK_CENTER,
                self.BTN_DBL_CLICK_CENTER,
                self.BTN_DRAG_CENTER )
        elif event.button == B_RIGHT:
            self._process_mouse_button_up(
                B_RIGHT,
                self.BTN_PRESS_RIGHT,
                self.BTN_CLICK_RIGHT,
                self.BTN_DBL_CLICK_RIGHT,
                self.BTN_DRAG_RIGHT )
        return self


    """
    def _process_mouse_collision( self, l_mouse ):
        self._last_collided = []
        self._mouse_in      = []
        self._mouse_out     = []
        point = box.Point( l_mouse )
        for obj in VM().scene.sorted:
            box_ = obj.collides( point )
            if not isinstance( box_, NoneType ):
                self._last_collided.append( obj )
                if obj not in self._over:
                    self._mouse_in.append( obj )
                    self._over.append( obj )
            else:
                try:
                    idx = self._over.index( obj )
                    self._mouse_out.append( obj )
                    self._over.pop( idx )
                except ValueError:
                    pass
    """
    def _process_mouse_collision( self, l_mouse ):
        self._last_collided = []
        #self._mouse_in      = []
        #self._mouse_out     = []
        point = Point( l_mouse )
        for i in xrange( len( self._over )-1, -1, -1 ):
            box_ = self._over[i].collides( point )
            if not isinstance( box_, NoneType ): continue
            self._mouse_out.append( self._over.pop( i ) )

        for obj in VM().scene.sorted:
            if obj in self._over:
                self._last_collided.append( obj )
            elif obj not in self._mouse_out:
                box_ = obj.collides( point )
                if isinstance( box_, NoneType ): continue
                self._mouse_in.append( obj )
                self._over.append( obj )

    def _process_mouse_button_down( self, btn, btn_press ):
        """ """
        # Set the pressed flag
        self._flag |= btn_press
        # Record the current location of the mouse
        self._location[ btn ] = VM().mouse.location
        # Record the collided objects right now
        self._btn_collided[ btn ] = self._last_collided[:]
        # Send the event
        VM().scene.on_mouse_button_down( Event( {
            "location" : self._location[ btn ].clone(),
            "object"   : self._btn_collided[ btn ][:],
            "button"   : btn } ) )

    def _process_mouse_button_up( self,
        btn, btn_press, btn_click, btn_dbl_click, btn_drag ):
        """ """
        # Unset the pressed bit
        self._flag &= ~btn_press
        # Button clicked?
        if self._flag & btn_click:
            # Then this is a double click
            self._flag &= ~btn_click
            # ... set the double click flag
            # update() will take care of it
            self._flag |= btn_dbl_click
        # The button is not clicked, this is the first click
        elif not ( self._flag & btn_drag ):
            # The user has clicked one time
            # set the flag bit
            self._flag |= btn_click
            # Start the timer
            self._time[ btn ] = VM().clock.time
        # Send the event
        VM().scene.on_mouse_button_up( Event( {
            "location" : VM().mouse.location.clone(),
            "object"   : self._over[:],
            "button"   : btn } ) )

    def _process_update_button( self,
        l_mouse, d_drag, t_click, t_now,
            btn, btn_press, btn_click, btn_dbl_click, btn_drag ):
        """ """
        # Left Button
        # Button double clicked?
        if self._flag & btn_dbl_click:
            # Unset the double click flag
            self._flag &= ~btn_dbl_click
            # ... send the event
            # no need to copy here!, the user can trash the objects
            VM().scene.on_mouse_double_click( Event( {
                "object"   : self._btn_collided[ btn ],
                "location" : self._location[ btn ],
                "button"   : btn } ) )
        # Button pressed?
        elif self._flag & btn_press:
            # Mouse not dragging?, Start a drag?
            # Only after distance_drag pixels moved
            if not ( self._flag & btn_drag ) \
            and ( ( self._location[ btn ] - l_mouse ).length() > d_drag ):
                # Start dragging, set the drag bit
                self._flag |= btn_drag
                # ... launch the event
                # no need to copy here!, the user can trash the objects
                VM().scene.on_mouse_drag_start( Event( {
                    "object"   : self._btn_collided[ btn ],
                    "location" : self._location[ btn ],
                    "button"   : btn } ) )
        # There is no button pressed, Is the mouse dragging?
        elif self._flag & btn_drag:
            # If it is stop dragging, unset the bit
            self._flag &= ~btn_drag
            # ... and send the event
            VM().scene.on_mouse_drag_end(
                    Event( {
                        "object"   : self._last_collided[:],
                        "location" : l_mouse,
                        "button"   : btn } ) )
        # There is no button pressed, was the button clicked?
        elif self._flag & btn_click \
        and ( t_now - self._time[ btn ] ) > t_click:
            # If it is clicked and the double click timeout expired
            # unset the clicked bit
            self._flag &= ~btn_click
            # ... and send the event
            # no need to copy here!, the user can trash the objects
            VM().scene.on_mouse_click(
                Event( {
                    "object"   : self._btn_collided[ btn ],
                    "location" : self._location[ btn ],
                    "button"   : btn } ) )

    def update( self ):
        """Here the flags, timers and start locations are checked
        and acted upon their value. This method generates mouse_start_drag,
        mouse_end_drag, mouse_click, mouse_double_click and mouse_motion
        events."""
        # Local variables, reduce call overhead
        l_mouse   = VM().mouse.location
        d_drag    = VM().mouse.drag_distance
        t_click   = VM().mouse.double_click_time
        t_now     = VM().clock.time

        # Send mouse in/out
        if self._mouse_in:
            VM().scene.on_mouse_in(
                Event( { "location" : l_mouse, "object" : self._mouse_in } ) )
            self._mouse_in = []
        if self._mouse_out:
            VM().scene.on_mouse_out(
                Event( { "location" : l_mouse, "object" : self._mouse_out } ) )
            self._mouse_out = []
        # Process the left button
        self._process_update_button(
            l_mouse, d_drag, t_click, t_now,
            B_LEFT,
            self.BTN_PRESS_LEFT,
            self.BTN_CLICK_LEFT,
            self.BTN_DBL_CLICK_LEFT,
            self.BTN_DRAG_LEFT )
        # Process the center button
        self._process_update_button(
            l_mouse, d_drag, t_click, t_now,
            B_CENTER,
            self.BTN_PRESS_CENTER,
            self.BTN_CLICK_CENTER,
            self.BTN_DBL_CLICK_CENTER,
            self.BTN_DRAG_CENTER )
        # Process the right button
        self._process_update_button(
            l_mouse, d_drag, t_click, t_now,
            B_RIGHT,
            self.BTN_PRESS_RIGHT,
            self.BTN_CLICK_RIGHT,
            self.BTN_DBL_CLICK_RIGHT,
            self.BTN_DRAG_RIGHT )

        # Update via the parent
        return VMState.update( self )

class Passive( VMState ):
    """
    This state of the VM, ignores all Pygame's events, so it gets the
    events and does not forward them. The only forwarded events are
    quit, draw and update.
    Passive is the best VM State, for game-intros, movie-modes and
    other situations where your scene does not require events.
    """
    # Singleton's shared state
    _shared_state = {}

    def __init__( self ):
        """Singletonize a PassiveMode object."""
        self.__init__ = self._shared_state
        if self.__init__: return
        VMState.__init__( self )

    def active_event( self, event ):
        """
        Ignores the Pygame's active event.
        @param event: A Pygame's ACTIVEEVENT event
        @type event: Event(Pygame)
        """
        return self

    def key_down( self, event ):
        """
        Ignores the Pygame's key down event.
        @param event: A Pygame's KEYDOWN event
        @type event: Event(Pygame)
        """
        return self

    def key_up( self, event ):
        """
        Ignores the Pygame's key up event.
        @param event: A Pygame's KEYUP event
        @type event: Event(Pygame)
        """
        return self

    def mouse_motion( self, event ):
        """
        Ignores the Pygame's mouse motion event.
        @param event: A Pygame's MOUSEMOTION event
        @type event: Event(Pygame)
        """
        return self

    def mouse_button_up( self, event ):
        """
        Ignores the Pygame's mouse button up event.
        @param event: A Pygame's MOUSEBUTTONUP event
        @type event: Event(Pygame)
        """
        return self

    def mouse_button_down( self, event ):
        """
        Ignores the Pygame's mouse button down event.
        @param event: A Pygame's MOUSEBUTTONDOWN event
        @type event: Event(Pygame)
        """
        return self

    def joy_axis_motion( self, event ):
        """
        Ignores the Pygame's joy axis motion event.
        @param event: A Pygame's JOYAXISMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_ball_motion( self, event ):
        """
        Ignores the Pygame's joy ball motion event.
        @param event: A Pygame's JOYBALLMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_hat_motion( self, event ):
        """
        Ignores the Pygame's joy hay motion event.
        @param event: A Pygame's JOYHATMOTION event
        @type event: Event(Pygame)
        """
        return self

    def joy_button_up( self, event ):
        """
        Ignores the Pygame's joy button up event.
        @param event: A Pygame's JOYBUTTONUP event
        @type event: Event(Pygame)
        """
        return self

    def joy_button_down( self, event ):
        """
        Ignores the Pygame's joy button down event.
        @param event: A Pygame's JOYBUTTONDOWN event
        @type event: Event(Pygame)
        """
        return self

    def video_resize( self, event ):
        """
        Ignores the Pygame's video resize event.
        @param event: A Pygame's VIDEORESIZE event
        @type event: Event(Pygame)
        """
        return self

    def video_expose( self, event ):
        """
        Ignores the Pygame's video expose event.
        @param event: A Pygame's VIDEOEXPOSE event
        @type event: Event(Pygame)
        """
        return self

    def user_event( self, event ):
        """
        Ignores the Pygame's user event.
        @param event: A Pygame's USEREVENT event
        @type event: Event(Pygame)
        """
        return self

class Conversation( Mouse ):
    """
    On this state, the mouse only collides with the visual elements of the
    dialog interface (HUD) and ignores all the other objects...
    The HUD is the class that handdle the visual interface of the dialogs.
    Conversation is the best VM state when your scene is undergoing a dialog
    between actors.
    """
    pass
