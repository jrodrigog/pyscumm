from types import NoneType
import math

class Vector2D( list ):
    """2D Vector class"""
    def __init__( self, v = [0.,0.] ):
        list.__init__( self, v )
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Vector2D()
        obj[0] = self[0]
        obj[1] = self[1]
        return obj
    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Vector2D()
        tmp = element.getAttribute("x")
        if tmp != None: obj[0] = float( tmp )
        tmp = element.getAttribute("y")
        if tmp != None: obj[1] = float( tmp )
        return obj
    def __add__( self, o ):
        return Vector2D( [
            self[0] + o[0],
            self[1] + o[1] ] )
    def __iadd__( self, o ):
        self[0] += o[0]
        self[1] += o[1]
        return self
    def __sub__( self, o ):
        return Vector2D( [
            self[0] - o[0],
            self[1] - o[1] ] )
    def __isub__( self, o ):
        self[0] -= o[0]
        self[1] -= o[1]
        return self
    def __mult__( self, k ):
        return Vector3D( [
            self[0] * k,
            self[1] * k ] )
    def __imult__( self, k ):
        self[0] *= k
        self[1] *= k
        return self
    def __eq__( self, o ):
        return self[0] == o[0] and self[1] == o[1]
    def length( self ):
        return math.sqrt(
            ( self[0] * self[0] ) + ( self[1] * self[1] ) )
    def scale( self, scale ):
        return Vector2D( [
            self[0] * scale,
            self[1] * scale ] )
    def rotate( self, rotation ):
        if not isinstance( rotation, VectorRotation ):
            rotation = RotateVector( rotation )
        return rotation.rotate( self )
    def __repr__( self ):
        return "Vector2D([%.2f,%.2f])" % ( self[0], self[1] )
    deserialize = classmethod( deserialize )

class Vector3D( list ):
    """3D Vector class"""
    def __init__( self, v = [0.,0.,0.] ):
        list.__init__( self, v )
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Vector3D()
        obj[0] = self[0]
        obj[1] = self[1]
        obj[2] = self[2]
        return obj
    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Vector3D()
        tmp = element.getAttribute("x")
        if tmp != None: obj[0] = float( tmp )
        tmp = element.getAttribute("y")
        if tmp != None: obj[1] = float( tmp )
        tmp = element.getAttribute("z")
        if tmp != None: obj[2] = float( tmp )
        return obj
    def __add__( self, o ):
        return Vector3D( [
            self[0] + o[0],
            self[1] + o[1],
            self[2] + o[2] ] )
    def __iadd__( self, o ):
        self[0] += o[0]
        self[1] += o[1]
        self[2] += o[2]
        return self
    def __sub__( self, o ):
        return Vector3D( [
            self[0] - o[0],
            self[1] - o[1],
            self[2] - o[2] ] )
    def __isub__( self, o ):
        self[0] -= o[0]
        self[1] -= o[1]
        self[2] -= o[2]
        return self
    def __mult__( self, k ):
        return Vector3D( [
            self[0] * k,
            self[1] * k,
            self[2] * k ] )
    def __imult__( self, k ):
        self[0] *= k
        self[1] *= k
        self[2] *= k
        return self
    def __eq__( self, o ):
        return self[0] == o[0]\
            and self[1] == o[1]\
            and self[2] == o[2]
    def length( self ):
        return math.sqrt(
            ( self[0] * self[0] )
            + ( self[1] * self[1] )
            + ( self[2] * self[2] ) )
    def scale( self, scale ):
        return Vector3D( [
            self[0] * scale,
            self[1] * scale,
            self[2] * scale ] )
    def rotate( self, rotation ):
        if not isinstance( rotation, VectorRotation ):
            rotation = RotateVector( rotation )
        return rotation.rotate( self )
    def __repr__( self ):
        return "Vector3D([%.2f,%.2f,%.2f])" % ( self[0], self[1], self[2] )
    deserialize = classmethod( deserialize )

class Vector4D( list ):
    """4D Vector class"""
    def __init__( self, v = [0.,0.,0.,0.] ):
        list.__init__( self, v )
    def clone( self, obj=None, deep=False ):
        if isinstance( obj, NoneType ): obj = Vector4D()
        obj[0] = self[0]
        obj[1] = self[1]
        obj[2] = self[2]
        obj[3] = self[3]
        return obj
    def deserialize( self, element, obj=None ):
        """Deserialize from XML"""
        if obj == None: obj = Vector4D()
        tmp = element.getAttribute("x")
        if tmp != None: obj[0] = float( tmp )
        tmp = element.getAttribute("y")
        if tmp != None: obj[1] = float( tmp )
        tmp = element.getAttribute("z")
        if tmp != None: obj[2] = float( tmp )
        tmp = element.getAttribute("u")
        if tmp != None: obj[3] = float( tmp )
        return obj
    def __add__( self, o ):
        return Vector3D( [
            self[0] + o[0],
            self[1] + o[1],
            self[2] + o[2],
            self[3] + o[3] ] )
    def __iadd__( self, o ):
        self[0] += o[0]
        self[1] += o[1]
        self[2] += o[2]
        self[3] += o[3]
        return self
    def __sub__( self, o ):
        return Vector3D( [
            self[0] - o[0],
            self[1] - o[1],
            self[2] - o[2],
            self[3] - o[3] ] )
    def __isub__( self, o ):
        self[0] -= o[0]
        self[1] -= o[1]
        self[2] -= o[2]
        self[3] -= o[3]
        return self
    def __mult__( self, k ):
        return Vector3D( [
            self[0] * k,
            self[1] * k,
            self[2] * k,
            self[3] * k ] )
    def __imult__( self, k ):
        self[0] *= k
        self[1] *= k
        self[2] *= k
        self[3] *= k
        return self
    def __eq__( self, o ):
        return self[0] == o[0]\
            and self[1] == o[1]\
            and self[2] == o[2]\
            and self[3] == o[3]
    def length( self ):
        return math.sqrt(
            ( self[0] * self[0] )
            + ( self[1] * self[1] )
            + ( self[2] * self[2] )
            + ( self[3] * self[3] ) )
    def scale( self, scale ):
        return Vector4D( [
            self[0] * scale,
            self[1] * scale,
            self[2] * scale,
            self[3] * scale ] )
    def rotate( self, rotation ):
        raise NotImplementedError
    def __repr__( self ):
        return "Vector4D([%.2f,%.2f,%.2f,%.2f])" % ( self[0], self[1], self[2], self[3] )
    deserialize = classmethod( deserialize )

class VectorRotation( list ):
    """This abstract class implements a common rotation for
    2D and 3D vectors based on the current rotation matrix.
    Reference:
    http://www.kwon3d.com/theory/transform/rot.html"""
    def rotate( self, vector ):
        """Rotates a 2D or 3D vector by a rotation matrix.
        @param vector: The vector to rotate
        @type vector: Vector2D/Vector3D
        @return: A new rotated vector
        @rtype: Vector2D/Vector3D
        """
        v = vector.clone()
        v[0] = ( self[0][0] * vector[0] ) \
            + ( self[0][1] * vector[1] )
        v[1] = ( self[1][0] * vector[0] ) \
            + ( self[1][1] * vector[1] )
        # handle 3D/2D
        try:
            v[0] += self[0][2] * vector[2]
            v[1] += self[1][2] * vector[2]
            v[2] = ( self[2][0] * vector[0] ) \
                + ( self[2][1] * vector[1] ) \
                + ( self[2][2] * vector[2] )
        except IndexError: pass
        return v

class RotateVectorZ( VectorRotation ):
    """
    Rotate a Vector in the Z axis
    [ cos -sin   0 ]
    [ sin  cos   0 ]
    [   0    0   1 ]
    """
    def __init__( self, alpha ):
        """Build a RotateVectorZ object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[ cos, -sin, 0. ],
             [ sin,  cos, 0. ],
             [  0.,   0., 1. ]] )

class RotateVectorX( VectorRotation ):
    """
    Rotate a Vector in the X axis.
    [   1    0    0 ]
    [   0  cos -sin ]
    [   0  sin  cos ]
    """
    def __init__( self, alpha ):
        """Build a RotateVectorX object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[  1.,  0.,   0. ],
             [  0., cos, -sin ],
             [  0., sin,  cos ]] )

class RotateVectorY( VectorRotation ):
    """
    Rotate a Vector in the Y axis.
    [ cos   0  sin ]
    [   0   1    0 ]
    [-sin   0  cos ]
    """
    def __init__( self, alpha ):
        """Build a RotateVectorY object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[  cos, 0., sin ],
             [   0., 1., 0.  ],
             [ -sin, 0., cos ]] )

class RotateAxisZ( VectorRotation ):
    """
    Rotate the Z Axis.
    [ cos sin   0 ]
    [-sin cos   0 ]
    [   0   0   1 ]
    """
    def __init__( self, alpha ):
        """Build a RotateAxisZ object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[  cos, sin, 0. ],
             [ -sin, cos, 0. ],
             [   0., 0.,  1. ]] )

class RotateAxisX( VectorRotation ):
    """
    Rotate the X Axis.
    [  1    0   0 ]
    [  0  cos sin ]
    [  0 -sin cos ]
    """
    def __init__( self, alpha ):
        """Build a RotateAxisX object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[ 1.,  0.,  0. ],
             [ 0., cos, sin ],
             [ 0.,-sin, cos ]] )

class RotateAxisY( VectorRotation ):
    """
    Rotate the Y Axis.
    [ cos   0 -sin ]
    [  0    1    0 ]
    [ sin   0  cos ]
    """
    def __init__( self, alpha ):
        """Build a RotateAxisY object, inits the rotation matrix.
        @param alpha: Rotation angle in degrees
        @type alpha: float
        """
        cos = math.cos( alpha )
        sin = math.sin( alpha )
        VectorRotation.__init__( self,
            [[ cos, 0., -sin ],
             [  0., 1.,   0. ],
             [ sin, 0.,  sin ]] )

class RotateVector( RotateVectorZ ):
    """This is a default 2D Vector rotation (In the Z axis)."""
    pass 

class RotateAxis( RotateAxisZ ):
    """This is a default 2D Axis rotation (In the Z axis)."""
    pass
