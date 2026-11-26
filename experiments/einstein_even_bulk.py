"""Exact polynomial Galerkin test of the proper even-parity ADM algebra."""

from functools import lru_cache

import sympy as sp

XYZ = sp.symbols("x y z")
X = sp.Matrix(XYZ)
I = sp.eye(3)
Q = sp.diag(-1, -1, 2) / 2
R2 = X.dot(X)
Y = X.dot(Q * X)


@lru_cache(None)
def moment(powers):
    if any(power % 2 for power in powers):
        return 0
    return sp.simplify(
        sp.prod(sp.gamma(sp.Rational(power + 1, 2)) for power in powers)
        / sp.gamma(sp.Rational(sum(powers) + 5, 2))
    )


def inner(left, right):
    polynomial = sp.Poly(sum(a * b for a, b in zip(left, right)), *XYZ)
    return sum(coefficient * moment(powers) for powers, coefficient in polynomial.terms())


def jacobian(vector):
    return vector.jacobian(XYZ)


def lapse_gradient(lapse):
    hessian = sp.hessian(lapse, XYZ)
    return hessian - I * sp.trace(hessian)


def shift_gradient(shift):
    derivative = jacobian(shift)
    return derivative + derivative.T


def check(order):
    tensors = [R2**j * tensor for j in range(order + 3) for tensor in
               (Y * I, Q, X * (Q * X).T + (Q * X) * X.T, Y * X * X.T)]
    lapses = [Y * R2**j * (1 - R2)**2 for j in range(order)]
    shifts = [R2**j * (1 - R2) * vector for j in range(order)
              for vector in (Q * X, Y * X)]
    lapse_fields = [lapse_gradient(lapse) for lapse in lapses]
    shift_fields = [shift_gradient(shift) for shift in shifts]
    gram = sp.Matrix([[inner(a, b) for b in tensors] for a in tensors]) / sp.pi
    scalar = sp.Matrix([[inner(a, b) for b in tensors] for a in lapse_fields]) / sp.pi
    vector = -sp.Matrix([[inner(a, b) for b in tensors] for a in shift_fields]) / sp.pi

    # The canonical momentum coefficients use the inverse tensor Gram metric.
    # Exact representation prevents a projected gauge vector from masking a defect.
    gauge_vectors = gram.inv() * vector.T
    for column, field in enumerate(shift_fields):
        reconstructed = sum((gauge_vectors[j, column] * tensor
                             for j, tensor in enumerate(tensors)), sp.zeros(3))
        assert (reconstructed + field).applyfunc(sp.expand) == sp.zeros(3)
    assert scalar * gauge_vectors == sp.zeros(order, 2 * order)
    assert scalar.rank() == order and vector.rank() == 2 * order
    print(f"order={order}: tensor modes={len(tensors)}, "
          f"constraint ranks=({order}, {2 * order}), mixed bracket exactly zero")


if __name__ == "__main__":
    for size in (1, 2, 3):
        check(size)
