"""Derive the normal-frame jet from a time graph on a fixed round tube."""

import sympy as sp


def check():
    r, theta = sp.symbols("r theta", positive=True)
    amplitude = sp.Function("N")(r)
    y = (3*sp.cos(theta)**2-1)/2
    graph = amplitude*y
    # First-order coefficients in (t, r, theta). The future normals
    # to the graph and to its cut within the timelike tube differ only
    # in the radial component. Keep the fixed tube at the same radius.
    metric = sp.diag(-1, 1, r**2)
    radial_tangent = sp.Matrix([graph.diff(r), 1, 0])
    angular_tangent = sp.Matrix([graph.diff(theta), 0, 1])
    slice_normal = sp.Matrix([1, graph.diff(r), graph.diff(theta)/r**2])
    tube_normal = sp.Matrix([1, 0, graph.diff(theta)/r**2])
    assert slice_normal.dot(metric*radial_tangent) == 0
    assert slice_normal.dot(metric*angular_tangent) == 0
    assert tube_normal.dot(metric*angular_tangent) == 0
    assert tube_normal-slice_normal == sp.Matrix([0, -graph.diff(r), 0])

    # The inverse displacement of the boundary label is delta T=-N.
    # Read off the signed relative boost in the common radial direction.
    delta_eta = -amplitude.diff(r)
    delta_time = -amplitude
    delta_beta = delta_eta-delta_time/r
    assert sp.expand(delta_beta - (-amplitude.diff(r)+amplitude/r)) == 0
    # This selects the nonzero area column of the previous trace test.
    mixed = sp.Matrix([[0, 0], [-2*r, 0]])
    assert mixed*sp.Matrix([amplitude, amplitude.diff(r)]) == sp.Matrix([0, -2*r*amplitude])
    print("Fixed tube and displaced slice: delta eta = -N_r.")
    print("Adapted boost changes by -N_r + N/r, including the lapse value.")


if __name__ == "__main__":
    check()
