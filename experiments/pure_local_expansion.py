"""Compute pure curvature heat coefficients from metric, clock, and ghost vertices."""

import argparse
from math import factorial, pi
from pathlib import Path

import numpy as np
from scipy.special import roots_genlaguerre

from curvature_band_matching import LENGTH, checkpointed_result, settled
from direct_curvature_insertion import operator_jets
from mixed_transverse_continuum import BANDS, TIMES, integrals
from pure_transverse_insertion_sum import continuum_response
from transverse_insertion_sum import WAVE


ORDER = 10
LENGTH_X = 5.6
GRIDS = (53, 57)
SHORTEST_GRID = 65


def fourier_vertices(size, shear, radius, direction, wave):
    t, y, z = radius * direction / WAVE
    jets = operator_jets(size, (t, 0., y, z), 0., shear=shear,
                         project_zero=False, length_x=2*pi/wave)
    result = []
    for block, channels in zip(jets, (11, 4)):
        a = np.array(block).reshape(3, 2, size, channels, 2, size, channels)
        a = np.fft.fft(np.fft.ifft(a, axis=2, norm="ortho"), axis=5, norm="ortho")
        result.append(a)
    return result


def matrix_at(jets, size, order, k, delta):
    matrix = jets[order, :, (k+delta) % size, :, :, k % size, :]
    return matrix.reshape(2*jets.shape[3], -1)


def vertices(shear, direction):
    size = 13
    radii = (-1., 0., 1.)
    samples = [fourier_vertices(size, shear, p, direction, 1.) for p in radii]
    independent = fourier_vertices(17, shear, .73, direction, 1.4)
    for actual, channels in zip(independent, (11, 4)):
        np.testing.assert_allclose(matrix_at(actual, 17, 0, 1, 0),
                                   (1.4**2+.73**2)*np.eye(2*channels), atol=1e-10, rtol=0)
    powers = [(i, j, 2-i-j) for i in range(3) for j in range(3-i)]
    pairs = [(k, p, jets) for p, jets in zip(radii, samples) for k in (-1, 0, 1)]
    design = np.array([[k**i * p**j for i, j, _ in powers] for k, p, _ in pairs])
    inverse = np.linalg.pinv(design)
    result = []
    for species in (0, 1):
        blocks = {}
        for order, delta in ((1, -1), (1, 1), (2, 0)):
            measured = np.array([matrix_at(jet[species], size, order, k, delta) for k, _, jet in pairs])
            coefficient = np.einsum("ij,jab->iab", inverse, measured)
            predicted = sum(c * 1.4**(i+m) * .73**j for (i, j, m), c in zip(powers, coefficient))
            np.testing.assert_allclose(predicted, matrix_at(independent[species], 17, order, 1, delta),
                                       atol=1e-10, rtol=0)
            blocks[order, delta] = coefficient
        result.append(blocks)
    return powers, result


def evaluate(vertex, powers, k, p, shift=0):
    """Matrix coefficients at input momentum k + shift*q."""
    a = np.zeros((3, *vertex.shape[1:]), dtype=complex)
    for (i, j, m), block in zip(powers, vertex):
        a[m] += k**i * p**j * block
        if i == 1:
            a[m+1] += shift * p**j * block
        if i == 2:
            a[1] += 2*k*shift * block
            a[2] += shift**2 * block
    return a


def trace_series(powers, blocks, k, p):
    # These are derivatives, so the diagonal H'' contributes -tr(H'').
    out = np.zeros(ORDER+1, dtype=complex)
    out[:3] -= np.trace(evaluate(blocks[2, 0], powers, k, p), axis1=1, axis2=2)
    for delta in (-1, 1):
        a = evaluate(blocks[1, delta], powers, k, p)
        b = evaluate(blocks[1, -delta], powers, k, p, delta)
        products = np.array([sum(np.trace(a[i] @ b[d-i]) for i in range(3) if 0 <= d-i < 3)
                             for d in range(5)])
        # The first-vertex pair carries the divided difference of the flat heat
        # exponential. Its series is integral_0^1 exp[-t(2 k delta q+q^2)] dt.
        weight = np.zeros(ORDER+1)
        for n in range(ORDER+1):
            term = np.polynomial.polynomial.polypow([0., -2*k*delta, -1.], n)[:ORDER+1]
            weight[:len(term)] += term / factorial(n+1)
        out += np.convolve(products, weight)[:ORDER+1]
    return out


def coefficient_rows(shear, nodes):
    signed_directions = [(np.ones(3)/np.sqrt(3), 1.)]
    if shear:
        # The transverse angular polynomial has degree at most four.
        signed_directions = [(np.eye(3)[0], 2/15), (np.eye(3)[1], 4/15),
                             (np.ones(3)/np.sqrt(3), 3/5)]
    xs, wx = np.polynomial.hermite.hermgauss(nodes)
    rs, wr = roots_genlaguerre(nodes, .5)
    integrated = np.zeros((2, ORDER+1), dtype=complex)
    for direction, fraction in signed_directions:
        powers, blocks = vertices(shear, direction)
        for k, a in zip(xs, wx):
            for r, b in zip(rs, wr):
                integrated += fraction*a*b*np.array([trace_series(powers, block, k, np.sqrt(r))
                                                       for block in blocks])
    density = integrated * (2*pi) / (2*(2*pi)**4)
    np.testing.assert_allclose(density.imag, 0, atol=1e-10, rtol=0)
    np.testing.assert_allclose(density[:, 1::2], 0, atol=1e-10, rtol=0)
    return density.real[:, ::2]


def band_prediction(action, q2):
    return np.array([sum(c*q2**j * (np.log(2) if j == 2 else
                                    sigma**(j-2)*(2.**(j-2)-1)/(j-2))
                         for j, c in enumerate(action) if j) for sigma in BANDS])


def production(directory, shear, size, harmonic, *, cached_only=False, shortest=False):
    times = TIMES[-1:] if shortest else TIMES
    key = ["pure-continuum", 1, shear, size, harmonic, LENGTH_X, times.tolist()]

    def compute():
        if cached_only:
            raise FileNotFoundError(f"Missing pure continuum trace: shear={shear}, N={size}, h={harmonic}")
        return continuum_response(size, shear, times.ravel(), harmonic, LENGTH_X).reshape(times.shape).tolist()

    family = "shortest" if shortest else "validation"
    return np.asarray(checkpointed_result(directory / f"pure-local-{family}-{int(shear)}.json", key, compute))


def local_actions(directory):
    coefficients = []
    for shear in (False, True):
        rows = [np.array(checkpointed_result(directory / "pure-local-coefficients.json",
                                           ["pure-local", 1, shear, n, ORDER],
                                           lambda: coefficient_rows(shear, n).tolist()))
                for n in (8, 9)]
        np.testing.assert_allclose(*rows, atol=1e-10, rtol=0)
        boson, ghost = rows[-1]
        print(f"shear={shear}; boson={boson}; ghost={ghost}", flush=True)
        trace = boson - 2*ghost
        np.testing.assert_allclose(trace[0], 0 if shear else 24/(16*pi*pi), atol=1e-10, rtol=0)
        action = -trace/4
        action[0] = 0
        coefficients.append(action)
    return coefficients


def curvature_coefficients(actions):
    conformal, shear = actions
    np.testing.assert_allclose(conformal[1]/3, -shear[1], atol=1e-10, rtol=0)
    return conformal[1]/3, (conformal[2]-6*shear[2])/18, shear[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--shear", type=int, choices=(0, 1), help="Generate continuum validation traces.")
    mode.add_argument("--coefficients-only", action="store_true")
    parser.add_argument("--shortest", action="store_true", help="Refine the shortest band only.")
    args = parser.parse_args()
    directory = args.checkpoint_dir
    if args.shortest and args.shear is None:
        parser.error("--shortest requires --shear")
    if args.shear is not None:
        for harmonic in (1, 2):
            for size in (SHORTEST_GRID,) if args.shortest else GRIDS:
                production(directory, bool(args.shear), size, harmonic, shortest=args.shortest)
                print(f"shear={args.shear}, h={harmonic}, N={size}: checkpoint ready", flush=True)
        return
    actions = local_actions(directory)
    print("Local Einstein, scalar squared, Ricci squared:", curvature_coefficients(actions), flush=True)
    if args.coefficients_only:
        return
    quartic = {}
    for shear, action in zip((False, True), actions):
        for harmonic in (1, 2):
            q2 = (2*pi*harmonic/LENGTH_X)**2
            coarse, fine = (production(directory, shear, size, harmonic, cached_only=True) for size in GRIDS)
            try:
                shortest = production(directory, shear, SHORTEST_GRID, harmonic, cached_only=True, shortest=True)
            except FileNotFoundError:
                pass
            else:
                coarse[-1], fine[-1] = fine[-1].copy(), shortest[0]
            normalization = -1/(4*LENGTH**3*LENGTH_X)
            # Subtract the independently derived Einstein kernel before
            # integrating; its exact band integral is added only for the
            # convergence check on the whole trace.
            einstein_density = action[1] * q2 / TIMES
            einstein = action[1] * q2 / (2*BANDS)
            full, coarser, fewer = (integrals(normalization*x - einstein_density, stride=stride)
                                    for x, stride in ((fine, 1), (coarse, 1), (fine, 2)))
            resolved = np.array([settled(a, b) and settled(c, d) and settled(d, e)
                                 for a, b, c, d, e in
                                 zip(coarse, fine, coarser+einstein, full+einstein, fewer+einstein)])
            print(f"Resolved bands={BANDS[resolved]}; unresolved bands={BANDS[~resolved]}")
            prediction = band_prediction(action, q2) - einstein
            residual = full - prediction
            observed = abs(full-coarser) + abs(full-fewer)
            np.testing.assert_array_less(abs(residual[resolved]), observed[resolved]+1e-10)
            empirical_quartic = action[2] + residual/(q2**2*np.log(2))
            quartic[shear, harmonic] = empirical_quartic
            print(f"shear={shear}, h={harmonic}: Einstein-subtracted={full}; "
                  f"residual={residual}; grid={full-coarser}; quadrature={full-fewer}")
            print(f"Quartic action coefficient after derived higher terms: {empirical_quartic}; "
                  f"local prediction={action[2]:.12g}")
    for harmonic in (1, 2):
        scalar = (quartic[False, harmonic]-6*quartic[True, harmonic])/18
        print(f"h={harmonic}: scalar-squared estimates={scalar}; "
              f"Ricci-squared estimates={quartic[True, harmonic]}")


if __name__ == "__main__":
    main()
