import pyscumm.vector
import types

class Collider( object ):
    def collides( self, collider ):
        raise NotImplementedError
    def update( self ):
        raise NotImplementedError
    def draw( self ):
        raise NotImplementedError

class Box( Collider ):
    def __init__( self, shadow=1., depth=1. ):
        self._shadow = shadow
        self._depth = depth
        self._box = BoxRect( self, [
            pyscumm.vector.Vector3D( [ -1., -1., 0. ] ),
            pyscumm.vector.Vector3D( [  1., -1., 0. ] ),
            pyscumm.vector.Vector3D( [  1.,  1., 0. ] ),
            pyscumm.vector.Vector3D( [ -1.,  1., 0. ] ) ] )
    def get_z( self ): return self._location[2]
    def set_z( self, z ): self._location[2] = z
    def get_shadow( self ): return self._shadow
    def set_shadow( self, shadow ): self._shadow = shadow
    def get_depth( self ): return self._depth
    def set_depth( self, depth ): self._depth = depth
    def get_box( self ): return self._box
    def set_box( self, box ): self._box = box

    def collides( self, collider ):
        if isinstance( collider, Point )\
        and self._box.point_inside( collider ):
            return self
        elif isinstance( collider, Box )\
        and self._box.box_inside( collider.box ):
            return self
        return None
    def __str__( self ):
        return "Box( location=%s, shadow=%s, depth=%s, box=%s )" % (
            self._location,
            self._shadow,
            self._depth,
            self._box )
    def update( self ):
        self._box.update()
    shadow   = property( get_shadow, set_shadow )
    depth    = property( get_depth, set_depth )
    box      = property( get_box, set_box )
    z        = property( get_z, set_z )

class Point( Collider, pyscumm.vector.Vector3D ):
    def __init__( self, v=[0.,0.,0.] ):
        pyscumm.vector.Vector3D.__init__( self, v )
    def collides( self, collider ):
        if isinstance( collider, Point ):
            raise NotImplementedError
        elif isinstance( collider, Box )\
        and collider.box.point_inside( self ):
            return self
        return None

class MultiBox( Collider, list ):
    def __init__( self, obj=[] ):
        list.__init__( self )
    def __str__( self ):
        return "MultiBox( %s )" % list.__str__( self )
    def update( self ):
        for box in self: box.update()
    def draw( self ):
        for box in self: box.draw()
    def collides( self, collider ):
        return MultiBox( [ o for o in self if o.collides( collider ) ] )

class WalkArea( MultiBox ):

    def __init__( self, box=[] ):
        MultiBox.__init__( self )
        for x in box: self.append( x )

    def __add( self, x ):
        node = BoxNode( x )
        collide = False
        for o in self:
            if not o.box.collides( x ): continue
            collide = True
            node.append( o )
            o.append( node )
        if len( self ):
            assert collide
        return node

    def __del( self, x ):
        for o in self: o.remove( x )

    def __setitem__( self, i, x ):
        self.__add( x )
        list.__setitem__( self, i, x )

    def __getitem__( self, i ):
        return list.__getitem__( i ).box

    def __delitem__( self, i ):
        self.__del( self[i] )
        list.__delitem__( item )

    def append( self, x ):
        """same as s[len(s):len(s)] = [x]"""
        l = len( self )
        self[l:l] = [self.__add( x )]

    def extend( self, x ):
        """same as s[len(s):len(s)] = x"""
        l = len( self )
        self[l:l] = self.__add( x )

    def insert( self, i, x ):
        """same as s[i:i] = [x]"""
        self[i:i] = [self.__add( x )]

    def pop( self, i=-1 ):
        """same as x = s[i]; del s[i]; return x"""
        x = self[i]
        self.__delitem__( i )
        return x.box

    def remove( self, x ):
        """same as del s[s.index(x)]"""
        self.__delitem__( self.index( x ) )

    def update( self ):
        for box in self: box.update()

    def draw( self ):
        for box in self: box.draw()

    def __str__( self ):
        return "WalkArea( %s )" % "\n".join( map( str, self ) )

#################################################################

class BoxNode( list ):
    def __init__( self, box=None, next=[] ):
        list.__init__( self, next )
        self._box = box
    def get_box( self ): return self._box
    def set_box( self, box ): self._box = box
    def __str__( self ):
        return "BoxNode( %s, (%s) %s )" % ( self._box, id( self ), map( id, self ) )
    box = property( get_box, set_box )


class BoxRect( list ):
    def __init__( self, box=None, obj=[] ):
        list.__init__( self, obj )
        self._box = box

    def get_box( self ): return self._box
    def set_box( self, box ): self._box = box

    def get_rect( self ):
        return self._rect

    def get_point( self ):
        return self._point

    def point_inside( self, point ):
        #If dist is negative to all the rects, point is inside
        return self._rect[0].dist_sqr( point ) <= 0 \
            and self._rect[1].dist_sqr( point ) <= 0 \
            and self._rect[2].dist_sqr( point ) <= 0 \
            and self._rect[3].dist_sqr( point ) <= 0

    def update( self ):
        location  = self._box.copy.location
        rotation  = pyscumm.vector.RotateVectorZ( self._box.copy.rotation[0] )
        scale     = self._box.copy.scale
        insertion = self._box.copy.insertion * scale
        location  = self._box.copy.location
        self._point = [
            ( ( ( point * scale ) + insertion ).rotate( rotation ) ) + location
            for point in self ]
        p_0, p_1, p_2, p_3 = self._point
        self._rect = [
            Rect.from_two_point( p_0, p_1 ),
            Rect.from_two_point( p_1, p_2 ),
            Rect.from_two_point( p_2, p_3 ),
            Rect.from_two_point( p_3, p_0 ) ]

    def box_inside( self, box ):
        point = box.point
        return self.point_inside( point[0] ) \
            or self.point_inside( point[1] ) \
            or self.point_inside( point[2] ) \
            or self.point_inside( point[3] )

    def __str__( self ):
        return "BoxRect( %s, %s )" % ( self._box, list.__str__( self ) )

    box   = property( get_box, set_box )
    point = property( get_point )
    rect  = property( get_rect )

"""
class BoxRect( list ):
    def __init__( self, location=None, obj=[] ):
        list.__init__( self, obj )
        self._location = location
        if isinstance( self._location, types.NoneType ):
            self._location = pyscumm.vector.Vector3D()

    def get_rect( self ):
        return [
            Rect.from_two_point(
                self[i]+self._location, self[(i+1)%4]+self._location )
                for i in xrange(4) ]

    def get_point( self ):
        return [ point + self._location for point in self ]

    def point_inside( self, point, rect=None ):
        #If dist is negative to all the rects, point is inside
        if isinstance( rect, types.NoneType ):
            rect = self.rect
        return not bool( reduce(
            lambda x,y: x+y,
            [ 1 for i in rect if i.dist_sqr( point ) > 0 ], 0 ) )

    def box_inside( self, box ):
        point = box.point
        rect = self.rect
        return self.point_inside( point[0], rect )\
            or self.point_inside( point[1], rect )\
            or self.point_inside( point[2], rect )\
            or self.point_inside( point[3], rect )

    def __str__( self ):
        return "BoxRect( %s, %s )" % ( self._location, list.__str__( self ) )

    point = property( get_point )
    rect  = property( get_rect )
"""

class Rect( pyscumm.vector.Vector3D ):
    def __init__( self, obj=[0.,0.,0.] ):
        pyscumm.vector.Vector3D.__init__( self, obj )
    def dist_sqr( self, p ):
        """d = (Ax1+By1+C)/sqrt(A*A+B*B). (No square root)"""
        self_0, self_1, self_2 = self
        p_0, p_1, p_2 = p
        return ((self_0*p_0)+(self_1*p_1)+self_2)/((self_0*self_0)+(self_1*self_1))
    def from_two_point( self, a, b ):
        """
        (X-x1)(y2-y1) = (Y-y1)(x2-x1)
        X(y2-y1)-x1(y2-y1) = Y(x2-x1)-y1(x2-x1)
        X(y2-y1) -Y(x2-x1) +(-x1(y2-y1)+y1(x2-x1)) = 0
        Ax + By + C = 0
        """
        a_0, a_1, a_2 = a
        b_0, b_1, b_2 = b
        return Rect([
            b_1-a_1,                         # A
            -(b_0-a_0),                      # B
            (-a_0*(b_1-a_1))+(a_1*(b_0-a_0)) # C
        ])

    def __str__( self ):
        return "Rect( %.2fx + %.2fy + %.2f = 0 )" % ( self[0], self[1], self[2] )
    from_two_point = classmethod( from_two_point )

"""
class Rect( pyscumm.vector.Vector3D ):
    def __init__( self, obj=[0.,0.,0.] ):
        pyscumm.vector.Vector3D.__init__( self, obj )
    def dist_sqr( self, p ):
        #d = (Ax1+By1+C)/sqrt(A*A+B*B). (No square root)
        return ((self[0]*p[0])+(self[1]*p[1])+self[2])/((self[0]*self[0])+(self[1]*self[1]))
    def from_two_point( self, a, b ):
        # (X-x1)(y2-y1) = (Y-y1)(x2-x1)
        # X(y2-y1)-x1(y2-y1) = Y(x2-x1)-y1(x2-x1)
        # X(y2-y1) -Y(x2-x1) +(-x1(y2-y1)+y1(x2-x1)) = 0
        # Ax + By + C = 0
        return Rect([
            b[1]-a[1],                             # A
            -(b[0]-a[0]),                          # B
            (-a[0]*(b[1]-a[1]))+(a[1]*(b[0]-a[0])) # C
        ])

    def __str__( self ):
        return "Rect( %.2fx + %.2fy + %.2f = 0 )" % ( self[0], self[1], self[2] )
    from_two_point = classmethod( from_two_point )
"""
