
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
