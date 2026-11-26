"""Compare short proper-time bands after restoring the diagnostic zero sector."""

import argparse
import json
from pathlib import Path

import numpy as np

from curvature_band_matching import common_volume_shift, momentum_projections
from curvature_cutoff_extrapolation import intercept_weights
from matched_wave_comparison import mixed_wave, pure_wave
from short_mixed_quadrature import mixed_projections


def read_checkpoint(directory, name):
    return json.loads((directory / f"{name}.json").read_text())


def restored_pure(directory):
    length = 5.6
    prior = read_checkpoint(directory, "curvature-long-56")
    short = read_checkpoint(directory, "curvature-long-56-018")
    shifts = read_checkpoint(directory, "pure-low-wave-zero-sector")
    square = (2 * np.pi / length)**2 * np.array([1, 4])
    momentum_weights = intercept_weights(square)
    cutoffs = np.array([.024, .021, .018])
    results, variations, coherent_variations = [], [], []
    for cutoff, cache, sizes in zip(cutoffs, (prior, prior, short),
                                  ((49, 53), (49, 53), (53, 57))):
        waves, changes = zip(*(pure_wave(cache, length, cutoff, h, sizes, signed_refinement=True)
                               for h in (1, 2)))
        responses = np.column_stack(waves)
        directions = np.stack(changes, axis=1)
        numerical = abs(directions).sum(axis=-1)
        for row, shear in enumerate((False, True)):
            for col, h in enumerate((1, 2)):
                key = json.dumps(["pure-low-wave-zero", 1, length, cutoff, h, shear, sizes[-1]])
                responses[row, col] -= shifts[key]
        responses[0] -= common_volume_shift(length)

        def project(data):
            einstein, scalar, ricci = momentum_projections(*data, square)
            return np.array([cutoff * einstein, momentum_weights @ scalar,
                             momentum_weights @ ricci])

        weights = np.column_stack([project(unit.reshape(2, 2)) for unit in np.eye(4)])
        result, observed = project(responses), abs(weights) @ numerical.ravel()
        results.append(result)
        variations.append(observed)
        paired = abs(weights @ directions.reshape(4, 3)).sum(axis=-1)
        coherent_variations.append(paired)
        print(f"Pure Lx={length}, sigma={cutoff}: {result}; raw-grid shifts={observed}; "
              f"paired shifts={paired}")
    for start in (0, 1):
        weights = intercept_weights(cutoffs[start:])
        print(f"Pure intercept for {cutoffs[start:]}: {weights @ results[start:]}; "
              f"propagated raw-grid shifts={abs(weights) @ variations[start:]}; "
              f"paired shifts={abs(weights) @ coherent_variations[start:]}")


def mixed_zero_projection(directory, length, cutoff, size):
    if cutoff == .018 or length == 2.4:
        name = f"mixed-zero-sector-{round(1000*cutoff):03d}"
        cache = read_checkpoint(directory, name)
        entries = [cache[json.dumps(["mixed-zero-sector", 1, length, size, axis, cutoff, 8])]
                   for axis in (0, 1)]
    else:
        cache = read_checkpoint(directory, "mixed-matched-zero-sector")
        entries = [cache[json.dumps(["mixed-matched-zero", 1, 1.8, 1, 25, axis,
                                    [.024, .021]])][(.024, .021).index(cutoff)]
                   for axis in (0, 1)]
    # Both orientation projections are linear in the integrated heat traces.
    return np.array(mixed_projections(*entries, length_x=length))


def restored_mixed(directory):
    sequences = (
        (1.8, ((.024, (21, 25), "mixed-024"), (.021, (21, 25), "mixed-021"),
               (.018, (25, 29), "mixed-018"))),
        (2.4, ((.021, (29, 33), "mixed-long-24"), (.018, (33, 37), "mixed-long-24-018"))),
    )
    all_results, all_variations, all_paired = [], [], []
    for length, sequence in sequences:
        results, variations, paired_variations = [], [], []
        for cutoff, sizes, name in sequence:
            projected, shifts, paired = mixed_wave(directory, length, 1, cutoff, sizes, name, paired=True)
            full = projected - mixed_zero_projection(directory, length, cutoff, sizes[-1])
            results.append(full)
            variations.append(shifts)
            paired_variations.append(paired)
            print(f"Mixed Lx={length}, sigma={cutoff}: restored={full}; raw-grid shifts={shifts}; paired shifts={paired}")
        cutoffs = np.array([row[0] for row in sequence])
        for start in range(len(cutoffs) - 1):
            weights = intercept_weights(cutoffs[start:])
            intercept = weights @ results[start:]
            observed = abs(weights) @ variations[start:]
            print(f"Mixed Lx={length}, intercept for {cutoffs[start:]}: "
                  f"{intercept}; propagated raw-grid shifts={observed}; "
                  f"paired shifts={abs(weights) @ paired_variations[start:]}")
            print(f"  RX plus half Ricci-clock: {intercept[0] + intercept[1]/2:.12g}; "
                  f"propagated shift={observed[0] + observed[1]/2:.12g}")
        all_results.append(results)
        all_variations.append(variations)
        all_paired.append(paired_variations)
    momenta_squared = (2 * np.pi / np.array([1.8, 2.4]))**2
    weights = intercept_weights(momenta_squared)
    projected, shifts, paired_shifts = [], [], []
    for i, cutoff in enumerate((.021, .018)):
        responses = np.array([all_results[0][i+1], all_results[1][i]])
        observed = np.array([all_variations[0][i+1], all_variations[1][i]])
        print(f"Mixed difference at sigma={cutoff} (lower momentum minus higher momentum): "
              f"{responses[1]-responses[0]}")
        projected.append(weights @ responses)
        shifts.append(abs(weights) @ observed)
        paired_shifts.append(abs(weights) @ np.array([all_paired[0][i+1], all_paired[1][i]]))
        print(f"Two-momentum projection at sigma={cutoff}: {projected[-1]}; shifts={shifts[-1]}")
    weights = intercept_weights(np.array([.021, .018]))
    print(f"Joint two-momentum, two-cutoff intercept: {weights @ projected}; "
          f"propagated shifts={abs(weights) @ shifts}; paired shifts={abs(weights) @ paired_shifts}")
    print("The momentum projection uses two boxes and assumes negligible residual box dependence.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--part", choices=("pure", "mixed"), required=True)
    args = parser.parse_args()
    try:
        (restored_pure if args.part == "pure" else restored_mixed)(args.checkpoint_dir)
    except (OSError, KeyError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print("Diagnostic only. Refinement shifts do not bound omitted cutoff or momentum terms.")


if __name__ == "__main__":
    main()
