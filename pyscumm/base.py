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
@since: 9/11/2006
"""

import heapq

class StateMachine( object ):
    """
    Abstract state machine (See: state pattern).
    """

    def __init__( self ):
        self._state = None

    def start( self ):
        """
        Start the state machine, this method need reimplementation
        on machine subclass, where you can start a machine with a state.
        if call this method without reimplement,
        a NotImplementedError excepcion is launched
        """
        raise NotImplementedError

    def get_state( self ):
        """
        Get the active state of the machine.
        @return: State
        """
        return self._state

    def set_state( self, state ):
        """
        Set a new state in the machine.
        @param state: The new state to active.
        @type state: State Object
        """
        self._state = state

    state = property( get_state, set_state )


class State( object ):
    """
    Abstract state (See: state pattern).
    """
    pass


class Logger( object ):
    """A Singleton Logger class"""

    _shared_state = {}

    def __init__( self ):
        """Build a Logger object"""
        self.__dict__ = self._shared_state
        if self._shared_state: return
        self._visual = True

    def warn( self, message ):
        """
        Log a warn message.
        @param message: The message to log
        @type state: String
        """
        if not self._visual: return
        print "[pyscumm] warn : %s" % message

    def info( self, message ):
        """
        Log an info message.
        @param message: The message to log
        @type state: String
        """
        if not self._visual: return
        print "[pyscumm] info : %s" % message

    def error( self, message ):
        """
        Log an error message.
        @param message: The message to log
        @type state: String
        """
        if not self._visual: return
        print "[pyscumm] error : %s" % message

    def get_visual( self ):
        """
        Get the visual logging output state.
        @return: Visual logging state
        @rtype: bool
        """
        return self._visual

    def set_visual( self, visual ):
        """
        Set the visual logging output state, set this to
        False and it won't print logging messages.
        @param visual: Visual logging state
        @type visual: bool
        """
        self._visual = visual

    visual = property( get_visual, set_visual )

class SortedList( list ):
    """An ordered list."""
    def __init__( self, obj=[] ):
        self = heapq.heapify( obj )
    def insert( self, item ):
        """Insert an item maintaining the list ordered."""
        heapq.heappush( self, item )
        return item
    def pop( self ):
        """Pop the first item."""
        return heapq.heappop( self )
