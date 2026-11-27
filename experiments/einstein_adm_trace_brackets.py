"""Compute actual bulk-to-boundary Poisson brackets in the tensor regulator."""

import sympy as sp

from einstein_even_bulk import XYZ, assemble, tensor_basis


def trace_rows(tensors):
    x, y, z = XYZ
    r = sp.Symbol("r")
    rows = []
    for tensor in tensors:
        pole = {x: 0, y: 0, z: r}
        equator = {x: r, y: 0, z: 0}
        radial = tensor[2, 2].subs(pole)
        angular_trace = ((tensor[0, 0]+tensor[1, 1])/2).subs(pole)
        shear = (tensor[2, 2]-tensor[1, 1]).subs(equator)/3
        # Mixed momentum pi_rA=b D_A Y. Evaluate off axis where D_theta Y != 0.
        on_sphere = {x: r/sp.sqrt(2), y: 0, z: r/sp.sqrt(2)}
        mixed = -(tensor[0, 0]-tensor[2, 2]).subs(on_sphere)/3
        # RW trace: angular gauge v=-d/2, radial gauge w=-J-r^2 v'.
        # Evaluate J=r*b at the seam. K shifts by 2w/r - 6v.
        displacement = -r*mixed + r*r*sp.diff(shear, r)/2
        rw_trace = angular_trace+3*shear+2*displacement/r
        rw_radial = radial+2*sp.diff(displacement, r)
        master = r*(rw_trace+(rw_radial-r*sp.diff(rw_trace, r))/2)/3
        # Induced K of a fixed relational sphere uses its displacement.
        intrinsic_trace = (angular_trace+3*shear).subs(r, 1)
        rows.append((intrinsic_trace, master.subs(r, 1), radial.subs(r, 1), mixed.subs(r, 1)))
    return sp.Matrix(rows).T


def check(order):
    gram, lapse, shift = assemble(order)
    traces = trace_rows(tensor_basis(order))
    inverse = gram.inv()
    geometry = traces[:2, :]
    flux = traces[2:, :]
    # Momentum coefficients are dual to metric coefficients with this Gram.
    mixed = geometry*inverse*flux.T
    assert mixed.rank() == 2
    assert geometry*inverse*shift.T == sp.zeros(2, shift.rows)
    assert flux*inverse*lapse.T == sp.zeros(2, lapse.rows)
    print(f"order={order}: trace/flux bracket={mixed}; proper cross brackets vanish")
    return mixed


if __name__ == "__main__":
    assert check(1) != check(2)
