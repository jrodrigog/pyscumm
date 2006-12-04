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

import base.State

class ObjectState( base.State ):

    def __cmp__( self ):
        # TODO
        pass

    def get_scene( self ):
        # TODO
        pass

    def set_scene( self ):
        # TODO
        pass

    def get_vm( self ):
        # TODO
        pass

    def set_vm( self ):
        # TODO
        pass

    def Action( self, object, cmd ):
        # TODO
        pass

    def update( self, obj ):
        # TODO
        pass

    def draw( self, obj ):
        # TODO
        pass

    def collide( self, obj ):
        # TODO
        pass


class ItemState( ObjectState ):

    def on_use( self, item, obj ):
        pass


class ActorState( ObjectState ):

    def on_walk( self, actor, room, to ):
        pass

    def on_use( self, actor, object ):
        pass

    def on_look( self, actor, object ):
        pass

    def on_talk( self, actor, object ):
        pass


class InventoryState( ObjectState ):
    pass


class CursorState( ObjectState ):
    pass


class RoomState( ObjectState ):
    pass


class ActionBoxState( ObjectState ):
    pass


class HudState( ObjectState ):
    pass
