from types import NoneType, GeneratorType
import heapq

Continue = None
Stop = False

class LockMachine( object ):
	def __init__( self, thread ): self._thread = thread
	def get_thread( self ): return self._thread
	def __cmp__( self, o ): return self._thread.__cmp__( o )
	thread = property( get_thread )

class LightThread( object ):
	"""A lightweigh thread, simulates the hard Python Thread,
	create a subclass and override run, then insert it on the
	scheduler"""
	def __init__( self ): self._stop = False
	def stop( self ): self._stop = True
	def isAlive( self ): return not self._stop
	def __cmp__( self, o ):
		"""Compare this Thread"""
		raise NotImplemented
	def run( self ):
		"""Override this, yield Continue or yield Stop
		return stops the iteration"""
		raise NotImplemented

class LightScheduler( object ):
	"""A Lightweight Scheduler based on:
	Implementing "weightless threads" with Python generators
	http://www-128.ibm.com/developerworks/library/l-pythrd.html
	"""
	def __init__( self ): self.init()
	
	def init( self ):
		self._waiting = PriorityQueue()
		self._running = []
		self._next    = []
		self._lock    = None
	
	def get_running( self ): return self._running
	def set_running( self, running ): self._running = running
	def get_waiting( self ): return self._waiting
	def set_waiting( self, waiting ): self._waiting = waiting
	
	def insert( self, thread ):
		# If it is a Wait: block the machine, do not
		# start more threads till the lock stops
		self._waiting.insert( thread )
		if isinstance( thread, LockMachine ):
			return thread.thread
		return thread
	
	def halt( self ):
		"""Stop every thread and execute its last iteration"""
		for i in xrange( len( self._running ) - 1, -1, -1 ):
			self._running[ i ].stop()
			try: self._next[ i ].next()
			except StopIteration: pass
		# Init everything
		self.init()

	def update( self ):
		"""Update everything if we are not locked"""
		# Run a step of each thread
		for i in xrange( len( self._running ) - 1, -1, -1 ):
			try:
				# Iterate one step
				# If generator returned value is not None,
				# thread ended; assert it
				assert isinstance( self._next[ i ], GeneratorType )
				assert isinstance( self._next[ i ].next(), NoneType )
			except ( StopIteration, AssertionError ):
				# If we are here the thread is dead
				# Mark the thread stopped
				self._running[ i ].stop()
			# If the thread is not alive, delete it
			if not self._running[ i ].isAlive():
				self._next.pop( i )
				self._running.pop( i )
		
		# If the queue is locked (Waiting) return now
		if isinstance( self._lock, LockMachine )\
			and self._lock.thread.isAlive(): return
		# No locking
		self._lock = None
		# Pop from the queue and put threads in the front
		# of the list; run the first iteration
		while len( self._waiting )\
		and not isinstance( self._lock, LockMachine ):
			t = self._waiting.pop()
			if isinstance( t, LockMachine ):
				self._lock = t
				t = self._lock.thread
			self._next.insert( 0, t.run() )
			self._running.insert( 0, t )
	
	def __str__( self ):
		return """\
LightScheduler
---------+-------------- -- --  - -
         | running: %d waiting: %d
 running | %s
    next | %s
 waiting | %s""" % (
	len( self._running ),
	len( self._waiting ),
	self._running,
	self._next,
	self._waiting )

	running = property( get_running, set_running )
	waiting = property( get_waiting, set_waiting )

class PriorityQueue( list ):
	def insert( self, item ):
		heapq.heappush( self, item )
		return item
	def pop( self ):
		return heapq.heappop( self )

