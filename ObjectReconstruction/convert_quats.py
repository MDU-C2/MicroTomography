from numpy import matrix, linalg, sqrt, trace
def mat2quat(t):
    #   Adapted from "robotic toolbox for python"
    #   Convert homogeneous transform to a unit-quaternion
    #   Return a unit quaternion corresponding to the rotational part of the
    #   homogeneous transform t.

    qs = sqrt(trace(t)+1)/2.0
    kx = t[2,1] - t[1,2]    # Oz - Ay
    ky = t[0,2] - t[2,0]    # Ax - Nz
    kz = t[1,0] - t[0,1]    # Ny - Ox
    if (t[0,0] &gt;= t[1,1]) and (t[0,0] &gt;= t[2,2]):
        kx1 = t[0,0] - t[1,1] - t[2,2] + 1      # Nx - Oy - Az + 1
        ky1 = t[1,0] + t[0,1]           # Ny + Ox
        kz1 = t[2,0] + t[0,2]           # Nz + Ax
        add = (kx &gt;= 0)
    elif (t[1,1] &gt;= t[2,2]):
        kx1 = t[1,0] + t[0,1]           # Ny + Ox
        ky1 = t[1,1] - t[0,0] - t[2,2] + 1  # Oy - Nx - Az + 1
        kz1 = t[2,1] + t[1,2]           # Oz + Ay
        add = (ky &gt;= 0)
    else:
        kx1 = t[2,0] + t[0,2]           # Nz + Ax
        ky1 = t[2,1] + t[1,2]           # Oz + Ay
        kz1 = t[2,2] - t[0,0] - t[1,1] + 1  # Az - Nx - Oy + 1
        add = (kz &gt;= 0)
    if add:
        kx = kx + kx1
        ky = ky + ky1
        kz = kz + kz1
    else:
        kx = kx - kx1
        ky = ky - ky1
        kz = kz - kz1
    kv = matrix([kx, ky, kz])
    nm = linalg.norm( kv )
    if nm == 0:
        e0 = 1.0
        q = matrix([0.0, 0.0, 0.0])
    else:
        e0 = qs
        q = (sqrt(1 - qs**2) / nm) * kv
    return e0, q[0,0], q[0,1], q[0,2]


