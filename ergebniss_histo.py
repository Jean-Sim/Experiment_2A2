import matplotlib.pyplot as plt
import numpy as np

L = 0.42
sigma_L = np.sqrt(0.0004**2 + 0.00029**2)
m = 407.54
sigma_m = 0.037
print("schall geschwindigkeit: ")
v = 2*L*m
print(v)

print("fehler v")
std_v = np.sqrt((2*L*sigma_m)**2 + (2*m*sigma_L)**2)
print(std_v)

def plot_histogram(mittelwert,std,marker_wert,anzahl_datenpunkte = 100000,bins = 100,):
    daten = np.random.normal(loc=mittelwert, scale=std, size=anzahl_datenpunkte)

    plt.figure(figsize=(10, 6))
    plt.hist(daten,bins=bins,density=True,alpha=0.65,color="steelblue",edgecolor="black",label="Verteilung")

    plt.axvline(mittelwert,color="dimgray",linestyle=":",linewidth=2,label=f"experimenteller wert ({mittelwert}) m/s")

    plt.axvline(marker_wert,color="crimson",linestyle="--",linewidth=2.5,label=f"literatur wert ({marker_wert}) m/s")
    plt.title(f"Histogramm (μ = {mittelwert}, σ = {std})", fontsize=14, pad=15)
    plt.xlabel("v/[m/s]", fontsize=12)
    plt.ylabel("Dichte", fontsize=12)
    plt.grid(axis="y", alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()

plot_histogram(round(v,2),std_v,343.42)
print("abstand v")
print((343.42-v)/std_v)
print("sigma L")
print(sigma_L)



