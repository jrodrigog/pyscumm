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

from pygame.constants import *

# Mouse Button Constants
B_LEFT   = 1
B_CENTER = 2
B_RIGHT  = 3

UPDATED     = 1
UPDATE_MASK = {
    "location"  : 1<<1,
    "insertion" : 1<<2,
    "rotation"  : 1<<3,
    "scale"     : 1<<4,
    #..................
    "size"      : 1<<5,
    "color"     : 1<<6,
    "speed"     : 1<<7,
    #..................
    "collider"  : 1<<8,
    "copy"      : 1<<9,
    #..................
    "name"      : 1<<10,
    "visible"   : 1<<11,
    "frozen"    : 1<<12,
    "solver"    : 1<<13,
    "child"     : 1<<14,
}

LOCATION_UPDATED  = UPDATE_MASK["location"]
INSERTION_UPDATED = UPDATE_MASK["insertion"]
ROTATION_UPDATED  = UPDATE_MASK["rotation"]
SCALE_UPDATED     = UPDATE_MASK["scale"]
SIZE_UPDATED      = UPDATE_MASK["size"]
COLOR_UPDATED     = UPDATE_MASK["color"]
SPEED_UPDATED     = UPDATE_MASK["speed"]
COLLIDER_UPDATED  = UPDATE_MASK["collider"]
COPY_UPDATED      = UPDATE_MASK["copy"]
NAME_UPDATED      = UPDATE_MASK["name"]
VISIBLE_UPDATED   = UPDATE_MASK["visible"]
FROZEN_UPDATED    = UPDATE_MASK["frozen"]
SOLVER_UPDATED    = UPDATE_MASK["solver"]
CHILD_UPDATED     = UPDATE_MASK["child"]

TRANSFORMED = \
      UPDATE_MASK["location"] \
    | UPDATE_MASK["insertion"] \
    | UPDATE_MASK["rotation"] \
    | UPDATE_MASK["scale"]

