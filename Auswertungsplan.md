Messunsicherheiten:

Messunsicherheit Länge (systematisch): ± 0,40 mm
Messunsicherheit Länge (Ablesung): ± 0,29 mm

Bei beiden gehe ich von einer Gleichverteilung aus, siehe Gerätekunde, S. 113.

Messunsicherheit Frequenz CASSY: ± 0,58 Hz

Ich gehe aufgrund der Torzeit von 1 s von einer Gleichverteilung mit einer Breite von 1 Hz aus. Diese Abschätzung ist sehr konservativ, da der Schwingungsgenerator wahrscheinlich Frequenzen erzeugt, die ziemlich nah an der eingestellten Frequenz liegen, und die Streuung entsprechend klein sein sollte. Trotzdem macht diese Annahme für unsere Daten Sinn, da wir mehrere Messpunkte haben, die sich teilweise stark unterscheiden (wahrscheinlich, weil wir die Torzeit nicht richtig eingehalten haben).

Darstellung der Messwerte und Fits:

Ich plane, wie unten illustriert, Messwerte, Anpassungen und gefundene Peaks inklusive ihrer Fehler aufgrund der Seitenbeschränkung so weit wie möglich in einem Plot darzustellen. Die Fit-Informationen mit den gefundenen Werten für die Peaks kommen in eine Tabelle darunter.

<img width="1242" height="696" alt="Unbenannt" src="https://github.com/user-attachments/assets/db68fb69-cbd1-485e-8eef-f11402e96424" />

Ich werde jeweils zwei breite Plots nutzen, um die Residuen der Fits zu zeigen. Da ich ODR verwenden werde, werden die Residuen orthogonal und normiert sein.

Bestimmung der Resonanzfrequenzen:

Wie oben angedeutet, möchte ich Fits verwenden, um die Resonanzfrequenzen (Peaks) zu finden. Ich habe mich für ODR-Fits entschieden, da weder die x- noch die y-Fehler vernachlässigbar sind.

Ich habe vor, eine Lorentz-Funktion in der Nähe des jeweiligen Peaks anzupassen (15–30 Punkte um den Peak). Leider können wir aufgrund der teilweise asymmetrischen Verteilung der Messwerte und der Präsenz von Doppelmessungen den Anpassungsbereich nicht konsistent wählen.

Ein weiteres Problem ist, dass teilweise (\chi^2/\mathrm{ddof}) in Abhängigkeit von der Fensterwahl schwankt. Solange diese Schwankungen klein genug sind, ist das noch okay. Ich werde die Fenster so wählen, dass diese Schwankungen bei benachbarten Fenstern möglichst gering sind.

Bemerkungen:

Was ich jetzt schon weiß, ist, dass die Werte für (\chi^2/\mathrm{ddof}) ungefähr im Bereich von 0,15 bis 1,5 liegen. Etwa drei Fits haben einen Wert von unter 0,3, was nicht gut ist. Das sollten wir aber durch die konservative Wahl des Frequenzfehlers des CASSYs erklären können.

Die ersten beiden Resonanzpeaks haben eine Einbuchtung an der Spitze. Woher diese kommt, weiß ich noch nicht. Der Tutor hat angesprochen, dass der erste Peak manchmal Anomalien aufweist und deshalb ausgeschlossen werden muss. Vielleicht gibt es dafür auch eine physikalische Erklärung.

Lineare Regression:

Bei der linearen Regression werde ich einen normalen Fit und keinen ODR-Fit verwenden, da es keine x-Fehler gibt. Die lineare Regression inklusive der Residuen wird ebenfalls einen eigenen Plot bekommen.

Fehlerrechnung:

Die Fehlerrechnung ist relativ einfach und sollte nicht viel Platz einnehmen. Ich werde noch kurz besprechen, welcher Fehler dominiert. Das Ganze ist aufgrund der einfachen Formel aber nicht allzu kompliziert.

Ergebnisse und Vergleich:

Das Ergebnis für die Schallgeschwindigkeit werde ich inklusive des Fehlers angeben.

Wenn du willst, können wir auch jeweils am Ende der drei Aufgaben unser Ergebnis als Histogramm darstellen und den Literaturwert eintragen.

Ich werde auf jeden Fall in der letzten Aufgabe („Zusammenfassung und Vergleich“) alle drei Ergebnisse als Histogramm in einem Plot darstellen und den gewichteten Mittelwert berechnen (sofern die Ergebnisse dies zulassen).

Anschließend werde ich die Ergebnisse sowohl anhand der relativen Abweichungen als auch mithilfe eines weiteren Histogramms mit dem Literaturwert vergleichen.
