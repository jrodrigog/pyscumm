from types import NoneType
from lt import LightThread, LockMachine

class Action( LightThread ):
	PRIORITY_LOWEST  = 21
	PRIORITY_LOW     = 10
	PRIORITY_NORMAL  = 0
	PRIORITY_HIGH    = -10
	PRIORITY_HIGHEST = -21
	def __init__( self, target=None, priority=PRIORITY_NORMAL ):
		LightThread.__init__( self )
		self._target = target
		self._priority = priority
	def __cmp__( self, o ):
		return cmp( self.priority, o.priority )
	def get_priority( self ): return self._priority
	def set_priority( self, priority ): self._priority = priority
	def get_target( self ): return self._target
	def set_target( self, target ): self._target = target
	priority = property( get_priority, set_priority )
	target = property( get_target, set_target )

class ActionScript( Action, list ):
	def __init__( self, target=None ):
		Action.__init__( self, target=target )
		list.__init__( self )
	def start( self ):
		self.run()
	def run( self ):
		if not isinstance( self._target, NoneType ):
			for action in self:
				self._target.action( action )

class Use( Action ):
	def __init__( self, object=None, priority=Action.PRIORITY_NORMAL ):
		Action.__init__( self, priority=priority )
		self._object = object
	def run( self ):
		if not ( isinstance( self._object, NoneType )\
		or isinstance( self._target, NoneType ) ):
			return self._target.on_use( self._object )
	def get_object( self ): return self._object
	def set_object( self, object ): self._object = object
	object = property( get_object, set_object )
	
class Walk( Action ):
	def __init__( self, room=None, to=None, priority=Action.PRIORITY_NORMAL ):
		Action.__init__( self, priority=priority )
		self._room = room
		self._to = to
	def run( self ):
		if not ( isinstance( self._room, NoneType )\
		or isinstance( self._to, NoneType )\
		or isinstance( self._target, NoneType ) ):
			return self._target.on_walk( self._room, self._to )
	def get_room( self ): return self._room
	def set_room( self, room ): self._room = room
	def get_to( self ): return self._to
	def set_to( self, to ): self._to = to
	room = property( get_room, set_room )
	to = property( get_to, set_to )

class Look( Action ):
	def __init__( self, object=None, priority=Action.PRIORITY_NORMAL ):
		Action.__init__( self, priority=priority )
		self._object = object
	def run( self ):
		if not ( isinstance( self._object, NoneType )\
		or isinstance( self._target, NoneType ) ):
			return self._target.on_look( self._object )
	def get_object( self ): return self._object
	def set_object( self, object ): self._object = object
	object = property( get_object, set_object )
	
class Talk( Action ):
	def __init__( self, object=None, priority=Action.PRIORITY_NORMAL ):
		Action.__init__( self, priority=priority )
		self._object = object
	def run( self ):
		if not ( isinstance( self._object, NoneType )\
		or isinstance( self._target, NoneType ) ):
			return self._target.on_talk( self._object )
	def get_object( self ): return self._object
	def set_object( self, object ): self._object = object
	object = property( get_object, set_object )

class Wait( Action, LockMachine ):
	def __init__( self, action ):
		Action.__init__( self )
		LockMachine.__init__( self, action )
	def get_priority( self ): return self._thread.priority
	def set_priority( self, priority ): self._thread.priority = priority
	def get_target( self ): return self._thread.target
	def set_target( self, target ): self._thread.target = target
	target = property( get_target, set_target )
	priority = property( get_priority, set_priority )
