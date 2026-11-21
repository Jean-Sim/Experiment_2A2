import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

n_alle = np.arange(1, 9, dtype=int)
f_alle = np.array([411.519, 817.862, 1224.440, 1633.470,2041.150, 2444.47, 2856.610, 3263.770])
sigma_alle = np.array([0.260, 0.903, 0.547, 0.239,0.390, 0.171, 0.171, 0.138])

def gerade(n, a, b):
    return a * n + b
    
n = n_alle
f = f_alle
sigma_f = sigma_alle

(a, b), kovarianz = curve_fit(gerade, n.astype(float), f, sigma=sigma_f, absolute_sigma=True)
sigma_a, sigma_b = np.sqrt(np.diag(kovarianz))

f_fit = gerade(n, a, b)
residuen = f - f_fit
residuen_norm = residuen / sigma_f
chi2 = float(np.sum(residuen_norm ** 2))
ndof = len(n) - 2
chi2_red = chi2 / ndof

print("lineare Regression [gesamt]")
print("f(n) = a*n + b")
print(f"a = ({a} +- {sigma_a}) hz")
print(f"b = ({b} +- {sigma_b}) hz")
print(f"chi2 = {chi2}")
print(f"ndof = {ndof}")
print(f"chi2_red = {chi2_red}")
print("n      f [hz]      Delta f [hz]      delta f / sigma_f")
for ni, fi, r, rn in zip(n, f, residuen, residuen_norm):
    print(f"{ni}   {fi}   {r}       {rn}")

# passen figsize im doc?
plt.figure(figsize=(9, 5), layout="constrained")
plt.errorbar(n, f, yerr=sigma_f, fmt="o", markersize=6, color="tab:blue", ecolor="tab:blue", elinewidth=1.3, capsize=4,label="$f_n$", zorder=3)
n_linie = np.linspace(0.8, 8.2, 350)
plt.plot(n_linie, gerade(n_linie, a, b), color="tab:orange", linewidth=2,label=rf"linearer fit: $f(n)={a:.2f}\,n{b:+.2f}$ Hz")
plt.xlabel("peakordnung $n$")
plt.ylabel("Resonanzfrequenz $f_n$ / Hz")
plt.title("lineare Regression [gesamt]")
plt.xticks(n_alle)
plt.grid(alpha=0.3)
plt.legend(loc="upper left")

plt.figure(figsize=(9, 4), layout="constrained")
plt.errorbar(n, residuen, yerr=sigma_f, fmt="o", markersize=6, color="tab:blue", ecolor="tab:blue", capsize=4,elinewidth=1.3, label=r"$f_n - f_{\mathrm{Fit}}(n)$", zorder=3, )
plt.axhline(0, color="black", linestyle="--", linewidth=1, label="nullinie")
plt.xlabel("peakordnung $n$")
plt.ylabel(r"Residuum $\Delta f$ / Hz")
plt.title("Residuen lineare Regression [gesamt]")
plt.xticks(n_alle)
plt.grid(alpha=0.3)
plt.legend(loc="best")
plt.show()
