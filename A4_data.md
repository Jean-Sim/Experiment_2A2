Nr 1):
v = 342,33 ± 0,40 = 2*L*m
m = 407,537 ± 0,037 Hz
L = 0,42 ± 0,00049 m

(sigma_L/L)^2 = 1.36 * 10^-6
(sigma_m/m)^2 = 8.24 * 10^-9

Nr 2):
v = (342,35 ± 0,48) = 2*L*m
m = (407,556 ± 0,309) Hz
L = 0,42 ± 0,00049 m

(sigma_L/L)^2 = 1.36 * 10^-6
(sigma_m/m)^2 = 5.75 * 10^-7

Nr 3):
v = (339,46 ± 7,23) = 2*f*m 
m = 5.200  +- 0,111 cm. 
f = 3264 +- 2Hz

(sigma_f/f)^2 = 3.75 * 10^-7
(sigma_m/m)^2 = 4.47 * 10^-4

man kann erkennen das der längen messfehler domniert bei 1 und 2, bei drei ist es der steigungs messfehler der auch von dem längen messfehler abhängt.

---------------------------
messung 1 und 2 frequenz korelation sind vernachlässigbar weil unterschiedliche messgeräte verwendet wurden also gilt nur längen korelation
cov(v_1,v_2) = 4*m_1*m_2*sigma_L^2 = 0.15952
messung 2 und drei können wir frequnz korelation auch vernachlkässigen da wir f_3 von messung zwei abgelesen aber neu eingestellt haben
cov(v_i,v_3) = v_i*v_3*sigma_r  |  sigma_r = sigma_hersteller / L
cov(v_1,v_3) = 0.10540
cov(v_2,v_3) = 0.10541

t_ij = |v_i - v_j|/sqrt(sigma_i^2 + sigma_j^2 - 2cov(i,j))
t_12 = 0.0611
t_13 = 0.399
t_23 = 0.401
sind alle verträglich 

gewichteter mittelwert:
<img width="177" height="93" alt="Screenshot 2026-11-20 191137" src="https://github.com/user-attachments/assets/936b269d-e883-4ae9-a8ef-e9e2204ccb3e" />

unsicherheit:
<img width="210" height="97" alt="Screenshot 2026-11-20 191330" src="https://github.com/user-attachments/assets/31184972-5957-4a30-a7e7-c30823d89631" />

ergebniss:
v = 342.33 +- 0.40
das gewichtete mitte hat zu keiner segnifikanten änderung des ergenisses geführt 

der fehler des finalen ergebnisses wird von dem längenfehler dominiert da aufgrund der gewichtung hauptsächlich v_1 und v_2 in das ergebniss eingeflossen sind.
Plot:<img width="1195" height="591" alt="Screenshot 2026-11-20 193930" src="https://github.com/user-attachments/assets/24fbfe3e-43e0-4e16-8e09-e0827bea76c2" />

