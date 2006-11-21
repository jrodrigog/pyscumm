import pyscumm.box
import pyscumm.vector

if __name__ == "__main__":
    """
    +-----+
    |     | location 10,10
    |  *  | each points goes offsetized from here
    |     |
    +-----+
    """
    b = pyscumm.box.Box()
    b.location[0] = 10.; b.location[1] = 10.
    b.box[0][0] = -10.; b.box[0][1] = -10.
    b.box[1][0] =  10.; b.box[1][1] = -10.
    b.box[2][0] =  10.; b.box[2][1] =  10.
    b.box[3][0] = -10.; b.box[3][1] =  10.
    bb = pyscumm.box.Box()
    bb.location[0] = 0.; bb.location[1] = 0.
    bb.box[0][0] = -10.; bb.box[0][1] = -10.
    bb.box[1][0] =  10.; bb.box[1][1] = -10.
    bb.box[2][0] =  10.; bb.box[2][1] =  10.
    bb.box[3][0] = -10.; bb.box[3][1] =  10.
    p = pyscumm.box.Point( pyscumm.vector.Vector3D( [ 10., 10., 0. ] ) )
    np = pyscumm.box.Point( pyscumm.vector.Vector3D( [ 21., 21., 0. ] ) )
    assert b.collides( p )
    assert not b.collides( np )
    assert bb.collides( b )
    bb.location[0] = -10.; bb.location[1] = -10.
    assert bb.collides( b )
    bb.location[0] = -20.; bb.location[1] = -20.
    assert not bb.collides( b )

    w = pyscumm.box.WalkArea()
    w.append( b )
    bb.location[0] = -5.; bb.location[1] = -5.
    w.append( bb )
    print w
