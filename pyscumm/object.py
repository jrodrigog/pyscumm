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

from base import StateMachine, State

class Object( dict, StateMachine ):

    def __init__(self):
        dict.__init__( self )
        StateMachine.__init__( self )

    def __cmp__( self ):
        raise NotImplemented

    def action( self, cmd ):
        self._state = self._state.action( cmd )

    def collides( self, obj ):
        self._state = self._state.collides( obj )

    def update( self ):
        #self._state = self._state.update()
        pass

    def draw( self ):
        self._state = self._state.draw()


class ObjectState( State ):

    def __init__( self ):
        State.__init__( self )

    def action( self, cmd ):
        raise NotImplemented

    def collides( self, obj ):
        raise NotImplemented

    def update( self ):
        raise NotImplemented

    def draw( self ):
        raise NotImplemented


class Cursor( Object ):

    def __init__( self ):
        StateMachine.__init__(self)


class CursorState( ObjectState ):

    def __init__( self ):
        pass



