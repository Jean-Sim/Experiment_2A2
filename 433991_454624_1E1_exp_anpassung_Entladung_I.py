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

peaks, props = scipy.signal.find_peaks(U)
#print(peaks)
#print(U[270:])
print([[U[i], f[i],i] for i in peaks if U[i] > 2.3])

n = 405
delta = 11
data_f = np.array(f[n-delta:n+delta])
data_f_error = 1/np.sqrt(3)
data_U = np.array(U[n-delta:n+delta])
data_U_error = (data_U*0.01 + 3*0.005)/np.sqrt(3)
plt.plot(range(len(f)),U,"r+")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy import odr


def lorentz(x, A, x0, gamma, y0):
    return y0 + A * gamma**2 / ((x - x0)**2 + gamma**2)

import numpy as np
import matplotlib.pyplot as plt


def plot_odr_residuen(x, y, xerr, yerr, output):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    xerr = np.broadcast_to(xerr, x.shape)
    yerr = np.broadcast_to(yerr, y.shape)

    popt = output.beta

    # Vom ODR angepasste Positionen
    x_korr = x + output.delta
    y_korr = lorentz(x_korr, *popt)

    # Normierte ODR-Korrekturen
    rx = output.delta / xerr
    ry = output.eps / yerr

    # Gewichteter Gesamtabstand
    d = np.hypot(rx, ry)

    # Vorzeichen durch Lage relativ zur Fitkurve
    vorzeichen = np.sign(y - lorentz(x, *popt))
    r_odr = vorzeichen * d

    # Kontrolle der chi²-Berechnung
    print("chi² aus Residuen:", np.sum(d**2))
    print("chi² aus ODR:", output.sum_square)

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    # Oberer Plot
    x_fit = np.linspace(x.min(), x.max(), 1000)

    ax1.errorbar(
        x, y, xerr=xerr, yerr=yerr,
        fmt="o", capsize=3,
        label="Messdaten"
    )

    ax1.plot(
        x_fit, lorentz(x_fit, *popt),
        "r-", label="Lorentz-ODR"
    )

    # ODR-Korrekturen als Verbindungslinien
    for xi, yi, xki, yki in zip(x, y, x_korr, y_korr):
        ax1.plot(
            [xi, xki], [yi, yki],
            color="green", alpha=0.6, linewidth=1
        )

    ax1.set_ylabel("Spannung [V]")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Unterer Plot: normierter ODR-Abstand
    ax2.plot(x, r_odr, "o")

    ax2.axhline(0, color="red", linestyle="--")

    for level in [-2, -1, 1, 2]:
        ax2.axhline(
            level, color="gray",
            linestyle=":", alpha=0.5
        )

    ax2.set_xlabel("Frequenz [Hz]")
    ax2.set_ylabel("Normierter ODR-Abstand")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    return r_odr



def fit_lorentz_odr(x, y, xerr, yerr, p0=None,show_corrections=False):

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.shape != x.shape or len(x) <= 4:
        raise ValueError("x und y müssen gleich lange 1D-Arrays mit N > 4 sein.")

    xerr = np.broadcast_to(
        np.asarray(xerr, dtype=float), x.shape
    )
    yerr = np.broadcast_to(
        np.asarray(yerr, dtype=float), y.shape
    )

    if (not all(np.all(np.isfinite(v))
                for v in (x, y, xerr, yerr))
            or np.any(xerr <= 0)
            or np.any(yerr <= 0)):
        raise ValueError("Endliche Werte und positive Fehler erforderlich.")

    # Automatische Startparameter
    if p0 is None:
        n = max(1, len(y) // 10)
        y0_guess = np.median(np.r_[y[:n], y[-n:]])
        idx = np.argmax(np.abs(y - y0_guess))

        p0 = [
            y[idx] - y0_guess,
            x[idx],
            (np.max(x) - np.min(x)) / 10,
            y0_guess
        ]

    # ODR-Fit
    model = odr.Model(
        lambda beta, x: lorentz(x, *beta)
    )
    data = odr.RealData(
        x, y, sx=xerr, sy=yerr
    )

    fit = odr.ODR(
        data, model,
        beta0=p0,
        maxit=1000
    )

    output = fit.run()

    if output.info > 4:
        print("Warnung: ODR-Konvergenz prüfen:", output.stopreason)

    popt = output.beta.copy()
    popt[2] = abs(popt[2])

    # Parameterunsicherheiten bei absoluten Messfehlern
    perr = np.sqrt(np.diag(output.cov_beta))

    # ODR-chi²
    chi2 = output.sum_square
    ndof = len(x) - len(popt)
    chi2_red = chi2 / ndof

    # --------------------------------
    # Normierte ODR-Residuen
    # --------------------------------

    delta = output.delta
    eps = output.eps

    # Korrigierte x-Koordinaten
    x_korr = x + delta
    y_korr = lorentz(x_korr, *popt)

    # Normierte x- und y-Abweichungen
    rx = delta / xerr
    ry = eps / yerr

    # Gewichteter ODR-Abstand
    d = np.hypot(rx, ry)

    # Vorzeichen: Messwert oberhalb oder unterhalb der Kurve
    # eps = Fitwert - Messwert
    r_odr = np.sign(-eps) * d

    # Einzelne chi²-Beiträge
    chi2_x = np.sum(rx**2)
    chi2_y = np.sum(ry**2)

    # --------------------------------
    # Ausgabe
    # --------------------------------

    print("\nLorentz-ODR-Fit:")

    for name, value, error in zip(
        ["A", "x0", "gamma", "y0"], popt, perr
    ):
        print(f"{name:6s} = {value:.6g} ± {error:.3g}")

    print(f"FWHM = {2*popt[2]:.6g} ± {2*perr[2]:.3g}")

    print(f"\nchi² x-Anteil = {chi2_x:.4f}")
    print(f"chi² y-Anteil = {chi2_y:.4f}")
    print(f"chi² gesamt  = {chi2:.4f}")
    print(f"ndof         = {ndof}")
    print(f"chi²/ndof    = {chi2_red:.4f}")

    # --------------------------------
    # Plot
    # --------------------------------

    x_fit = np.linspace(x.min(), x.max(), 1000)
    y_fit = lorentz(x_fit, *popt)

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(10, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}
    )

    # Messdaten
    ax1.errorbar(
        x, y,
        xerr=xerr,
        yerr=yerr,
        fmt="o",
        markersize=4,
        capsize=3,
        label="Messdaten"
    )

    # Lorentz-Fit
    ax1.plot(
        x_fit, y_fit,
        "r-",
        label=(
            f"Lorentz-ODR "
            f"($\\chi^2/ndof={chi2_red:.2f}$)"
        )
    )

    # Optional: ODR-Verschiebungen anzeigen
    if show_corrections:
        for xi, yi, xki, yki in zip(
            x, y, x_korr, y_korr
        ):
            ax1.plot(
                [xi, xki], [yi, yki],
                color="green",
                alpha=0.6,
                linewidth=1
            )

    ax1.set_ylabel("Spannung [V]")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Normierte ODR-Residuen
    ax2.plot(
        x, r_odr,
        "o",
        markersize=4,
        label="Normierte ODR-Residuen"
    )

    ax2.axhline(
        0, color="red", linestyle="--"
    )

    # Orientierungslinien
    for level in [-2, -1, 1, 2]:
        ax2.axhline(
            level,
            color="gray",
            linestyle=":",
            alpha=0.4
        )

    ax2.set_xlabel("Frequenz [Hz]")
    ax2.set_ylabel("ODR-Residuen (normiert)")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    return popt, perr, chi2_red, output


#fit_lorentz(data_f,data_U,(data_U*0.01 + 3*0.005)/np.sqrt(3))
fit_lorentz_odr(data_f,data_U,data_f_error,data_U_error)