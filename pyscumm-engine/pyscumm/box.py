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
@since: 18/02/2007
"""

class WalkableBox(Box):

    def __init__(self, points, zplane, scale, light):
        Box.__init__(self, points)
        self.z = zplane
        self.scale = scale
        self.light = light


class Box:

    def __init__(self, points):
        self._vertex = points

    def vertex(self):
        return self._vertex

    def point_inside(self, point):
        """
        Check if a point are inside the box
        @param point: The point to check collition
        @type point: Tuple (x,y)
        @return: True if the point are colliding or False if not colliding
        @rtype: boolean
        """
        n = len(self._vertex)
        inside = False
        p1x, p1y = self._vertex[0]
        for i in range(n+1):
            p2x, p2y = self._vertex[i % n]
            if point[1] > min(p1y, p2y):
                if point[1] <= max(p1y, p2y):
                    if point[0] <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (point[1] - p1y) * (p2x - p1x) / \
                                      (p2y - p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def box_inside(self, other):
        """
        Check if a box are colliding with other box
        @param other: The box for check
        @type point: Box
        @return: True if are colliding or False if not colliding
        @rtype: boolean
        """
        for point in other.vertex():
            print 'checking', point, 'in', self._vertex
            if self.point_inside(point):
                return True
        return False



a=Box( ((0,0), (4,0), (4,4), (0,4)) )
b=Box( ((4,0), (10,0), (10,7), (7,8)) )
print a.box_inside(b)
