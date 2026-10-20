# Digital Circuits Repository

> **Interaktive Logikschaltungen für Lehre, Übungen und Probeklausuren**  
> Fachbereich Elektrotechnik und Informationstechnik / Informatik  
> Hochschule Hamm-Lippstadt (HSHL) — Prof. Dr. Robin Nunkesser  
> Simulator: [Digital von H.Neemann (GitHub)](https://github.com/hneemann/Digital)

---

## 🚀 Schnellstart

1. **Digital herunterladen:**  
   Laden Sie die aktuelle Version von *Digital* (z. B. `Digital.zip`) unter [github.com/hneemann/Digital/releases](https://github.com/hneemann/Digital/releases) herunter und entpacken Sie das Archiv. *(Java 11 oder neuer erforderlich)*.
2. **Schaltung herunterladen:**  
   Klicken Sie in den untenstehenden Tabellen auf den gewünschten Dateinamen (`.dig`), um die Schaltung direkt herunterzuladen.
3. **In Digital öffnen:**  
   Starten Sie `Digital.jar` und öffnen Sie die heruntergeladene `.dig`-Datei (`Datei -> Öffnen`). Sie können die Eingänge per Klick interaktiv schalten, Taktzyklen durchlaufen und Signallaufzeiten beobachten.

---

## 📂 Struktur des Repositories

```text
digital-circuits/
├── 01_grundgatter/             # Elementare Logikgatter (AND, OR, NOT, NAND, NOR, XOR, XNOR)
├── 02_boolesche_algebra/        # Schaltungssynthese, Teilschritte und Auswertung
├── 03_schaltnetze/              # Addierer, Multiplexer, Demultiplexer, Prioritätsencoder
├── 04_hazards/                  # Zeitverhalten, Statische/Dynamische Hazards, Glitches
├── 05_schaltwerke/              # Speicherglieder, Latches, Flipflops, Register, Zähler, Automaten
├── 06_uebungen_probeklausuren/  # Schaltungen aus den Übungsaufgaben und Probeklausuren
└── scripts/                     # Hilfsskripte (Headless-Export nach SVG, Synchronisation)
```

---

## 📑 Schaltungsübersicht

### 1. Elementare Grundgatter (`01_grundgatter/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`Algebra_Overview.dig`](01_grundgatter/Algebra_Overview.dig) | Übersicht der drei Grundoperationen (AND, OR, NOT) | Vorlesung: Kapitel 4 & 5 |
| [`Simple_TT_AND.dig`](01_grundgatter/Simple_TT_AND.dig) | 2-Eingang UND-Gatter mit Eingabeschaltern und LED | Vorlesung: Kapitel 4 |
| [`Simple_TT_OR.dig`](01_grundgatter/Simple_TT_OR.dig) | 2-Eingang ODER-Gatter mit Eingabeschaltern | Vorlesung: Kapitel 4 |
| [`Simple_TT_NOT.dig`](01_grundgatter/Simple_TT_NOT.dig) | Inverter (NOT-Gatter) | Vorlesung: Kapitel 4 |
| [`Simple_TT_AND_FanIn3.dig`](01_grundgatter/Simple_TT_AND_FanIn3.dig) | UND-Gatter mit 3 Eingängen (Fan-In 3) | Vorlesung: Kapitel 4 |
| [`Simple_TT_OR_FanIn3.dig`](01_grundgatter/Simple_TT_OR_FanIn3.dig) | ODER-Gatter mit 3 Eingängen (Fan-In 3) | Vorlesung: Kapitel 4 |
| [`Simple_TT_NAND_FanIn3.dig`](01_grundgatter/Simple_TT_NAND_FanIn3.dig) | NAND-Gatter mit 3 Eingängen | Vorlesung: Kapitel 4 |
| [`Simple_TT_NOR_FanIn3.dig`](01_grundgatter/Simple_TT_NOR_FanIn3.dig) | NOR-Gatter mit 3 Eingängen | Vorlesung: Kapitel 4 |
| [`Simple_TT_XOR_FanIn3.dig`](01_grundgatter/Simple_TT_XOR_FanIn3.dig) | XOR-Gatter mit 3 Eingängen (Ungerade Parität) | Vorlesung: Kapitel 4 |
| [`Simple_TT_XNOR_FanIn3.dig`](01_grundgatter/Simple_TT_XNOR_FanIn3.dig) | XNOR-Gatter mit 3 Eingängen | Vorlesung: Kapitel 4 |
| [`Simple_TT_XOR_FanIn3_with2.dig`](01_grundgatter/Simple_TT_XOR_FanIn3_with2.dig) | Kaskadiertes 3-Eingang XOR aus zwei 2-Eingang XOR-Gattern | Vorlesung: Kapitel 4 |
| [`ti2_nand.dig`](01_grundgatter/ti2_nand.dig) | 2-Eingang NAND-Gatter (Funktionelle Vollständigkeit) | Vorlesung: Kapitel 5 |
| [`SimpleAND.dig`](01_grundgatter/SimpleAND.dig) | Grundlegendes UND-Gatter | Vorlesung: Kapitel 5 |
| [`TruthTableAND.dig`](01_grundgatter/TruthTableAND.dig) | Wahrheitstabelle des UND-Gatters | Vorlesung: Kapitel 4 |
| [`switches_and.dig`](01_grundgatter/switches_and.dig) | Schaltermodell: Reihenschaltung (Konjunktion) | Vorlesung: Kapitel 4 |
| [`switches_or.dig`](01_grundgatter/switches_or.dig) | Schaltermodell: Parallelschaltung (Disjunktion) | Vorlesung: Kapitel 4 |

---

### 2. Boolesche Algebra & Schaltungssynthese (`02_boolesche_algebra/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`AusdruckSchaltnetz.dig`](02_boolesche_algebra/AusdruckSchaltnetz.dig) | Vollständiges Schaltnetz für $y = (x_0 \wedge \neg x_1) \vee (x_2 \wedge x_3)$ | Vorlesung: Kapitel 4 |
| [`AusdruckSchaltnetz_Step1.dig`](02_boolesche_algebra/AusdruckSchaltnetz_Step1.dig) | Syntheseschritt 1: Eingangsbeschaltung | Vorlesung: Kapitel 4 |
| [`AusdruckSchaltnetz_Step2.dig`](02_boolesche_algebra/AusdruckSchaltnetz_Step2.dig) | Syntheseschritt 2: Invertierung $\neg x_1$ | Vorlesung: Kapitel 4 |
| [`AusdruckSchaltnetz_Step3.dig`](02_boolesche_algebra/AusdruckSchaltnetz_Step3.dig) | Syntheseschritt 3: Erste Konjunktion $x_0 \wedge \neg x_1$ | Vorlesung: Kapitel 4 |
| [`AusdruckSchaltnetz_Step4.dig`](02_boolesche_algebra/AusdruckSchaltnetz_Step4.dig) | Syntheseschritt 4: Zweite Konjunktion $x_2 \wedge x_3$ | Vorlesung: Kapitel 4 |
| [`AusdruckSchaltnetz_Step5.dig`](02_boolesche_algebra/AusdruckSchaltnetz_Step5.dig) | Syntheseschritt 5: Abschließende Disjunktion am Ausgang | Vorlesung: Kapitel 4 |

---

### 3. Kombinatorische Schaltnetze (`03_schaltnetze/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`Halbaddierer.dig`](03_schaltnetze/Halbaddierer.dig) | 1-Bit Halbaddierer (Summe via XOR, Carry via AND) | Vorlesung: Kapitel 5 |
| [`Volladdierer.dig`](03_schaltnetze/Volladdierer.dig) | 1-Bit Volladdierer mit Carry-In und Carry-Out | Vorlesung: Kapitel 5 |
| [`VierBitAddierer.dig`](03_schaltnetze/VierBitAddierer.dig) | 4-Bit Ripple-Carry-Addierer aus kaskadierten Volladdierern | Vorlesung: Kapitel 5 |
| [`Multiplexer.dig`](03_schaltnetze/Multiplexer.dig) | 4-zu-1 Multiplexer (Gatterebene) | Vorlesung: Kapitel 5 |
| [`Demultiplexer.dig`](03_schaltnetze/Demultiplexer.dig) | 1-zu-4 Demultiplexer mit Freigabesignal | Vorlesung: Kapitel 5 |
| [`priorityencoder.dig`](03_schaltnetze/priorityencoder.dig) | Prioritäts-Encoder (Priorisierung paralleler Anforderungen) | Vorlesung: Kapitel 5 |
| [`TI2_halbaddierer.dig`](03_schaltnetze/TI2_halbaddierer.dig) | Didaktische Variante des Halbaddierers | Vorlesung: Kapitel 5 |
| [`TI2_volladdierer.dig`](03_schaltnetze/TI2_volladdierer.dig) | Didaktische Variante des Volladdierers | Vorlesung: Kapitel 5 |
| [`ti2_mux.dig`](03_schaltnetze/ti2_mux.dig) | Multiplexer-Variante | Vorlesung: Kapitel 5 |

---

### 4. Zeitverhalten & Hazards (`04_hazards/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`hazard.dig`](04_hazards/hazard.dig) | Grundschaltung zur Demonstration von Laufzeitunterschieden | Vorlesung: Kapitel 5 |
| [`hazard_tt.dig`](04_hazards/hazard_tt.dig) | Statischer 1-Hazard: Schaltung mit Glitch bei Übergang $x_2: 1 \to 0$ | Vorlesung: Kapitel 5 |
| [`hazard_tt_repariert.dig`](04_hazards/hazard_tt_repariert.dig) | Hazard-freies Netz durch Hinzufügen des Konsensus-Terms | Vorlesung: Kapitel 5 |
| [`LogikHazard.dig`](04_hazards/LogikHazard.dig) | Demonstrator für statischen Logikhazard mit Verzögerungsglied | Vorlesung: Kapitel 5 |
| [`logikhazard_signal.dig`](04_hazards/logikhazard_signal.dig) | Signalverlauf mit Glitch-Erzeugung | Vorlesung: Kapitel 5 |
| [`logikhazard_signal2.dig`](04_hazards/logikhazard_signal2.dig) | Zweite Signalkonfiguration zur Hazard-Analyse | Vorlesung: Kapitel 5 |
| [`logikhazard_signal_repariert.dig`](04_hazards/logikhazard_signal_repariert.dig) | Reparierter Signalpfad ohne Störimpuls | Vorlesung: Kapitel 5 |
| [`dynhazard.dig`](04_hazards/dynhazard.dig) | Dynamischer Hazard: Schaltung mit Dreifach-Übergang $0 \to 1 \to 0 \to 1$ | Vorlesung: Kapitel 5 |
| [`funktionshazard_loesung.dig`](04_hazards/funktionshazard_loesung.dig) | Funktionshazard-Analyse bei simultaner Änderung zweier Eingänge | Vorlesung: Kapitel 5 |

---

### 5. Sequentielle Schaltwerke & Speicher (`05_schaltwerke/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`RS_Latch.dig`](05_schaltwerke/RS_Latch.dig) | Asynchrones RS-Flipflop (Rückgekoppelte NOR-Gatter) | Vorlesung: Kapitel 5 & 9 |
| [`RS_Latch_Getaktet.dig`](05_schaltwerke/RS_Latch_Getaktet.dig) | Taktzustandsgesteuertes RS-Latch | Vorlesung: Kapitel 5 & 9 |
| [`D_Latch.dig`](05_schaltwerke/D_Latch.dig) | Taktgesteuertes D-Latch (Transparent Latch) | Vorlesung: Kapitel 5 & 9 |
| [`Register4Bit.dig`](05_schaltwerke/Register4Bit.dig) | 4-Bit-Datenregister mit gemeinsamen Takteingang | Vorlesung: Kapitel 9 |
| [`Binaerzaehler.dig`](05_schaltwerke/Binaerzaehler.dig) | Asynchroner/Synchroner 4-Bit Binärzähler | Vorlesung: Kapitel 9 |
| [`MooreAutomat.dig`](05_schaltwerke/MooreAutomat.dig) | Endlicher Automat (FSM) nach Moore mit Zustandsspeicher | Vorlesung: Kapitel 5 & 8 |
| [`Sample_and_hold.dig`](05_schaltwerke/Sample_and_hold.dig) | Sample-and-Hold Abtast- und Halteglied | Vorlesung: Kapitel 5 |

---

### 6. Übungsaufgaben & Probeklausuren (`06_uebungen_probeklausuren/`)

| Schaltung (`.dig`) | Beschreibung | Herkunft / Verwendung |
| :--- | :--- | :--- |
| [`Digital_Counter_Combinatorics.dig`](06_uebungen_probeklausuren/Digital_Counter_Combinatorics.dig) | 3-Bit-Synchronzähler: Kombinatorisches Schaltnetz der Folgezustände | Übungsblatt 9 / TI-Übung |
| [`Digital_Counter_Sequential.dig`](06_uebungen_probeklausuren/Digital_Counter_Sequential.dig) | Vollständiger 3-Bit-Synchronzähler mit D-Flipflops und Taktgeber | Übungsblatt 9 / TI-Übung |
| [`Digital_Multiplexer.dig`](06_uebungen_probeklausuren/Digital_Multiplexer.dig) | 4-zu-1 Multiplexer zur Funktionsanalyse und Wahrheitstabellen-Bestimmung | Übungsblatt 4 / Probeklausur Teil 1 |
| [`Digital_TruthTable_01.dig`](06_uebungen_probeklausuren/Digital_TruthTable_01.dig) | Schaltnetz-Analyse 01: Ermittlung der Wahrheitstabelle ($n=3$ Eingänge) | Übungsblatt 4 / Probeklausur Teil 1 |
| [`Digital_TruthTable_02.dig`](06_uebungen_probeklausuren/Digital_TruthTable_02.dig) | Schaltnetz-Analyse 02: Alternative Schaltungsvariante | Übungsblatt 4 / Aufgabenpool |
| [`Digital_TruthTable_03.dig`](06_uebungen_probeklausuren/Digital_TruthTable_03.dig) | Schaltnetz-Analyse 03: Alternative Schaltungsvariante | Übungsblatt 4 / Aufgabenpool |

---

## 🛠️ Lizenz & Verwendung

Diese Schaltungen wurden für Lehrveranstaltungen an der Hochschule Hamm-Lippstadt erstellt.  
Verwendung für Studium, Lehre und akademische Weiterbildung frei.
