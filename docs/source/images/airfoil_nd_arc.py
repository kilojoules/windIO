
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
import matplotlib.pylab as plt
import matplotlib.patches as patches 
from matplotlib.patches import PathPatch, FancyArrowPatch
from matplotlib.path import Path

af = np.array([[ 1.00000e+00, -8.91000e-03],
       [ 9.83380e-01, -5.58000e-03],
       [ 9.64570e-01, -2.61000e-03],
       [ 9.43639e-01, -5.10000e-04],
       [ 9.20709e-01,  5.80000e-04],
       [ 8.95879e-01,  4.00000e-04],
       [ 8.69269e-01, -1.34000e-03],
       [ 8.41008e-01, -4.79000e-03],
       [ 8.11238e-01, -1.00200e-02],
       [ 7.80088e-01, -1.71500e-02],
       [ 7.47717e-01, -2.63100e-02],
       [ 7.14277e-01, -3.72200e-02],
       [ 6.79927e-01, -4.96600e-02],
       [ 6.44836e-01, -6.31810e-02],
       [ 6.09166e-01, -7.72210e-02],
       [ 5.73096e-01, -9.11610e-02],
       [ 5.36795e-01, -1.04421e-01],
       [ 5.00435e-01, -1.16521e-01],
       [ 4.64195e-01, -1.27101e-01],
       [ 4.28244e-01, -1.35911e-01],
       [ 3.92764e-01, -1.42831e-01],
       [ 3.57914e-01, -1.47801e-01],
       [ 3.23863e-01, -1.50802e-01],
       [ 2.90783e-01, -1.51882e-01],
       [ 2.58823e-01, -1.51082e-01],
       [ 2.28132e-01, -1.48471e-01],
       [ 1.98882e-01, -1.44111e-01],
       [ 1.71182e-01, -1.38101e-01],
       [ 1.45181e-01, -1.30521e-01],
       [ 1.21011e-01, -1.21551e-01],
       [ 9.87710e-02, -1.11361e-01],
       [ 7.85810e-02, -1.00181e-01],
       [ 6.05210e-02, -8.82510e-02],
       [ 4.47000e-02, -7.58210e-02],
       [ 3.11800e-02, -6.31210e-02],
       [ 2.00300e-02, -5.03510e-02],
       [ 1.13000e-02, -3.76400e-02],
       [ 5.03000e-03, -2.50200e-02],
       [ 1.26000e-03, -1.25600e-02],
       [ 0.00000e+00, -1.19000e-03],
       [ 1.26000e-03,  1.32600e-02],
       [ 5.03000e-03,  2.66700e-02],
       [ 1.13000e-02,  4.00100e-02],
       [ 2.00300e-02,  5.33910e-02],
       [ 3.11800e-02,  6.65510e-02],
       [ 4.47000e-02,  7.93810e-02],
       [ 6.05210e-02,  9.16710e-02],
       [ 7.85810e-02,  1.03231e-01],
       [ 9.87710e-02,  1.13851e-01],
       [ 1.21011e-01,  1.23321e-01],
       [ 1.45181e-01,  1.31461e-01],
       [ 1.71182e-01,  1.38141e-01],
       [ 1.98882e-01,  1.43251e-01],
       [ 2.28132e-01,  1.46731e-01],
       [ 2.58823e-01,  1.48661e-01],
       [ 2.90783e-01,  1.49081e-01],
       [ 3.23863e-01,  1.48071e-01],
       [ 3.57914e-01,  1.45781e-01],
       [ 3.92764e-01,  1.42301e-01],
       [ 4.28244e-01,  1.37761e-01],
       [ 4.64195e-01,  1.32291e-01],
       [ 5.00435e-01,  1.26011e-01],
       [ 5.36795e-01,  1.19091e-01],
       [ 5.73096e-01,  1.11691e-01],
       [ 6.09166e-01,  1.03911e-01],
       [ 6.44836e-01,  9.58710e-02],
       [ 6.79927e-01,  8.76610e-02],
       [ 7.14277e-01,  7.93910e-02],
       [ 7.47717e-01,  7.11610e-02],
       [ 7.80088e-01,  6.30910e-02],
       [ 8.11238e-01,  5.52810e-02],
       [ 8.41008e-01,  4.78000e-02],
       [ 8.69269e-01,  4.07400e-02],
       [ 8.95879e-01,  3.41700e-02],
       [ 9.20709e-01,  2.81200e-02],
       [ 9.43639e-01,  2.26600e-02],
       [ 9.64570e-01,  1.77500e-02],
       [ 9.83380e-01,  1.33300e-02],
       [ 1.00000e+00,  9.37000e-03]])[::-1]

def compute_curve_length(x, y):
    st = np.zeros_like(x)
    st[1:] = np.cumsum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
    xi = PchipInterpolator(st, x)
    yi = PchipInterpolator(st, y)

    def grad_mag(s):
        return np.sqrt(xi(s, 1) ** 2 + yi(s, 1) ** 2 )

    s = np.zeros_like(x)
    for i, (st1, st2) in enumerate(zip(st[:-1], st[1:]), 1):
        s[i] = quad(grad_mag, st1, st2)[0] + s[i - 1]
    return s

class InterpArc:
    def __init__(self, s, x, y):
        self._xi = PchipInterpolator(s, x)
        self._yi = PchipInterpolator(s, y)

    def __call__(self, s):
        return np.array([self._xi(s), self._yi(s)]).T



def plot_af(ax):
    # Define custom Bezier path vertices and codes
    verts = [
        [1.02, 0.005],      # Move to start
        [1.02, 0.02],      # Control point 1
        [1.02, 0.03],      # Control point 1
        [0.96, 0.045],    # Control point 2
        [0.90, 0.06],    # Control point 2
    ]

    codes = [
        Path.MOVETO,   # Move to start
        Path.LINETO,
        Path.CURVE4,   # Quadratic Bezier control point 2
        Path.CURVE4,   # Quadratic Bezier control point 2
        Path.CURVE4,   # Quadratic Bezier control point 2
    ]

    path = Path(verts, codes)

    # Add the Bezier path (no arrowhead)
    curve_patch = PathPatch(
        path,
        facecolor='none',
        edgecolor='blue',
        linewidth=2
    )
    ax.add_patch(curve_patch)

    # Add an arrowhead at the end point of the curve
    arrow = FancyArrowPatch(
        posA=verts[-1],  # from last control point
        posB=(0.85, 0.07),  # to end point
        arrowstyle='->',
        mutation_scale=10,
        color='blue',
        linewidth=2
    )
    ax.add_patch(arrow)

    # Define custom Bezier path vertices and codes
    verts = [
        [0.85, -0.03],    # Control point 2
        [0.96, -0.01],    # Control point 2
        [1.02, -0.03],      # Control point 1
        [1.02, -0.035],      # Control point 1
        [1.02, -0.005],      # Move to start
    ]

    codes = [
        Path.MOVETO,   # Move to start
        Path.CURVE4,   # Quadratic Bezier control point 2
        Path.CURVE4,   # Quadratic Bezier control point 2
        Path.CURVE4,   # Quadratic Bezier control point 2
        Path.LINETO,
    ]

    path = Path(verts, codes)

    # Add the Bezier path (no arrowhead)
    curve_patch = PathPatch(
        path,
        facecolor='none',
        edgecolor='blue',
        linewidth=2
    )
    ax.add_patch(curve_patch)
    # Add an arrowhead at the end point of the curve
    arrow = FancyArrowPatch(
        posA=(1.02, -0.02),  # from last control point
        posB=(1.02, 0.01),  # to end point
        arrowstyle='->',
        mutation_scale=10,
        color='blue',
        linewidth=2
    )
    ax.add_patch(arrow)

    ax.plot(af[:, 0], af[:,1], "k-", linewidth=2)

    ax.annotate(
        "nd_arc_position = 0.0", 
        xy=(1.02, 0.),                     # point to annotate
        xytext=(1.05, 0.),  # text position offset
        fontsize=15,
        fontfamily='monospace',
        color='black'
    )
    ax.annotate(
        "nd_arc_position = 1.0", 
        xy=(1.02, 0.),                     # point to annotate
        xytext=(1.05, -0.05),  # text position offset
        fontsize=15,
        fontfamily='monospace',
        color='black'
    )
    return ax

fig, ax = plt.subplots(figsize=(10, 4))
ax = plot_af(ax)
plt.axis('off')
plt.axis("equal")
plt.tight_layout()
plt.savefig("airfoil_nd_arc.svg")

# midpoint+width

fig, ax = plt.subplots(figsize=(10, 4))
ax = plot_af(ax)

s = compute_curve_length(af[:, 0], af[:, 1])
s /= s[-1]
interp = InterpArc(s, af[:, 0], af[:, 1])
cap = interp(np.linspace(0.25, 0.4, 30))
cap_pts = interp(np.linspace(0.25, 0.4, 3))
plt.plot(cap[:, 0], cap[:, 1], "r-", linewidth=5)
plt.plot(cap_pts[:, 0], cap_pts[:, 1], 'go', markersize=10)

ix = 1
for label, pt in zip(["start_nd_arc", "midpoint_nd_arc", "end_nd_arc"], cap_pts):
    ax.annotate(
        label, 
        xy=pt,                     # point to annotate
        xytext=(pt[0], pt[1]+0.05 * ix),  # text position offset
        arrowprops=dict(arrowstyle='->', color='black'),
        fontsize=15,
        fontfamily='monospace',
        color='black'
    )
    ix += 1

# plot the width
arrow = FancyArrowPatch(
    (cap_pts[0][0], cap_pts[0][1]-0.03), (cap_pts[2][0], cap_pts[2][1]-0.03),
    connectionstyle="arc3,rad=0.1",
    arrowstyle="<->",
    mutation_scale=10,
    linewidth=2, color='blue'
)
ax.add_patch(arrow)
ax.text(0.28, 0.075, 'width', color='black', fontsize=12)


plt.axis('off')
plt.axis("equal")
plt.tight_layout()
plt.savefig("airfoil_midpoint_nd_arc.svg")

