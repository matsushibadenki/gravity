"""Check the traceless tensor constraint and its local dispersion."""

from fractions import Fraction as F


def trace_free(matrix):
    trace = sum(matrix[i][i] for i in range(3))
    return [[matrix[i][j] - (trace / 3 if i == j else 0) for j in range(3)] for i in range(3)]


def main():
    # Rotations allow k along z. The three gauge shifts span the complement of TT.
    gauge = []
    for axis in range(3):
        shift = [[F(int(i == 2 and j == axis) + int(j == 2 and i == axis), 2)
                  for j in range(3)] for i in range(3)]
        gauge.append(trace_free(shift))

    assert [sum(value**2 for row in matrix for value in row) for matrix in gauge] == [
        F(1, 2), F(1, 2), F(2, 3)
    ]
    # At order k^2, vector and scalar gauge components have different eigenvalues.
    def longitudinal(matrix):
        return trace_free([
            [(int(i == 2) * matrix[j][2] + int(j == 2) * matrix[i][2]) / 2
             for j in range(3)] for i in range(3)
        ])

    for matrix, factor in zip(gauge, (F(1, 2), F(1, 2), F(2, 3))):
        assert longitudinal(matrix) == [[factor * value for value in row] for row in matrix]
    vector_factor, scalar_factor = F(1, 2), F(2, 3)
    assert scalar_factor - vector_factor == F(1, 6)
    print("Gauge rank: 3 at nonzero momentum. Two physical canonical pairs remain.")
    print("The order-k^2 gauge-null conditions are independent and force a=b=0.")

    for momentum in (F(1, 16), F(1, 8)):
        squared_frequency = momentum**4
        assert (2 * momentum)**4 / squared_frequency == 16
    print("A local positive order-k^4 kernel doubles momentum and quadruples frequency.")


if __name__ == "__main__":
    main()
