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
@author: Juan Jose Alonso Lara (KarlsBerg, kernel.no.found@gmail.com)
@since: 23/02/2008
"""


from base import State
from engine import engine

import pygame
from euclid import Vector2



class Room(State, object):

    def __init__(self):
        State.__init__(self)
        self.background = None
        self.camera = Camera()
        self._container = {}

    def get_container(self):
        return self._container

    def add(self, obj):
        self._container[obj] = obj

    def remove(self, obj):
        del self._container[obj]

    def on_event(self, event_dict):
        pass

    def update(self):
        for obj in self.container:
            obj.update()

    def draw(self):
        # Draw background
        pygame.display.get_surface().blit(self.background, -self.camera.position)
        # Draw objects
        # THIS MUST ORDER BY Z PLANE !!!
        obj_sorted = self._container.values()
        obj_sorted.sort(key=lambda d: d.position.z)
        for obj in obj_sorted:
            obj.update()
            obj.draw()

    container = property(get_container, None)



class Camera(object):

    def __init__(self):
        self._position = Vector2(0, 0)
        #self._rect = pygame.Rect(self._position, Engine().display.get_size())
        #pygame.display.get_surface().set_clip()

    def _get_position(self):
        return self._position

    def _set_position(self, p):
        print 'setting pos camera', p
        self._position = Vector2(*p)

    position = property(_get_position, _set_position)

