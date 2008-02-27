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

from base import StateMachine, StopEngine, ChangeRoom, debugger
from driver import Mouse, Display, Clock
from constant import MOUSE_MOTION, DOUBLE_CLICK, SINGLE_CLICK, KEY_DOWN, KEY_UP, DRAG_START, DRAG_END

import pygame.time
import pygame.event



class Engine(StateMachine):

    def __init__( self ):
        StateMachine.__init__(self)
        self.mouse = Mouse()
        self.display = Display()
        self.clock = Clock()
        self.__dragging = [ 0, 0, 0 ]
        self.__button_time = [ 0, 0, 0 ]

    def run(self, room):
        pygame.init()
        debugger.info("turning ON engine...")
        try:
            import psyco
            psyco.full()
            debugger.info("python-psyco module found, performance acelerarion enabled")
        except ImportError:
            debugger.warn("python-psyco module not found, performance aceleration unavaliable")

        self.display.open()
        self.room = room()
        leave = False
        while not leave:
            try:
                self.clock.tick()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise StopEngine()
                    elif event.type == pygame.MOUSEMOTION:
                        event_dict = { "type":MOUSE_MOTION, "pos":self.mouse.position, "obj":self._get_picked()  }
                        debugger.info("MOUSE_MOTION event launched %s" % event_dict)
                        self.room.on_event(event_dict)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.__process_mouse_button_down( event )
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.__process_mouse_button_up( event )
                        #self.room.on_event(event)
                    elif event.type == pygame.KEYDOWN:
                        event_dict = { "type":KEY_DOWN, "key":event.key, "mod":"NotImplemented" }
                        debugger.info("KEY_DOWN event launched %s" % event_dict)
                        self.room.on_event(event_dict)
                    elif event.type == pygame.KEYUP:
                        event_dict = { "type":KEY_UP, "key":event.key, "mod":"NotImplemented" }
                        debugger.info("KEY_UP event launched %s" % event_dict)
                        self.room.on_event(event_dict)
                self.__update()
                # Sort the container list by Z axis.
                #self.room.container.sort(key=lambda d: d.position.z)
                # Call update the room
                self.room.update()
                self.room.draw()
                self.mouse.update()
                self.mouse.draw()
                self.display.flip()
            except ChangeRoom, e:
                debugger.info("ChangeRoom exception raised, changing room to %s" % e.__class__.__name__)
                self.room = e
            except StopEngine:
                debugger.info("stopping Engine...")
                leave = True
        self.display.close()
        debugger.info("engine totally stopped, exiting")

    def __process_mouse_button_down(self, event):
        if event.button not in [1,2,3]:
            return
        # Check if DOUBLE_CLICK
        if self.clock.time - self.__button_time[event.button-1] < self.mouse.doubleclick_time:
            event_dict = { "type":DOUBLE_CLICK, "btn":event.button, "obj":self._get_picked(), "pos":self.mouse.position  }
            debugger.info("DOUBLE_CLICK event launched %s" % event_dict)
            self.room.on_event(event_dict)
            self.__dragging[event.button-1] = 0
        else:
            self.__button_time[event.button-1] = self.clock.time
        # Prepare a possible a DRAG_START
            self.__dragging[event.button-1] = self.clock.time

    def _get_picked(self):
        picked = []
        m_pos = self.mouse.position
        for obj in self.room.container:
            if obj.collider.collidepoint(m_pos.x, m_pos.y):
                picked.append(obj)
        picked.sort(key=lambda d: d.position.z)
        return picked

    def __process_mouse_button_up(self, event):
        if self.__dragging[event.button-1]:
            event_dict = { "type":SINGLE_CLICK, "btn":event.button, "obj":self._get_picked(), "pos":self.mouse.position  }
            debugger.info("SINGLE_CLICK event launched %s" % event_dict)
            self.room.on_event( event_dict )
            self.__dragging[event.button-1] = 0
        else:
            event_dict = { "type":DRAG_END, "btn":event.button, "obj":self._get_picked(), "pos":self.mouse.position  }
            debugger.info("DRAG_END event launched %s" % event_dict)
            self.room.on_event( event_dict )

    def __update(self):
        for list_pos, x in enumerate(self.__dragging):
            if self.__dragging[list_pos]:
                if ( self.clock.time - self.__dragging[list_pos] ) >= self.mouse.drag_time:
                    event_dict = { "type":DRAG_START, "btn":"NotImplementedError", "obj":self._get_picked(), "pos":self.mouse.position  }
                    debugger.info("DRAG_START event launched %s" % event_dict)
                    self.room.on_event( event_dict )
                    self.__dragging[list_pos] = 0



engine = Engine()
