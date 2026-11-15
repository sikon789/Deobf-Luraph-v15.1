"""Exact axis-aligned CENTERLINE bounds of a cubic; no stroke padding assumption."""
import math

def extrema(values):
 p0,p1,p2,p3=values
 a=-p0+3*p1-3*p2+p3;b=2*(p0-2*p1+p2);c=p1-p0
 roots=[]
 if abs(a)<1e-14:
  if abs(b)>1e-14:roots=[-c/b]
 else:
  disc=b*b-4*a*c
  if disc>=0:
   root=math.sqrt(disc);roots=[(-b-root)/(2*a),(-b+root)/(2*a)]
 ts=[0.,1.]+[t for t in roots if 0<t<1]
 def at(t):
  u=1-t;return u*u*u*p0+3*u*u*t*p1+3*u*t*t*p2+t*t*t*p3
 vals=[at(t) for t in ts]
 return min(vals),max(vals),ts

def bounds(points):
 x=extrema([p[0] for p in points]);y=extrema([p[1] for p in points]);return (x[0],y[0],x[1],y[1])
if __name__=='__main__':
 P=(.10309408235831216*423+38,.23615914764640822*489+9)
 Q=(.9398762730617523*423+131,.510912760897002*489+147)
 T=(.027051005843111098*423+23,.01499372543231546*489+22)
 points=[P,(P[0]+T[0],P[1]+T[1]),Q,Q]
 print('CENTERLINE_BOUNDS_ONLY',bounds(points))
 assert bounds([(0,0),(0,100),(100,100),(100,0)])==(0.,0.,100.,75.)
 print('CUBIC_EXTREMA_SELFTEST_PASS')
