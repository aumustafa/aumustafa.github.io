import numpy as np, math
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.basePen import BasePen

WGHT = 400
font = instantiateVariableFont(TTFont("fonts/Sentient-Variable.woff2"), {"wght": WGHT})
gs = font.getGlyphSet()

class Flat(BasePen):
    def __init__(s, gs): super().__init__(gs); s.contours=[]; s.cur=[]
    def _moveTo(s,p): s.cur=[p]
    def _lineTo(s,p): s.cur.append(p)
    def _curveToOne(s,a,b,c):
        p0=s.cur[-1]
        for t in np.linspace(0,1,21)[1:]:
            u=1-t; s.cur.append(tuple(u**3*np.array(p0)+3*u*u*t*np.array(a)+3*u*t*t*np.array(b)+t**3*np.array(c)))
    def _qCurveToOne(s,a,b):
        p0=s.cur[-1]
        for t in np.linspace(0,1,17)[1:]:
            u=1-t; s.cur.append(tuple(u*u*np.array(p0)+2*u*t*np.array(a)+t*t*np.array(b)))
    def _closePath(s): s.contours.append(np.array(s.cur)); s.cur=[]
    _endPath=_closePath

pen = Flat(gs); gs["A"].draw(pen)
cons = [np.array([(x,-y) for x,y in c]) for c in pen.contours]   # flip y for SVG
def area(c): return 0.5*abs(np.dot(c[:,0],np.roll(c[:,1],-1))-np.dot(c[:,1],np.roll(c[:,0],-1)))
cons.sort(key=area, reverse=True)
outer, inner = cons[0], cons[1:]
print("contours:", len(cons), [round(area(c)) for c in cons])

# One closed path: outer loop, bridge to the counter, counter loop, bridge back
path = outer
for inn in inner:
    d = np.linalg.norm(outer[:,None,:]-inn[None,:,:],axis=2); i,j = np.unravel_index(d.argmin(), d.shape)
    o = np.roll(outer,-i,axis=0); n = np.roll(inn,-j,axis=0)
    path = np.vstack([o, o[:1], n, n[:1]])          # ends at counter start; closes back along the bridge
    break
z = path[:,0]+1j*path[:,1]
# resample uniformly by arclength (closed)
zc = np.append(z, z[0]); seg = np.abs(np.diff(zc)); s = np.concatenate([[0],np.cumsum(seg)])
N=2048; t = np.linspace(0,s[-1],N,endpoint=False)
zs = np.interp(t,s,zc.real)+1j*np.interp(t,s,zc.imag)

# Fit into the 485.4 x 300 golden-ratio frame
W,H = 485.4,300.0
x0,x1,y0,y1 = zs.real.min(),zs.real.max(),zs.imag.min(),zs.imag.max()
sc = 266/(y1-y0)
zs = (zs-complex((x0+x1)/2,(y0+y1)/2))*sc + complex(W/2,H/2)

K=160
c = np.fft.fft(zs)/N
ks = np.array([k for k in range(-K,K+1)]); cs = c[ks%N]
def pos(u, upto=None):
    return (cs*np.exp(2j*np.pi*ks*u)).sum()
U = np.linspace(0,1,1600)
curve = (np.exp(2j*np.pi*np.outer(U,ks))@cs)

# Chain: the 3 biggest circles of the real series (k != 0) + one closing arm to the exact tip
big = [i for i in np.argsort(-abs(cs)) if ks[i]!=0][:3]
def chain(u):
    p = cs[ks==0][0]; pts=[p]
    for i in big:
        p = p + cs[i]*np.exp(2j*np.pi*ks[i]*u); pts.append(p)
    tip = pos(u); pts.append(tip); return pts
np.save("/tmp/curve.npy", curve); np.save("/tmp/cs.npy", cs)

def build(u, fname):
    idx = int(u*(len(U)-1))
    f = lambda a: " L".join(f"{p.real:.1f},{p.imag:.1f}" for p in a)
    d_full = "M"+f(np.append(curve,curve[0])); d_part = "M"+f(curve[:idx+1])
    pts = chain(u)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Rotating circles with arrows tracing the letter A">',
       f'<rect width="{W}" height="{H:.0f}" fill="#ffffff"/>',
       f'<path d="{d_full}" fill="none" stroke="#004488" stroke-opacity="0.18" stroke-width="2" stroke-linejoin="round"/>',
       f'<path d="{d_part}" fill="none" stroke="#004488" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>']
    for a,b in zip(pts[:-1],pts[1:]):
        o.append(f'<circle cx="{a.real:.1f}" cy="{a.imag:.1f}" r="{abs(b-a):.1f}" fill="none" stroke="#b0b0b0" stroke-width="1.5"/>')
    for a,b in zip(pts[:-1],pts[1:]):
        v=b-a; L=abs(v); e=v/L; nrm=1j*e
        hl,hw = min(15,L*0.45), 5.5            # arrowhead length / half-width
        base=b-e*hl; tri=[b, base+nrm*hw, base-nrm*hw]
        shaft=f'x1="{a.real:.1f}" y1="{a.imag:.1f}" x2="{base.real:.1f}" y2="{base.imag:.1f}"'
        tp=" ".join(f"{p.real:.1f},{p.imag:.1f}" for p in tri)
        o.append(f'<line {shaft} stroke="#fff" stroke-opacity="0.85" stroke-width="6" stroke-linecap="round"/>')
        o.append(f'<polygon points="{tp}" fill="#fff" fill-opacity="0.85" stroke="#fff" stroke-opacity="0.85" stroke-width="3" stroke-linejoin="round"/>')
        o.append(f'<line {shaft} stroke="#000" stroke-width="2.5" stroke-linecap="round"/>')
        o.append(f'<polygon points="{tp}" fill="#000"/>')
    for p in pts[:-1]:
        o.append(f'<circle cx="{p.real:.1f}" cy="{p.imag:.1f}" r="3" fill="#000"/>')
    o.append("</svg>")
    open(fname,"w").write("\n".join(o)+"\n")
    print(fname, [round(abs(b-a),1) for a,b in zip(pts[:-1],pts[1:])])

import sys
build(0.40, "pub-thumbs/fourier-A.svg")