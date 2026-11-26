"""Periodic Euclidean time transfer with a fixed intrinsic curvature collar."""

import numpy as np

from einstein_collar_gluing import eliminate, radial_block, source_vector


def check(cells, steps):
    dt, width, kappa = 1 / steps, .125, .3
    grid = np.linspace(0, 2, 2*cells+1)
    time = np.arange(steps) * dt
    # Unitary Fourier transform of a real, nonstatic periodic source.
    source_time = .1*(1 + .2*np.cos(2*np.pi*time) + .3*np.sin(4*np.pi*time))
    spectrum = np.fft.fft(source_time, norm="ortho")
    full = glued = source_quadratic = 0.
    max_response_gap = 0.
    for frequency, j in enumerate(spectrum):
        omega2 = 4*np.sin(np.pi*frequency/steps)**2/dt**2

        def block(interval):
            # Endpoint half weights assign the seam time kinetic term once.
            weight = np.ones(len(interval))
            weight[[0, -1]] = .5
            return dt*kappa*(radial_block(interval, 2)
                             + np.diag(omega2*weight/cells))

        matrix = block(grid)[1:-1, 1:-1]
        source = dt*source_vector(grid, width, intrinsic=True)[1:-1]
        direct_response = source @ np.linalg.solve(matrix, source)
        source_quadratic += abs(j/.1)**2*direct_response
        full += (-np.linalg.slogdet(matrix)[1] + abs(j)**2*direct_response)/2
        inside, outside = grid[:cells+1], grid[cells:]
        left = eliminate(block(inside)[1:, 1:],
                         dt*source_vector(inside, width, intrinsic=True)[1:])
        right = eliminate(block(outside)[:-1, :-1][::-1, ::-1],
                          dt*source_vector(outside, width, intrinsic=True)[:-1][::-1])
        stiffness, linear, constant, logdet = np.add(left, right)
        response = constant + linear**2/stiffness
        max_response_gap = max(max_response_gap, abs(response-direct_response))
        glued += (-logdet - np.log(stiffness) + abs(j)**2*response)/2
    np.testing.assert_allclose(glued, full, atol=1e-9, rtol=0)
    assert max_response_gap < 1e-10
    print(f"cells={cells}, time steps={steps}: log amplitude gap={glued-full:+.3e}, "
          f"maximum response gap={max_response_gap:.3e}")

    return full, source_quadratic


if __name__ == "__main__":
    for resolution in (32, 64, 128):
        check(resolution, resolution//4)
