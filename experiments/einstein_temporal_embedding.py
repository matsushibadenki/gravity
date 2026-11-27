"""Normal connection of a temporally displaced sphere to first order."""

import sympy as sp


def check():
    theta, phi, epsilon, radius = sp.symbols("theta phi eps r", real=True)
    normal = sp.Matrix([sp.sin(theta)*sp.cos(phi),
                        sp.sin(theta)*sp.sin(phi), sp.cos(theta)])
    harmonic = (3*sp.cos(theta)**2-1)/2
    # Embedding (epsilon Y, r n). Choose the outward spacelike normal
    # radial and the future normal orthogonal to both surface tangents.
    tangent = radius*normal.diff(theta)
    future_spatial = epsilon*harmonic.diff(theta)*normal.diff(theta)/radius
    assert sp.trigsimp(future_spatial.dot(tangent)-epsilon*harmonic.diff(theta)) == 0
    assert sp.trigsimp(future_spatial.dot(normal)) == 0
    connection = sp.trigsimp(normal.dot(future_spatial.diff(theta)))
    assert sp.trigsimp(connection+epsilon*harmonic.diff(theta)/radius) == 0
    assert sp.trigsimp(normal.dot(future_spatial.diff(phi))) == 0
    print("Radial-frame normal connection: omega_A=-D_A(delta T)/r.")
    print("After boost: omega_A=D_A(eta-delta T/r).")


if __name__ == "__main__":
    check()
