"""Stationary relative-time energy using a Legendre basis for the same tensor span."""

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss, legvander
from scipy.linalg import solve_triangular


def face(order, lo, hi, extra_points=0, smearings=1):
    nodes, weights = leggauss(2*order+18+extra_points)
    r = lo+(hi-lo)*(nodes+1)/2
    scale = np.sqrt((hi-lo)/2 * weights * (4/5)*r**2)
    def tensors(r):
        s = r*r
        p = legvander(2*(s-lo*lo)/(hi*hi-lo*lo)-1, order+2)
        one, zero = np.ones_like(r), np.zeros_like(r)
        components = [[s,one,2*s,s*s], [zero,one/2,s/2,zero],
                      [s,-one/2,zero,zero], [zero,one/2,zero,zero]]
        return np.array([(p[:,:,None]*np.array(c).T[:,None,:]).reshape(len(r),-1)
                         for c in components])
    a,b,c,d = tensors(r)
    raw = np.vstack([scale[:,None]*row*factor for row,factor in
                     ((a,1),(b,np.sqrt(12)),(c,np.sqrt(2)),(d,np.sqrt(12)))])
    q, upper = np.linalg.qr(raw, mode="reduced")
    def white(rows):
        return solve_triangular(upper.T, rows.T, lower=True).T
    trace = white(scale[:,None]*(a+2*c))
    kinetic = 32*(np.eye(q.shape[1])-trace.T@trace/2)
    rows = []
    mapped_s = Legendre([(lo**2+hi**2)/2,(hi**2-lo**2)/2], domain=[lo**2,hi**2])
    clamp = 1-mapped_s if lo == 0 else (1-mapped_s)*(4-mapped_s)
    for degree in range(smearings):
        probe = Legendre.basis(degree, domain=mapped_s.domain)
        proper = clamp*probe
        for f,g in ((proper,0*proper),(0*proper,proper)):
            coeff = [2*g,2*f,2*(f.deriv()+g),4*g.deriv()]
            raw_shift = np.array([poly(r*r) for poly in coeff]).T
            amps = [np.sum(component[:,:4]*raw_shift, axis=1) for component in (a,b,c,d)]
            shift = np.concatenate([scale*value*factor for value,factor in
                                    zip(amps,(1,np.sqrt(12),np.sqrt(2),np.sqrt(12)))])
            rows.append(shift@q)
        # Laplacian of r^2 Y f(r^2), followed by projection on trace momentum.
        f = clamp**2*probe
        rows.append((-2*scale*r*r*(14*f.deriv()(r*r)+4*r*r*f.deriv(2)(r*r)))@trace)
    flux = white(tensors(np.array([1.]))[:2,0,:])
    proper_basis, upper_rows = np.linalg.qr(np.array(rows).T, mode="reduced")
    assert np.linalg.matrix_rank(upper_rows) == len(rows)
    conditions = np.vstack((proper_basis.T,flux))
    compliance = conditions@np.linalg.solve(kinetic,conditions.T)
    count = len(rows)
    return compliance[count:,count:] - compliance[count:,:count]@np.linalg.solve(
        compliance[:count,:count],compliance[:count,count:])


def check():
    jump = np.array([-6.,1.])/16
    residuals = {}
    for order in (2,3,4,6,8,12,16,24,32,48,64,96,128):
        compliance = face(order,0,1)+face(order,1,2)
        curvature = jump@np.linalg.solve(compliance,jump)
        residuals[order] = curvature
        print(f"N={order:3d}  residual={curvature:.12g}  N residual={order*curvature:.8g}")
        if order >= 32:
            finer = face(order,0,1,12)+face(order,1,2,12)
            np.testing.assert_allclose(curvature,jump@np.linalg.solve(finer,jump),
                                       rtol=3e-7, atol=1e-10)
        if order in (2,3):
            np.testing.assert_allclose(curvature,{2:.12548834,3:.10184998}[order], atol=1e-7)

    for orders in ((24,32,48,64), (48,64,96,128)):
        h = 1/np.array(orders)
        fit = np.polynomial.polynomial.polyfit(h, [residuals[k] for k in orders], 2)
        print(f"Orders {orders}: free intercept={fit[0]:.8g}, 1/N slope={fit[1]:.8g}")

    # An independent sequence also refines the proper smearing space.
    for order in (4,8,16,32,64,96,128):
        count = order-1
        compliance = face(order,0,1,smearings=count)+face(order,1,2,smearings=count)
        curvature = jump@np.linalg.solve(compliance,jump)
        finer = face(order,0,1,12,count)+face(order,1,2,12,count)
        relative_change = abs(jump@np.linalg.solve(finer,jump)/curvature-1)
        print(f"N={order}, smearings/family={count}: residual={curvature:.12g}, "
              f"quadrature change={relative_change:.3g}")
        assert relative_change < 3e-6


if __name__ == "__main__":
    check()
