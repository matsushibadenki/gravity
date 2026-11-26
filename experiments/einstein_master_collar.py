"""Static susceptibility of a collar-smeared dynamical master-field source."""

import numpy as np
from numpy.polynomial.legendre import leggauss


def response(width, nodes, intrinsic=False):
    x, weights = leggauss(nodes)
    r = 1 + width * x
    # Normalized parabolic collar. The doubled domain is split at r=s.
    weight = 3 * weights * (1 - x**2) / 4
    y = (x[:, None] + 1) * (x[None, :] + 1) / 2 - 1
    s = 1 + width * y
    inner_weight = (x[:, None] + 1) / 2 * weights * 3 * (1 - y**2) / 4
    # Dirichlet Green function is f(min)g(max)/5. Apply D=d/dr+3/r
    # to each factor on the open triangles and include the delta on the diagonal.
    df = 6 * s**2
    dg = r**-3 - 6 * r**2 / 32
    if intrinsic:
        weight = weight / r**2
        inner_weight = inner_weight / s**2
    regular = 32 / 5 * np.sum(weight[:, None] * inner_weight * df * dg[:, None])
    contact = 48 / (5 * width)
    if intrinsic:
        contact = 9 / width * np.sum(weights * (1 - x**2)**2 / r**4)
    return contact + regular, regular


if __name__ == "__main__":
    previous = None
    for width in (.2, .1, .05, .025, .0125):
        total, finite = response(width, 32)
        np.testing.assert_allclose([total, finite], response(width, 16), rtol=1e-12)
        error = abs(finite - 78 / 5)
        if previous is not None:
            assert error < .6 * previous
        previous = error
        print(f"width={width:.4f}: susceptibility={total:.9f}, "
              f"after contact subtraction={finite:.9f}")
