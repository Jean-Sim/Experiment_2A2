import warnings

import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
from praktikum import cassy

windows = [(63, 15), (120, 15), (165, 5), (218, 12),(257, 5), (312, 7), (356, 7), (405, 11),]

start_vaues = [(3.54703, 411.519, 49.6783, -1.15706),(135.152, 817.862, 392.038, -132.770),(102.859, 1224.39, 180.673, -100.471),
    (1.88962, 1633.470, 30.6315, 0.497807), (0.620912, 2041.150, 9.34164, 1.75260),(2113.91, 2444.460, 258.966, -2112.010),
    (3.42487, 2856.610, 9.60273, -1.57383),(1.36890, 3263.770, 5.30674, 0.198474),]

file = "data/messreihe2.labx"

data = cassy.CassyDaten(file)

U = np.array(data.messung(1).datenreihe("U_A1").werte)
f = np.array(data.messung(1).datenreihe("f_B1").werte)

f, U = map(list, zip(*sorted(zip(f, U))))
f = np.array(f)
U = np.array(U)

def lorentz(f, A, f0, gamma, y0):
    return y0 + A * gamma**2 / ((f - f0)**2 + gamma**2)

def berechne_residuen(f, U):
    modell = odr.Model(lambda beta, x: lorentz(x, *beta))
    ergebnisse = []

    for nummer, ((n, halbbreite), startwerte) in enumerate(zip(windows, start_vaues), start=1): #zip(windows, start_vaues):
        sl = slice(n - halbbreite, n + halbbreite)
        x = f[sl]
        y = U[sl]

        xerr = np.full_like(x, 1 / np.sqrt(3), dtype=float)
        yerr = np.abs((0.01 * y + 3 * 0.005) / np.sqrt(3))

        daten = odr.RealData(x, y, sx=xerr, sy=yerr)
        anpassung = odr.ODR(daten, modell, beta0=startwerte, maxit=1000)
        output = anpassung.run()

        rx = output.delta / xerr
        ry = output.eps / yerr
        d = np.hypot(rx, ry)
        residuen = np.sign(-output.eps) * d
        chi2_aus_residuen = float(np.sum(d**2))

        chi2_red = float(output.sum_square / (len(x) - 4))

        ergebnisse.append((nummer, x.copy(), residuen, output.beta[1], chi2_red))
        print(f"Fit {nummer}: f0 = {output.beta[1]:.2f} Hz, "f"chi2/ndof = {chi2_red:.2f}")
    return ergebnisse

# ein plot is zu un übersichlich und 6 würden im doc zuviel platz brauchen imo
def plotte_residuen(ergebnisse):
    fig, achsen = plt.subplots(2, 1, figsize=(6, 8),  layout="constrained")
    farben = plt.get_cmap("tab10").colors

    for achse, gruppe in zip(achsen, (ergebnisse[:4], ergebnisse[4:])):
        for nummer, x, residuen, f0, chi2_red in gruppe:
            achse.plot(x, residuen, linestyle="none", marker="o", markersize=5,color=farben[nummer - 1],label=rf"Fit {nummer}",)
        achse.axhline(0, color="black", linestyle="--", linewidth=1)
        for niveau in (-2, -1, 1, 2):
            achse.axhline(niveau, color="gray", linestyle=":", alpha=0.50)
        achse.set_title(f"Normierte ODR-Residuen: Fits {gruppe[0][0]}–{gruppe[-1][0]}")
        achse.set_xlabel(r"Frequenz $f$ / Hz")
        achse.set_ylabel("Normierter ODR-Abstand")
        achse.grid(alpha=0.3)
        achse.legend(fontsize=8)
    return fig, achsen

ergebnisse = berechne_residuen(f, U)
plotte_residuen(ergebnisse)
plt.show()