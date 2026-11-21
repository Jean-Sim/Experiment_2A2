import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from praktikum import cassy
from scipy.optimize import curve_fit
from scipy import odr

file = "data/messreihe2.labx"

data = cassy.CassyDaten(file)

U = np.array(data.messung(1).datenreihe("U_A1").werte)
f = np.array(data.messung(1).datenreihe("f_B1").werte)

f, U = map(list, zip(*sorted(zip(f, U))))

peaks, props = scipy.signal.find_peaks(U)
#print(peaks)
#print(U[270:])
#print([[U[i], f[i],i] for i in peaks if U[i] > 2.3])

n = 165
delta = 5
data_f = np.array(f[n-delta:n+delta])
data_f_error = 1/np.sqrt(3)
data_U = np.array(U[n-delta:n+delta])
data_U_error = (data_U*0.01 + 3*0.005)/np.sqrt(3)
plt.plot(range(len(f)),U,"r+")
plt.show()


def lorentz(x, A, x0, gamma, y0):
    return y0 + A * gamma**2 / ((x - x0)**2 + gamma**2)

def plot_odr_residuen(x, y, x_err, y_err, output):
    x = np.array(x)
    y = np.array(y)

    x_err = np.broadcast_to(x_err, x.shape)
    y_err = np.broadcast_to(y_err, y.shape)

    popt = output.beta

    x_korr = x + output.delta
    y_korr = lorentz(x_korr, *popt)
    rx = output.delta / x_err
    ry = output.eps / y_err
    d = np.hypot(rx, ry)

    pari = np.sign(y - lorentz(x, *popt))
    r_odr = pari * d

    #print("chi residuen:", np.sum(d**2))
    #print("chi odr", output.sum_square)
    fig, (ax1, ax2) = plt.subplots(2, 1,gridspec_kw={"height_ratios": [3, 1]} )
    x_fit = np.linspace(x.min(), x.max(), 1000)

    ax1.errorbar(x, y, xerr=x_err, yerr=y_err,fmt="o",label="daten")

    ax1.plot(x_fit, lorentz(x_fit, *popt),"r-", label="odr")

    for xi, yi, xki, yki in zip(x, y, x_korr, y_korr):
        ax1.plot([xi, xki], [yi, yki], alpha=0.6, linewidth=1)

    ax1.set_ylabel("spanug")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(x, r_odr, "o")
    ax2.axhline(0, color="red", linestyle="--")

    for level in [-2, -1, 1, 2]:
        ax2.axhline(level, color="gray",linestyle=":", alpha=0.3)

    ax2.set_xlabel("frequenz")
    ax2.set_ylabel("normierter abstand")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    return r_odr



def fit_lorentz_odr(x, y, xerr, yerr, p0=None):

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    #if x.ndim != 1 or y.shape != x.shape or len(x) <= 4:
    #    raise ValueError("datenfehlen oder falsche form")

    xerr = np.broadcast_to(np.array(xerr), x.shape)
    yerr = np.broadcast_to(np.array(yerr), y.shape)

    n = max(1, len(y) // 10)#/10)
    y0_guess = np.median(np.r_[y[:n], y[-n:]])
    idx = np.argmax(np.abs(y - y0_guess))

    p0 = [y[idx] - y0_guess,x[idx],(np.max(x) - np.min(x)) / 10,y0_guess]
    model = odr.Model(lambda beta, x: lorentz(x, *beta))
    data = odr.RealData(x, y, sx=xerr, sy=yerr)
    fit = odr.ODR(data, model,beta0=p0,maxit=1000)
    output = fit.run()

    popt = output.beta.copy()
    popt[2] = abs(popt[2])

    perr = np.sqrt(np.diag(output.cov_beta))
    chi2 = output.sum_square
    ndof = len(x) - len(popt)
    chi2_red = chi2 / ndof

    delta = output.delta
    eps = output.eps

    x_korr = x + delta
    y_korr = lorentz(x_korr, *popt)

    rx = delta / xerr
    ry = eps / yerr
    d = np.hypot(rx, ry)
    r_odr = np.sign(-eps) * d

    chi2_x = np.sum(rx**2)
    chi2_y = np.sum(ry**2)

    print("lorentzodr")

    for name, value, error in zip(["A", "x0", "gamma", "y0"], popt, perr):
        print(f"{name} = {value} +- {error}")

    print(f"FWHM = {2*popt[2]} +- {2*perr[2]}")

    print(f"chi2 x = {chi2_x}")
    print(f"chi2 y = {chi2_y}")
    print(f"chi2 gesamt  = {chi2}")
    print(f"ddof         = {ndof}")
    print(f"chi2/ndof    = {chi2_red}")

    x_fit = np.linspace(x.min(), x.max(), 1000)
    y_fit = lorentz(x_fit, *popt)

    fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(10, 7),sharex=True,gridspec_kw={"height_ratios": [3, 1]})

    ax1.errorbar(x, y,xerr=xerr,yerr=yerr,fmt="o",markersize=4,capsize=3,label="messdaten")
    ax1.plot(x_fit, y_fit, "r-",label=(f"lorentz odr  "f"($chi2/ndof={chi2_red}$)"))

    #for xi, yi, xki, yki in zip(x, y, x_korr, y_korr):
        #ax1.plot([xi, xki], [yi, yki],color="green",alpha=0.6,linewidth=1)
    ax1.set_ylabel("spannung")
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax2.plot(x, r_odr,"o",markersize=4,label="normierte residuen")

    ax2.axhline(0, color="red", linestyle="--")

    #for x in [-2, -1, 1, 2]:
    ax2.set_xlabel("frequenz")
    ax2.set_ylabel("odr residuen (norm)")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    return popt, perr, chi2_red, output


#fit_lorentz(data_f,data_U,(data_U*0.01 + 3*0.005)/np.sqrt(3))
fit_lorentz_odr(data_f,data_U,data_f_error,data_U_error)
