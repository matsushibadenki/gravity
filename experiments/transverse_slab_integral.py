"""Integrate disjoint-slab mutual information over transverse momenta."""

from math import log, sqrt

import numpy as np

from disjoint_slab_information import mutual_information


def focused_rule(points):
    nodes, weights = np.polynomial.legendre.leggauss(points)
    angles = np.pi * nodes**3
    weights = weights * (1.5 * nodes**2)
    assert np.isclose(np.sum(weights), 1)
    return (angles, angles), (weights, weights)


def main():
    spacing, width = 0.15, 0.6
    gaps = (0.6, 1.2, 1.8, 2.4, 3.0, 3.6)
    strength = 0.45 * sqrt(3 / 2)
    results = {}
    for nx, points in ((64, 16), (64, 24), (64, 32), (96, 32)):
        shape = (nx, points, points)
        values = mutual_information(spacing, shape, width, gaps, strength, "improved",
                                    transverse_rule=focused_rule(points))
        assert np.all(values > 0) and np.all(np.diff(values, axis=0) < 0)
        assert np.all(values[:, 1] >= values[:, 0])
        results[nx, points] = values
        print(f"Lx={nx*spacing:.1f}, transverse points={points}^2", flush=True)
        for gap, (shell, joint) in zip(gaps, values):
            print(f"  d={gap:.1f}: shell={shell:.10f}, joint={joint:.10f}", flush=True)

    reference = results[64, 32]
    for key in ((64, 16), (64, 24), (96, 32)):
        differences = np.abs(results[key] - reference) / reference
        print(f"{key}: relative differences from (64, 32), shell="
              f"{np.round(100*differences[:, 0], 3)}%", flush=True)
    assert np.max(np.abs(results[64, 24] - reference) / reference) < np.max(
        np.abs(results[64, 16] - reference) / reference
    )
    longer = results[96, 32]
    print("Longer-box shell effective slopes:",
          [round(log(left / right) / 0.6, 4) for left, right in zip(longer[:-1, 0], longer[1:, 0])],
          flush=True)
    baseline = mutual_information(spacing, (96, 32, 32), width, gaps, 0, "improved",
                                  transverse_rule=focused_rule(32))
    print("Coupled minus uncoupled, columns shell and joint:", longer - baseline, flush=True)


if __name__ == "__main__":
    main()
