"""Canonical time links for the linear tilted frame on a smooth ADM seam."""

import sympy as sp


def frame_charge(metric_trace, master_trace, time, boost, flux, newton):
    energy = (4*metric_trace-6*master_trace)/(10*newton)
    area = metric_trace/(10*newton)
    tangent = flux + 3*(boost-time)/(5*newton)
    return sp.Matrix([-energy, tangent, area])


def check():
    g = sp.symbols("G", positive=True)
    steps = 4
    coordinates = []
    momenta = []
    charges = []
    for face in ("left", "right"):
        coordinates.append([sp.Matrix(sp.symbols(f"{face}_{t}_0:3"))
                            for t in range(steps+1)])
        momenta.append([sp.Matrix(sp.symbols(f"p_{face}_{t}_0:3"))
                        for t in range(steps)])
        charges.append([
            frame_charge(*sp.symbols(f"K_{face}_{t} Psi_{face}_{t}"),
                         coordinates[-1][t][0], coordinates[-1][t][2],
                         sp.Symbol(f"flux_{face}_{t}"), g)
            for t in range(steps)
        ])

    phase = sum(sign*momentum.dot(q_next-q) for sign, qs, ps in
                zip((1, -1), coordinates, momenta)
                for q, q_next, momentum in zip(qs, qs[1:], ps))
    constrained = phase.subs({p: c for ps, cs in zip(momenta, charges)
                              for p_vec, c_vec in zip(ps, cs)
                              for p, c in zip(p_vec, c_vec)}, simultaneous=True)
    # Verify the temporal correction is present before the frame match.
    assert sp.diff(constrained, coordinates[0][0][0],
                   coordinates[0][1][1]) == -3/(5*g)

    match = {right: left for left_vec, right_vec in zip(*coordinates)
             for left, right in zip(left_vec, right_vec)}
    for t in range(steps):
        for prefix in ("K", "Psi", "flux"):
            match[sp.Symbol(f"{prefix}_right_{t}")] = sp.Symbol(f"{prefix}_left_{t}")
    assert sp.expand(constrained.subs(match, simultaneous=True)) == 0

    # Unit momentum-definition Jacobian, with frame difference/common
    # coordinates normalized as difference and arithmetic mean.
    variables = list(momenta[0][0])+list(momenta[1][0])
    variables += list(coordinates[0][0])+list(coordinates[1][0])
    conditions = ((momenta[0][0]-charges[0][0])
                  .col_join(momenta[1][0]-charges[1][0])
                  .col_join(coordinates[0][0]-coordinates[1][0])
                  .col_join((coordinates[0][0]+coordinates[1][0])/2))
    assert abs(conditions.jacobian(variables).det()) == 1
    print("Temporal correction present before matching; four-link oriented phase cancels exactly.")
    print("Frame momentum and difference/average coordinate Jacobian has magnitude 1.")


if __name__ == "__main__":
    check()
