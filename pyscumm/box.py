import types
from vector import Vector3D, RotateVectorZ

class Collider( object ):
    def clone( self, obj=None, deep=False ):
        raise NotImplementedError
    def collides( self, collider ):
        raise NotImplementedError
    def update( self ):
        raise NotImplementedError
    def draw( self ):
        raise NotImplementedError

class Box( Collider ):
    def __init__( self, shadow=1., depth=1. ):
        self.shadow = shadow
        self.depth = depth
        self.box = BoxRect( self, [
            Vector3D( [ -1., -1., 0. ] ),
            Vector3D( [  1., -1., 0. ] ),
            Vector3D( [  1.,  1., 0. ] ),
            Vector3D( [ -1.,  1., 0. ] ) ] )

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = Box()
        obj.shadow = self.shadow
        obj.depth = self.depth
        self.box.clone( obj.box, deep )
        return obj

    def collides( self, collider ):
        if isinstance( collider, Point )\
        and self.box.point_inside( collider ):
            return self
        elif isinstance( collider, Box )\
        and self.box.box_inside( collider.box ):
            return self
        return None

    def __str__( self ):
        return "Box( location=%s, shadow=%s, depth=%s, box=%s )" % (
            self.location,
            self.shadow,
            self.depth,
            self.box )

    def update( self ):
        self.box.update()


class Point( Collider, Vector3D ):
    def __init__( self, v=[0.,0.,0.] ):
        Vector3D.__init__( self, v )
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = Point()
        return Vector3D.clone( self, obj, deep )
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
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = MultiBox()
        for o in self: obj.append( o.clone( deep=deep ) )
        return obj
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

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = WalkArea()
        return MultiBox.clone( self, obj, deep=deep )

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
        self.box = box
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = BoxNode()
        for o in self: obj.append( o.clone( deep=deep ) )
        return obj
    def __str__( self ):
        return "BoxNode( %s, (%s) %s )" % (
            self.box, id( self ), map( id, self ) )


class BoxRect( list ):
    def __init__( self, box=None, obj=[] ):
        list.__init__( self, obj )
        self.box = box

    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = BoxRect()
        self[0].clone( obj[0], deep )
        self[1].clone( obj[1], deep )
        self[2].clone( obj[2], deep )
        self[3].clone( obj[3], deep )
        return obj

    def point_inside( self, point ):
        #If dist is negative to all the rects, point is inside
        return self.rect[0].dist_sqr( point ) <= 0 \
            and self.rect[1].dist_sqr( point ) <= 0 \
            and self.rect[2].dist_sqr( point ) <= 0 \
            and self.rect[3].dist_sqr( point ) <= 0

    def update( self ):
        location  = self.box.copy.location
        rotation  = RotateVectorZ( self.box.copy.rotation[0] )
        scale     = self.box.copy.scale
        insertion = self.box.copy.insertion * scale
        location  = self.box.copy.location
        self.point = [
            ( ( ( point * scale ) + insertion ).rotate( rotation ) ) + location
            for point in self ]
        p_0, p_1, p_2, p_3 = self.point
        self.rect = [
            from_two_point( p_0, p_1 ),
            from_two_point( p_1, p_2 ),
            from_two_point( p_2, p_3 ),
            from_two_point( p_3, p_0 ) ]

    def box_inside( self, box ):
        point = box.point
        return self.point_inside( point[0] ) \
            or self.point_inside( point[1] ) \
            or self.point_inside( point[2] ) \
            or self.point_inside( point[3] )

    def __str__( self ):
        return "BoxRect( %s )" % ( list.__str__( self ) )

"""
class BoxRect( list ):
    def __init__( self, location=None, obj=[] ):
        list.__init__( self, obj )
        self._location = location
        if isinstance( self._location, types.types.NoneType ):
            self._location = Vector3D()

    def get_rect( self ):
        return [
            Rect.from_two_point(
                self[i]+self._location, self[(i+1)%4]+self._location )
                for i in xrange(4) ]

    def get_point( self ):
        return [ point + self._location for point in self ]

    def point_inside( self, point, rect=None ):
        #If dist is negative to all the rects, point is inside
        if isinstance( rect, types.types.NoneType ):
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

class Rect( Vector3D ):
    def __init__( self, obj=[0.,0.,0.] ):
        Vector3D.__init__( self, obj )
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, types.NoneType ): obj = Rect()
        return Vector3D.clone( self, obj, deep )
    def dist_sqr( self, p ):
        """d = (Ax1+By1+C)/sqrt(A*A+B*B). (No square root)"""
        self_0, self_1, self_2 = self
        p_0, p_1, p_2 = p
        return ((self_0*p_0)+(self_1*p_1)+self_2)/((self_0*self_0)+(self_1*self_1))

    def __str__( self ):
        return "Rect( %.2fx + %.2fy + %.2f = 0 )" % ( self[0], self[1], self[2] )

def from_two_point( a, b ):
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

"""
class Rect( Vector3D ):
    def __init__( self, obj=[0.,0.,0.] ):
        Vector3D.__init__( self, obj )
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
