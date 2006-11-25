import math
import pyscumm

v = pyscumm.vector.Vector2D( [ 1., 0. ] )

print v.rotate( math.pi / 2. )
print v.rotate( pyscumm.vector.RotateAxisZ( math.pi / 2. ) )

rot = pyscumm.vector.RotateVector( math.pi )
vv = [ v.clone() for i in xrange(8) ]
print vv
vvv = [ i.rotate( rot ) for i in vv ]
print vvv
