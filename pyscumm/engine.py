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

"""
@author: Juan Jose Alonso Lara (KarlsBerg, jjalonso@pyscumm.org)
@since: 18/02/2007
"""

from base import StateMachine, State, StopEngine, ChangeRoom, Debugger
from driver import Mouse, Display, Clock
from constant import MOUSE_MOTION, DOUBLE_CLICK, SINGLE_CLICK, KEY_DOWN, KEY_UP, DRAG_START, DRAG_END

import pygame.time
import pygame.event



class Engine( StateMachine ):

    _shared_state = {}
    a = 0
    def __init__( self ):
        self.__dict__ = self._shared_state
        if self._shared_state: return
        StateMachine.__init__(self)
        self.mouse              = Mouse()
        self.display            = Display()
        self.clock              = Clock()
        self.__state_button     = [ 0, 0, 0 ]
        self.__time_button        = [ 0, 0, 0 ]

    def run( self, state ):
        Debugger().info("turning ON engine...")
        try:
            import psyco
            psyco.full()
            Debugger().info("python-psyco module found, performance acelerarion enabled")
        except ImportError:
            Debugger().warn("python-psyco module not found, performance aceleration unavaliable")

        self.display.open()
        self.state = state()
        self.state.init()
        leave = False
        while not leave:
            try:
                self.clock.tick()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise StopEngine()
                    elif event.type == pygame.MOUSEMOTION:
                        event_dict = { "type":MOUSE_MOTION, "pos":self.mouse.get_pos(), "obj":"NotImplemented"  }
                        Debugger().info("MOUSE_MOTION event launched %s" % event_dict)
                        self.state.on_event(event_dict)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__process_mouse_button_down( event )
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.__process_mouse_button_up( event )
                        #self.state.on_event(event)
                    elif event.type == pygame.KEYDOWN:
                        event_dict = { "type":KEY_DOWN, "key":event.key, "mod":"NotImplemented" }
                        Debugger().info("KEY_DOWN event launched %s" % event_dict)
                        self.state.on_event(event_dict)
                    elif event.type == pygame.KEYUP:
                        event_dict = { "type":KEY_UP, "key":event.key, "mod":"NotImplemented" }
                        Debugger().info("KEY_UP event launched %s" % event_dict)
                        self.state.on_event(event_dict)
                self.__update()
                self.state.update()
                self.state.draw()
                self.display.flip()
            except ChangeRoom, e:
                Debugger().info( "ChangeRoom exception raised, changing state to %s" % e.__class__.__name__ )
                self.state = e
                self.state.init()
            except StopEngine:
                Debugger().info( "stopping Engine..." )
                leave = True
        self.display.close()
        Debugger().info( "engine totally stopped, exiting" )

    def __process_mouse_button_down( self, event ):
        if event.button not in [1,2,3]: return
        self.__state_button[event.button-1] = True
        if self.clock.time - self.__time_button[event.button-1] < self.mouse.doubleclick_time:
            print "DOUBLE_CLICK"
            self.__time_button[event.button-1] = 0
        else:
            self.__time_button[event.button-1] = self.clock.time


    def __process_mouse_button_up( self, event ):
        if event.button not in [1,2,3]: return
        self.__state_button[event.button-1] = False
        if self.__time_button[event.button-1]:
            print 'SINGLE CLICK'
        elif not self.__time_button[event.button-1] and not self.__state_button[event.button-1]:
            print 'DRAG END'






    def __update( self ):
        for list_pos, x in enumerate(self.__state_button):
            if self.__time_button[list_pos]:
                if ( self.clock.time - self.__time_button[list_pos] ) >= self.mouse.drag_time and self.__state_button[list_pos]:
                    print 'DRAG START'
                    self.__time_button[list_pos] = 0

    def __draw( self ):
        self.state.draw()



class Room( State ):

    def __init__( self ):
        State.__init__(self)
        self.container = []

    def init( self ):
        print 'Me inician'

    def on_event( self, event_dict ):
        pass

    def update( self ):
        for obj in self.container:
            obj.update()

    def draw( self ):
        for obj in self.container:
            obj.draw()
