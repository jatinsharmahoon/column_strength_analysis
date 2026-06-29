# Column Buckling Analysis Tool with Tkinter GUI

[cite_start]A Python-based desktop engineering application developed for the Mechanics of Solids framework (ME-211) at NIT Hamirpur[cite: 1317, 1318]. [cite_start]The tool executes stability evaluations for columns under concentric axial loading [cite: 1320, 1330][cite_start], applying three core classical/empirical structural mechanics theories: **Euler's Elastic Buckling**, **Rankine's Empirical Theory**, and **Johnson's Parabolic Formula**[cite: 1332].

[cite_start]The software supports structural variations including circular, hollow circular, and I-section geometries across arbitrary boundary end conditions[cite: 1333, 1394].

---

## Application Architecture

The application is structured into two main decoupled modules following clean software engineering patterns:
1. [cite_start]**Analytical Core (`Column` Class):** Encapsulates geometric calculations (Area, Moment of Inertia, Radius of Gyration) and resolves critical/safe loading limits[cite: 1401, 1414, 1434].
2. [cite_start]**Graphical Interface (`ColumnAnalysisApp` Class):** Drives an interactive Tkinter frame that dynamically reveals structural input spaces depending on the selected cross-section geometry[cite: 1438, 1442].

---

## Governing Engineering Principles

### 1. Slenderness Classification ($\lambda$)
[cite_start]Columns are mathematically classified by their slenderness ratio[cite: 1332, 1352]:

$$\lambda = \frac{L_e}{r}$$

[cite_start]Where $L_e$ is the effective length adjusted by boundary constraint factor $k$ ($L_e = k \cdot L$) [cite: 1353, 1420][cite_start], and $r$ is the minimum radius of gyration ($r = \sqrt{I/A}$)[cite: 1377, 1422]. [cite_start]Classification follows standard operational bounds[cite: 1352]:
* [cite_start]**Short Columns ($\lambda < 32$):** Governed primarily by pure compressive yielding/crushing limits[cite: 1347, 1354].
* [cite_start]**Intermediate Columns ($32 \le \lambda \le 120$):** Subject to transitional buckling profiles[cite: 1355].
* [cite_start]**Long/Slender Columns ($\lambda > 120$):** Extremely susceptible to elastic buckling failure[cite: 1349, 1356].

### 2. Failure Models Solved
* [cite_start]**Euler's Buckling Load ($P_{\text{cr}}$):** Models elastic instability parameters for high slenderness ranges[cite: 1359]:

$$P_{\text{cr}} = \frac{\pi^2 E I}{L_e^2}$$

* **Rankine's Critical Load:** Unifies material crushing and elastic stability bounds for structural transition zones[cite: 1370, 1424]:

$$P_{\text{cr}} = \frac{\sigma_y A}{1 + a \lambda^2}$$

* [cite_start]**Johnson's Parabolic Load:** Empirically tracks short/compact constraints[cite: 1380, 1427]. Valid below critical threshold limits ($C_c = \sqrt{2\pi^2 E / \sigma_y}$); the program dynamically halts calculation if bounds exceed reality to avoid unphysical evaluations.

---

## Verification & Case Validation

[cite_start]The mathematical integrity of this application was benchmarked against classic theoretical problems (e.g., *AMIE Winter 1984 validation loop*)[cite: 1526, 1527]:

### Problem Boundary Conditions
* **Structure:** Hollow Cylindrical Cast Iron Column [cite: 1527]
* [cite_start]**Dimensions:** Length ($L$) = $6\text{ m}$, Outer Diameter = $20\text{ cm}$ ($r_o = 0.1\text{ m}$), Thickness = $25\text{ mm}$ ($r_i = 0.075\text{ m}$) [cite: 1527, 1528]
* [cite_start]**Material Matrix:** Modulus ($E$) = $120\text{ GPa}$, Yield Strength ($\sigma_y$) = $550\text{ MPa}$ [cite: 1526, 1528]
* [cite_start]**Constraints:** Pinned-Pinned boundary ($k = 1.0$), Rankine Constant ($a$) = $1/1600$, Factor of Safety = $4$ [cite: 1526, 1528]

### Software Results Verification Output
[cite_start]Upon triggering execution, the desktop app populates a validated verification solution matrix[cite: 1529]:

| Property Evaluation | Program Computed Value |
| :--- | :---: |
| **Slenderness Ratio ($\lambda$)** | [cite_start]$96.00$ (Intermediate Column) [cite: 1529] |
| **Cross-Sectional Area ($A$)** | [cite_start]$0.0137\text{ m}^2$ [cite: 1529] |
| **Moment of Inertia ($I$)** | [cite_start]$5.3689 \times 10^{-5}\text{ m}^4$ [cite: 1529] |
| **Euler Critical Buckling Load** | [cite_start]$1,766,308.08\text{ N}$ [cite: 1529] |
| **Rankine Critical Crushing Load** | [cite_start]$1,118,262.92\text{ N}$ [cite: 1529] |

---

## Requirements & Execution

### Pre-requisites
[cite_start]Ensure your Python ecosystem possesses `matplotlib` for generating performance plots[cite: 1334, 1397]:
```bash
pip install matplotlib
