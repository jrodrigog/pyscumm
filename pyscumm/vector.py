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
    deserialize = classmethod( deserialize )
