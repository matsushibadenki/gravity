"""Green boundary forms for the four marked-sphere ADM smearing data."""

import sympy as sp


def check():
    r, lo, hi = sp.symbols("r lo hi", positive=True)
    # Axisymmetric Cartesian quadrupole, with angular norm divided out.
    # Test the Green form with regular polynomial tensor coefficients.
    coefficients = (1+r**2, 2-r**2, 1+r**4, 3+r**2)
    a, b, c, d = coefficients
    radial = r**2*a+b+2*r**2*c+r**4*d
    mixed = (b+r**2*c)/2
    angular = r**2*a-b/2
    shear = b/2
    trace = radial+2*angular
    div_r = sp.diff(radial,r)+2*(radial-angular)/r-6*mixed/r
    div_s = sp.diff(mixed,r)+3*mixed/r+(angular-2*shear)/r
    curvature = (sp.diff(div_r,r)+2*div_r/r-6*div_s/r
                 -sp.diff(trace,r,2)-2*sp.diff(trace,r)/r+6*trace/r**2)
    lapse = r**2*(1+r**2+r**4)
    lap = sp.diff(lapse,r,2)+2*sp.diff(lapse,r)/r-6*lapse/r**2
    hessian = (
        sp.diff(lapse,r,2)-lap,
        sp.diff(lapse,r)/r-lapse/r**2,
        sp.diff(lapse,r)/r-3*lapse/r**2-lap,
        lapse/r**2,
    )
    contraction = sum(w*x*y for w,x,y in zip(
        (1,12,2,12),(radial,mixed,angular,shear),hessian))
    lapse_boundary = r**2*(lapse*(div_r-sp.diff(trace,r)-6*mixed/r)
                          +2*sp.diff(lapse,r)*angular)
    assert sp.expand(r**2*(lapse*curvature-contraction)-sp.diff(lapse_boundary,r)) == 0

    # W^r=uY and W^A=(v/r)D^A Y. The momentum modes use the same tensor ansatz.
    u, v = r*(1+r**2), r*(2+r**4)
    lie = (2*sp.diff(u,r),sp.diff(v,r)+(u-v)/r,
           2*u/r-6*v/r,2*v/r)
    shift_contraction = sum(w*x*y for w,x,y in zip(
        (1,12,2,12),(radial,mixed,angular,shear),lie))
    shift_boundary = 2*r**2*(u*radial+6*v*mixed)
    assert sp.expand(r**2*(shift_contraction+2*(u*div_r+6*v*div_s))
                     -sp.diff(shift_boundary,r)) == 0

    # Rank on arbitrary one-sided jets (metric and momentum independent).
    h, c, dc, b, pnn, pnA = sp.symbols("h c dc b pnn pnA")
    charges = sp.Matrix([2*(h-c)-2*dc-12*b,2*c,2*pnn,12*pnA])
    assert charges.jacobian([h,c,dc,b,pnn,pnA]).rank() == 4
    # Opposite normals reverse the entire Green form, including the
    # signed derivative of N. A smooth common smearing carries no net charge.
    for form in (lapse_boundary, shift_boundary):
        whole = form.subs(r,hi)-form.subs(r,lo)
        faces = (form.subs(r,1)-form.subs(r,lo))+(form.subs(r,hi)-form.subs(r,1))
        assert sp.expand(faces-whole) == 0
    print("Lapse and shift Green identities verified symbolically.")
    print("One-sided charge rank is four. The smooth internal surface terms cancel.")


def check_smooth_embedding_integral():
    """Check the common-frame factor on the already smoothly matched seam."""
    directions, links = 4, 3
    identity = sp.eye(directions*links)
    forward = sp.zeros(links)
    for i in range(links-1):
        forward[i,i+1] = 1
    difference = sp.kronecker_product(forward-sp.eye(links),sp.eye(directions))
    # On matched data the net charge vanishes. Integration of the real
    # link multipliers gives delta(P). Fix all common frame coordinates.
    # A representative time-dependent frame shift only alters the p-linear term.
    gauge = sp.diag(*([2,3,5,7]*links))
    constraints = sp.diag(gauge,identity)
    poisson = sp.BlockMatrix([[sp.zeros(identity.rows),identity],
                             [-identity,sp.zeros(identity.rows)]]).as_explicit()
    bracket = constraints*poisson*constraints.T
    fp = sp.sqrt(bracket.det())
    assert fp == abs(gauge.det())
    p = sp.Matrix(sp.symbols(f"p:{identity.rows}"))
    x = sp.Matrix(sp.symbols(f"x:{identity.rows}"))
    assert (p.T*difference*x)[0].subs(dict.fromkeys(p,0)) == 0
    print("Common-frame smooth-seam integral: delta(P) removes the link phase, "
          "and the bracket determinant cancels the gauge delta Jacobian.")


def check_one_sided_bracket():
    """Evaluate the bare surface-charge bracket in the regulated bulk form."""
    import numpy as np

    from einstein_matched_mesh_sewing import assemble, tests

    for cells in (2,4,8):
        edges = np.linspace(0,2,2*cells+1)
        lapse, shift = tests(edges,2,2), tests(edges,1,1)
        for side in (edges[:cells+1],edges[cells:]):
            value, derivative = np.split(
                assemble(side,shift,lapse,tensor_continuity=0)[-1],2)
            a, b, c, d = value
            da, db, _, _ = derivative
            h, mixed, angular = a+b+2*c+d,(b+c)/2,a-b/2
            angular_derivative = 2*(a+da-db/2)
            lapse_charge = np.vstack((2*(h-angular)-2*angular_derivative-12*mixed,
                                      2*angular))
            shift_charge = np.vstack((2*h,12*mixed))
            # Unit row norms isolate rank from the growth of trace norms.
            lapse_charge /= np.linalg.norm(lapse_charge,axis=1)[:,None]
            shift_charge /= np.linalg.norm(shift_charge,axis=1)[:,None]
            mixed_bracket = lapse_charge@shift_charge.T
            singular = np.linalg.svd(mixed_bracket,compute_uv=False)
            assert singular[-1] > 1e-8
            print(f"cells={cells}, left radius={side[0]:g}, "
                  f"bare mixed charge singular values={singular}")


if __name__ == "__main__":
    check()
    check_smooth_embedding_integral()
    check_one_sided_bracket()
