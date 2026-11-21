
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

m1 = 407.537
m2 = 407.556
v1 = 342.33
v2 = 342.35
v3 = 339.46
L = 0.42
sigma_L = 0.00049
sigma_hersteller_L = 0.0004

def cor_12(m1,m2,sigma_L):
    return 4*m1*m2*sigma_L**2
def cori3(vi,v3,sigma_L_hersteller, L):
    sigma_r = sigma_L_hersteller/L
    return vi*v3*sigma_r**2

def plot_distributions(pairs):
    fig, ax = plt.subplots(figsize=(12, 6))
    x_min = min(mu - 4*sigma for mu, sigma, name in pairs)
    x_max = max(mu + 4*sigma for mu, sigma, name in pairs)
    x = np.linspace(x_min, x_max, 1000)
    colors = ["blue", "red", "green"]

    for (mu, sigma, name), color in zip(pairs, colors):
        y = norm.pdf(x, loc=mu, scale=sigma)
        ax.plot(x, y, color=color, linewidth=2,label=f"{name}: μ = {mu}, σ = {sigma}")
        ax.fill_between(x, y, color=color, alpha=0.15)
    ax.set_xlabel("v / [m/s]")
    ax.set_ylabel("Wahrscheinlichkeitsdichte")
    ax.set_title("Vergleich der Normalverteilungen")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

ergebnisse = ((342.33 ,0.40, "Ergebniss 1 und 4"),(342.35, 0.48, "Ergebniss 2"),(339.46 ,7.23, "Ergebniss 3"))
plot_distributions(ergebnisse)
