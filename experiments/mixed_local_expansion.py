"""Derive the mixed short-time coefficients from continuum Fourier vertices."""

import argparse
from math import pi
from pathlib import Path

import numpy as np
from scipy.special import roots_genlaguerre

from curvature_band_matching import checkpointed_result
from direct_curvature_insertion import longitudinal_fourier, mixed_operator_jets
from mixed_transverse_continuum import (
    BANDS, GRIDS, LENGTH_SEQUENCE, SHORTEST_REFINEMENT, TIMES, integrals, matched_trace, trace_rows,
)
from short_mixed_quadrature import mixed_projections
from transverse_insertion_sum import WAVE


CHANNELS = 22


def vertices_at(size, axis, radius, wave=1.):
    p = radius / (WAVE * np.sqrt(3))
    jets = mixed_operator_jets(size, (p, 0., p, p), axis, False, 2*pi/wave, 1)
    return longitudinal_fourier(jets, size).reshape(3, 3, 2, size, 11, 2, size, 11)


def vertex_polynomials(axis):
    """Reconstruct degree-(2-w) vertices in loop momentum and probe momentum."""
    size = 13
    samples = [(longitudinal, radius) for radius in (-1., 0., 1.) for longitudinal in (-1, 0, 1)]
    jets = {radius: vertices_at(size, axis, radius) for radius in (-1., 0., 1.)}
    independent_size = 17
    independent = vertices_at(independent_size, axis, .73, wave=1.4)
    result = {}
    for b in range(3):
        for winding in range(3):
            degree = 2 - winding
            powers = [(i, j, degree-i-j) for i in range(degree+1) for j in range(degree+1-i)]
            design = np.array([[k**i * p**j for i, j, _ in powers] for k, p in samples])
            for delta in range(-b, b+1):
                blocks = np.array([jets[p][b, winding, :, (k+delta) % size, :, :, k % size, :]
                                   .reshape(CHANNELS, CHANNELS) for k, p in samples])
                coefficients = (np.linalg.pinv(design) @ blocks.reshape(len(samples), -1)).reshape(-1, CHANNELS, CHANNELS)
                prediction = sum(c * 1.4**(i+m) * .73**j for (i, j, m), c in zip(powers, coefficients))
                actual = independent[b, winding, :, (1+delta) % independent_size, :, :, 1, :].reshape(
                    CHANNELS, CHANNELS)
                np.testing.assert_allclose(prediction, actual, rtol=0, atol=1e-10)
                coefficients[abs(coefficients) < 1e-12] = 0
                result[b, winding, delta] = (powers, coefficients)
    return result


def thermal_polynomial(vertices, k, p, order):
    """Trace the exp(-H) series after removing the scalar flat heat factor."""
    width = 3 * CHANNELS
    center = slice(CHANNELS, 2*CHANNELS)
    blocks = {}
    for (b, winding, delta), (powers, coefficients) in vertices.items():
        for source in (-1, 0, 1):
            dest = source + delta
            if not -1 <= dest <= 1:
                continue
            r = slice((dest+1)*CHANNELS, (dest+2)*CHANNELS)
            c = slice((source+1)*CHANNELS, (source+2)*CHANNELS)
            # Evaluate the vertex on k+source*q and collect the powers of q.
            for (i, j, m), coefficient in zip(powers, coefficients):
                factors = ((k**i, 0),)
                if i == 1:
                    factors += ((source, 1),)
                elif i == 2:
                    factors += ((2*k*source, 1), (source**2, 2))
                for factor, power in factors:
                    key = b, winding, m + power
                    blocks.setdefault(key, np.zeros((width, width), dtype=complex))[r, c] += (
                        factor * p**j * coefficient)
    flat = blocks.pop((0, 0, 0))
    np.testing.assert_allclose(flat, (k*k+p*p)*np.eye(width), rtol=0, atol=1e-9)
    state = np.zeros((3, 3, order+1, width, CHANNELS), dtype=complex)
    state[0, 0, 0, center] = np.eye(CHANNELS)
    output = np.zeros(order+1, dtype=complex)
    terms = [(b, v, q, block) for (b, v, q), block in blocks.items() if np.any(block)]
    for power in range(1, order+5):
        updated = np.zeros_like(state)
        for b, v, q, block in terms:
            updated[b:, v:, q:] -= block @ state[:3-b, :3-v, :order+1-q] / power
        state = updated
        output += np.trace(state[2, 2, :, center, :], axis1=-2, axis2=-1)
    return output


def coefficients(axis, nodes, order):
    vertices = vertex_polynomials(axis)
    longitudinal, wx = np.polynomial.hermite.hermgauss(nodes)
    square, wp = roots_genlaguerre(nodes, .5)
    total = sum((a*b * thermal_polynomial(vertices, k, np.sqrt(p2), order)
                 for k, a in zip(longitudinal, wx) for p2, b in zip(square, wp)))
    np.testing.assert_allclose(total.imag, 0, rtol=0, atol=1e-8)
    # (2! 2!) for amplitude derivatives, divided by the two real phases.
    density = 2 * total.real * (2*pi) / (2*pi)**4
    np.testing.assert_allclose(density[0], 1/(2*pi*pi), rtol=0, atol=1e-10)
    np.testing.assert_allclose(density[1::2], 0, rtol=0, atol=1e-10)
    return density[2::2]


def validate(directory, projected):
    # projected contains the coefficients of (s q^2)^j, with all four
    # momentum directions integrated before the short-time expansion.
    corrected = []
    for index, length in enumerate(LENGTH_SEQUENCE):
        q2 = (2*pi/length)**2
        measured = np.array(mixed_projections(*(trace_rows(
            directory, index, GRIDS[index][-1], axis, cached_only=True)[0] for axis in (0, 1)),
            length_x=length))
        predicted = np.array([np.polynomial.polynomial.polyval(TIMES*q2, row) for row in projected])
        band_measured = np.array([integrals(channel) for channel in measured])
        band_terms = np.stack((np.full(BANDS.shape, np.log(2)), *[
            (2**order-1)/order * (BANDS*q2)**order for order in range(1, projected.shape[1])
        ]))
        predictions = np.cumsum(projected[:, :, None] * band_terms, axis=1)
        print(f"Lx={length:g}: endpoint max residual={abs(measured[..., [0,-1]]-predicted[..., [0,-1]]).max(axis=(1,2))}")
        print("Maximum band residual by truncation [RX, Ricci-clock]:",
              abs(band_measured[:, None] - predictions).max(axis=-1))
        print("Measured minus full prediction by band:", band_measured - predictions[:, -1])
        corrected.append(band_measured - (predictions[:, -1] - predictions[:, 0]))
    corrected = np.array(corrected)
    print("Band-constant ranges after subtracting independently derived nonconstant terms:",
          np.stack((corrected.min(axis=(0, 2)), corrected.max(axis=(0, 2))), axis=-1))

    size, shortest = SHORTEST_REFINEMENT
    try:
        traces = [matched_trace(directory, len(LENGTH_SEQUENCE)-1, size, axis,
                                cached_only=True, bands=(shortest,))[0] for axis in (0, 1)]
    except FileNotFoundError:
        return
    length = LENGTH_SEQUENCE[-1]
    q2 = (2*pi/length)**2
    measured = np.array(mixed_projections(*traces, length_x=2*length, harmonic=2))
    predicted = np.array([np.polynomial.polynomial.polyval(TIMES[shortest]*q2, row) for row in projected])
    residual = np.array([integrals(row[None, :], times=TIMES[[shortest]])[0]
                         for row in measured - predicted])
    print(f"Lowest doubled-box shortest-band residual at N={size}:", residual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--order", type=int, choices=(8, 12), default=8, help="Highest power of q before projection.")
    args = parser.parse_args()
    # A term with probe degree r has at most r+4 factors and loop degree r+6.
    min_nodes = (args.order + 8) // 2
    values = []
    for axis in (0, 1):
        rows = [np.array(checkpointed_result(args.checkpoint_dir / "mixed-local-expansion.json",
                                           ["mixed-local-expansion", 1, axis, nodes, args.order],
                                           lambda: coefficients(axis, nodes, args.order).tolist()))
                for nodes in (min_nodes, min_nodes + 1)]
        np.testing.assert_allclose(*rows, rtol=0, atol=1e-10)
        values.append(rows[-1])
        print(f"axis={axis}: density coefficients={rows[-1]}", flush=True)
    spatial, temporal = values
    projected = np.array([temporal/24, (spatial-temporal)/8])
    print("Projected coefficients in ascending powers of sq^2:", projected, flush=True)
    print("Predicted constant dyadic-band coefficients:", projected[:, 0] * np.log(2))
    validate(args.checkpoint_dir, projected)


if __name__ == "__main__":
    main()
