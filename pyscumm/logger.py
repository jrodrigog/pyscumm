class Logger( object ):
    """A Logger Singleton class"""

    _shared_state = {}

    def __init__( self ):
        self.__dict__ = self._shared_state
        if self._shared_state: return
        self._visual = True

    def get_visual( self ):
        return self._visual

    def set_visual( self, visual ):
        self._visual = visual

    visual = property( get_visual, set_visual )
