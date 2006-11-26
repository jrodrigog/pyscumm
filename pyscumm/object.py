import box

import pyscumm.base


class Object( dict, pyscumm.base.StateMachine ):

    def __init__(self):
        dict.__init__( self )
        pyscumm.base.StateMachine.__init__( self )

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


class ObjectState( pyscumm.base.State ):

    def __init__( self ):
        pyscumm.base.State.__init__( self )

    def __cmp__( self ):
        raise NotImplemented

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
        pyscumm.base.StateMachine.__init__(self)


class CursorState( ObjectState ):

    def __init__( self ):
        pass



