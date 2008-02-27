#    PySCUMM Engine. SCUMM based engine for Python
#    Copyright (C) 2008  PySCUMM Engine. http://pyscumm.org
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

import pyscumm, pygame
print dir(pyscumm)


class PosterItem(pyscumm.Item):

    def __init__(self):
        pyscumm.Item.__init__(self)
        self.image = pyscumm.resource.load('Item1.png')
        self.position.x, self.position.y, self.position.z = 70, 225, 1
        self.description = 'Welcome poster'


class BoneItem(pyscumm.Item):

    def __init__(self):
        pyscumm.Item.__init__(self)
        self.image = pyscumm.resource.load('Item2.png')
        self.position.x, self.position.y, self.position.z = 700, 400, 2
        self.description = 'Ridiculous arm bone'


class BeachRoom(pyscumm.Room):

    def __init__(self):
        pyscumm.Room.__init__(self)
        self.background = pyscumm.resource.load('Background1.png')
        self.add(PosterItem())
        self.add(BoneItem())

    def update(self):
        #for d in self.container:
        #    print d.position.z
        pass

    def on_event(self, e):
        if e['type'] == pyscumm.KEY_DOWN:
            if e['key'] == pyscumm.K_RIGHT:
                self.camera.position.x += 20
            elif e['key'] == pyscumm.K_LEFT:
                self.camera.position.x -= 20
            elif e['key'] == pyscumm.K_F12:
                print pyscumm.engine.clock.fps

# Create a Engine, and run the Playa room
pyscumm.engine.display.title = 'PySCUMM Demo Adventure'
pyscumm.engine.run(BeachRoom)

