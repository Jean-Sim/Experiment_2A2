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
cov(v_1,v_2) = 4*m_1*m_2*sigma_L = 0.15952
messung 2 und drei können wir frequnz korelation auch vernachlkässigen da wir f_3 von messung zwei abgelesen aber neu eingestellt haben
cov(v_i,v_3) = v_i*v_3*sigma_r  |  sigma_r = sigma_hersteller / L
cov(v_1,v_3) = 0.10540
cov(v_2,v_3) = 0.10541

covarianz matrix:
<img width="436" height="116" alt="Screenshot 2026-11-20 190341" src="https://github.com/user-attachments/assets/7320d42e-e5bd-422f-81de-d2a8e77d53fe" />

Korelationsmatrix:
<img width="334" height="108" alt="Screenshot 2026-11-20 190228" src="https://github.com/user-attachments/assets/ad08d4be-4e24-4f86-b728-b7de6248e5f6" />

t_ij = |v_i - v_j|/(sigma_i^2 + sigma_j^2 - 2cov(i,j))
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
