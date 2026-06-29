# Column Buckling Analysis Tool with Tkinter GUI

A Python-based desktop engineering application developed for the Mechanics of Solids framework (ME-211) at NIT Hamirpur. The tool executes stability evaluations for columns under concentric axial loading, applying three core classical/empirical structural mechanics theories: **Euler's Elastic Buckling**, **Rankine's Empirical Theory**, and **Johnson's Parabolic Formula**.

The software supports structural variations including circular, hollow circular, and I-section geometries across arbitrary boundary end conditions.

---

## Application Architecture

The application is structured into two main decoupled modules following clean software engineering patterns:
1. **Analytical Core (`Column` Class):** Encapsulates geometric calculations (Area, Moment of Inertia, Radius of Gyration) and resolves critical/safe loading limits.
2. **Graphical Interface (`ColumnAnalysisApp` Class):** Drives an interactive Tkinter frame that dynamically reveals structural input spaces depending on the selected cross-section geometry.

---

## Governing Engineering Principles

### 1. Slenderness Classification ($\lambda$)
Columns are mathematically classified by their slenderness ratio:

$$\lambda = \frac{L_e}{r}$$

Where $L_e$ is the effective length adjusted by boundary constraint factor $k$ ($L_e = k \cdot L$) , and $r$ is the minimum radius of gyration ($r = \sqrt{I/A}$). Classification follows standard operational bounds:
* **Short Columns ($\lambda < 32$):** Governed primarily by pure compressive yielding/crushing limits.
* **Intermediate Columns ($32 \le \lambda \le 120$):** Subject to transitional buckling profiles.
* **Long/Slender Columns ($\lambda > 120$):** Extremely susceptible to elastic buckling failure.

### 2. Failure Models Solved
* **Euler's Buckling Load ($P_{\text{cr}}$):** Models elastic instability parameters for high slenderness ranges:

$$P_{\text{cr}} = \frac{\pi^2 E I}{L_e^2}$$

* **Rankine's Critical Load:** Unifies material crushing and elastic stability bounds for structural transition zones:

$$P_{\text{cr}} = \frac{\sigma_y A}{1 + a \lambda^2}$$

* **Johnson's Parabolic Load:** Empirically tracks short/compact constraints. Valid below critical threshold limits ($C_c = \sqrt{2\pi^2 E / \sigma_y}$); the program dynamically halts calculation if bounds exceed reality to avoid unphysical evaluations.

---

## Verification & Case Validation

The mathematical integrity of this application was benchmarked against classic theoretical problems (e.g., *AMIE Winter 1984 validation loop*):

### Problem Boundary Conditions
* **Structure:** Hollow Cylindrical Cast Iron Column
* **Dimensions:** Length ($L$) = $6\text{ m}$, Outer Diameter = $20\text{ cm}$ ($r_o = 0.1\text{ m}$), Thickness = $25\text{ mm}$ ($r_i = 0.075\text{ m}$)
* **Material Matrix:** Modulus ($E$) = $120\text{ GPa}$, Yield Strength ($\sigma_y$) = $550\text{ MPa}$ 
* **Constraints:** Pinned-Pinned boundary ($k = 1.0$), Rankine Constant ($a$) = $1/1600$, Factor of Safety = $4$ 
### Software Results Verification Output
Upon triggering execution, the desktop app populates a validated verification solution matrix:

| Property Evaluation | Program Computed Value |
| :--- | :---: |
| **Slenderness Ratio ($\lambda$)** | $96.00$ (Intermediate Column)  |
| **Cross-Sectional Area ($A$)** | $0.0137\text{ m}^2$  |
| **Moment of Inertia ($I$)** | $5.3689 \times 10^{-5}\text{ m}^4$  |
| **Euler Critical Buckling Load** | $1,766,308.08\text{ N}$ |
| **Rankine Critical Crushing Load** | $1,118,262.92\text{ N}$  |

---

## Requirements & Execution

### Pre-requisites
Ensure your Python ecosystem possesses `matplotlib` for generating performance plots
```bash
pip install matplotlib
