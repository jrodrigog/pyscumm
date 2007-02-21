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
@author: Juan Carlos Rodrigo Garcia (Brainsucker, jrodrigo@pyscumm.org)
@since: 20/11/2006
"""

import time


class StateMachine:
    """
    Abstract state machine (See: state pattern).
    """

    def __init__( self ):
        self.state = None

    def init( self ):
        """
        Start the state machine, this method need reimplementation
        on machine subclass, where you can start a machine with a state.
        if call this method without reimplement,
        a NotImplementedError excepcion is launched
        """
        raise NotImplementedError



class State( object ):
    """
    Abstract state (See: state pattern).
    """
    pass



class StopEngine( Exception ):
    pass



class ChangeRoom( Exception ):
    pass



class Debugger:
    """A Singleton Logger class"""

    _shared_state = {}

    def __init__( self ):
        """
        Build a Debugger object with Singleton pattern.
        """
        self.__dict__ = self._shared_state
        if self._shared_state: return
        self.visual  = True
        self.console = True

    def warn( self, message ):
        """
        Log a warning message.
        @param message: The message to log
        @type state: String
        """
        if not self.console: return
        print time.strftime('%H:%M:%S:')," warning : %s" % message

    def info( self, message ):
        """
        Log an info message.
        @param message: The message to log
        @type state: String
        """
        if not self.console: return
        print time.strftime('%H:%M:%S:')," info : %s" % message

    def error( self, message ):
        """
        Log an error message.
        @param message: The message to log
        @type state: String
        """
        if not self.console: return
        print time.strftime('%H:%M:%S:')," error : %s" % message
