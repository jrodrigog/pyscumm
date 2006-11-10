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



class StateMachine( object ):
	"""
	Abstract state machine (See: state pattern).
	"""

	def __init__( self ):
		self._state = None

	def start( self ):
		"""
		Start the state machine, this method need reimplementation
		on machine subclass, where you can start a machine with a state.if
		
		if call this method without reimplement,
		a NotImplementedError excepcion is launched
		"""
		raise NotImplementedError

	def get_state( self ):
		"""
		Get the active state of the machine
		
		@return: State
		"""
		return self._state

	def set_state( self, state ):
		"""
		Set a new state in the machine.
		
		@param state: The new state to active.
		@type state: State Object
		@return: None
		"""
		self._state = state

	state	= property( get_state, set_state )



class State( object ):
	"""
	Abstract state (See: state pattern).
	"""

	_instance = None

	def instance( self ):
		if not self._instance:
			self._instance = self()
		return self._instance
	
	instance	= classmethod( instance )
