import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from praktikum import cassy
from scipy.optimize import curve_fit

file = "data/messreihe2.labx"

data = cassy.CassyDaten(file)

U = np.array(data.messung(1).datenreihe("U_A1").werte)
f = np.array(data.messung(1).datenreihe("f_B1").werte)

f, U = map(list, zip(*sorted(zip(f, U))))

def plot_resonanzen(U, f):

    U = np.array(U)
    f = np.array(f)

    fits = [(63,  15, 3.54703,  411.519,  49.6783, -1.15706, 0.260),(120, 15, 135.152,  817.862, 392.038, -132.770, 0.903),
        (165,  5, 102.859, 1224.39,  180.673,  -100.471, 0.553),(218, 12, 1.88962, 1633.470,  30.6315,  0.497807, 0.239),
        (257,  5, 0.620912,2041.150,   9.34164, 1.75260, 0.390),(312,  7, 2113.91, 2444.460, 258.966, -2112.010, 0.234),
        (356,  7, 3.42487, 2856.610,   9.60273,-1.57383, 0.171),(405, 11, 1.36890, 3263.770,   5.30674, 0.198474,0.138)]

    def lorentz(f, A, f0, gamma, y0):
        return A * gamma**2 / ((f - f0)**2 + gamma**2) + y0

    fig, ax = plt.subplots(figsize=(12, 6), layout="constrained")
    ax.plot(f, U, "r+", markersize=5, label="Messwerte")

    for n, (index, w, A, f0, gamma, y0, df0) in enumerate(fits):
        f_window = f[index - w:index + w]
        f_fit = np.linspace(f_window.min(), f_window.max(), 300)
        U_fit = lorentz(f_fit, A, f0, gamma, y0)

        ax.plot(f_fit, U_fit,color="tab:orange",linewidth=2,label="Lorentz-Fits" if n == 0 else None,zorder=2)
        U_peak = lorentz(f0, A, f0, gamma, y0)
        ax.errorbar(f0, U_peak,xerr=df0,fmt="o",color="tab:blue",ecolor="tab:blue",markersize=6,elinewidth=1.5,capsize=4,label="Resonanzpeaks" if n == 0 else None,zorder=5)
    ax.set_xlabel(r"Frequenz $f$ / Hz")
    ax.set_ylabel(r"Spannung $U$ / V")
    ax.set_title("Resonanzkurve mit Lorentz-Fits")

    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(f.min(), f.max())

    return fig, ax

fig, ax = plot_resonanzen(U, f)
plt.show()

