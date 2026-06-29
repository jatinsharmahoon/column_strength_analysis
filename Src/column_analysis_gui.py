"""
Column Analysis Program (Tkinter GUI version)
-----------------------------------------------
Analyzes columns under concentric axial loading using three classical
buckling theories: Euler's, Rankine's, and Johnson's parabolic formula.
Supports circular, hollow circular, and I-section cross-sections, and
multiple end conditions.

This rebuilds the architecture described in the original MOS-211 project
report (Column class + ColumnAnalysisApp GUI), with full working logic.
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt


class Column:
    """Represents a column and computes its buckling/critical load properties."""

    def __init__(self, length, outer_radius, inner_radius, modulus,
                 yield_strength, end_condition, cross_section,
                 h=None, b=None, t_f=None, t_w=None):
        self.length = length
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.modulus = modulus
        self.yield_strength = yield_strength
        self.end_condition = end_condition
        self.cross_section = cross_section
        self.h = h
        self.b = b
        self.t_f = t_f
        self.t_w = t_w

        self.area = None
        self.I = None
        self.calculate_properties()

    # ------------------------------------------------------------------
    def calculate_properties(self):
        """Computes cross-sectional area and second moment of area (I)."""
        if self.cross_section == "circular":
            r = self.outer_radius
            self.area = math.pi * r ** 2
            self.I = math.pi * r ** 4 / 4

        elif self.cross_section == "hollow_circular":
            r_o, r_i = self.outer_radius, self.inner_radius
            self.area = math.pi * (r_o ** 2 - r_i ** 2)
            self.I = math.pi * (r_o ** 4 - r_i ** 4) / 4

        elif self.cross_section == "i_section":
            h, b, t_f, t_w = self.h, self.b, self.t_f, self.t_w
            self.area = 2 * b * t_f + (h - 2 * t_f) * t_w
            self.I = (b * h ** 3) / 12 - ((b - t_w) * (h - 2 * t_f) ** 3) / 12

        else:
            raise ValueError(f"Unknown cross-section type: {self.cross_section}")

    # ------------------------------------------------------------------
    def get_effective_length_factor(self):
        """Returns the effective length factor (k) for the end condition."""
        factors = {
            "pinned": 1.0,
            "fixed_free": 2.0,
            "fixed": 0.5,
            "fixed_pinned": 1 / math.sqrt(2),
        }
        if self.end_condition not in factors:
            raise ValueError(f"Unknown end condition: {self.end_condition}")
        return factors[self.end_condition]

    def effective_length(self):
        return self.get_effective_length_factor() * self.length

    def radius_of_gyration(self):
        return math.sqrt(self.I / self.area)

    def slenderness_ratio(self):
        return self.effective_length() / self.radius_of_gyration()

    def column_type(self):
        """Classifies the column based on slenderness ratio."""
        lam = self.slenderness_ratio()
        if lam < 32:
            return "Short"
        elif lam <= 120:
            return "Intermediate"
        else:
            return "Long"

    # ------------------------------------------------------------------
    def critical_load_euler(self):
        """Euler's critical buckling load."""
        Le = self.effective_length()
        return (math.pi ** 2) * self.modulus * self.I / (Le ** 2)

    def critical_load_rankine(self, rankine_constant):
        """Rankine's empirical critical load."""
        lam = self.slenderness_ratio()
        return (self.yield_strength * self.area) / (1 + rankine_constant * lam ** 2)

    def critical_load_johnson(self):
        """
        Johnson's parabolic formula for critical stress:
            sigma_cr = sigma_y * [1 - (sigma_y / (4 * pi^2 * E)) * (Le/r)^2]
        Valid only for slenderness ratios below the critical value
        Cc = sqrt(2 * pi^2 * E / sigma_y). Beyond that, Euler's theory
        governs and Johnson's formula is not physically meaningful.
        Returns None (with a flag) if the column is outside Johnson's
        valid range, rather than silently returning a nonsensical number.
        """
        lam = self.slenderness_ratio()
        Cc = math.sqrt(2 * (math.pi ** 2) * self.modulus / self.yield_strength)
        if lam >= Cc:
            return None  # Outside Johnson's valid range; Euler governs instead
        sigma_cr = self.yield_strength * (
            1 - (self.yield_strength / (4 * (math.pi ** 2) * self.modulus)) * (lam ** 2)
        )
        return sigma_cr * self.area

    def johnson_validity_limit(self):
        """Returns the critical slenderness ratio (Cc) above which Johnson's
        formula is not valid for this column."""
        return math.sqrt(2 * (math.pi ** 2) * self.modulus / self.yield_strength)

    # ------------------------------------------------------------------
    def analyze(self, rankine_constant, factor_of_safety):
        """Runs the full analysis and returns a results dictionary."""
        euler = self.critical_load_euler()
        rankine = self.critical_load_rankine(rankine_constant)
        johnson = self.critical_load_johnson()
        lam = self.slenderness_ratio()
        col_type = self.column_type()
        r = self.radius_of_gyration()

        results = {
            "euler_load_N": euler,
            "rankine_load_N": rankine,
            "johnson_load_N": johnson,
            "johnson_valid": johnson is not None,
            "johnson_validity_limit_lambda": self.johnson_validity_limit(),
            "slenderness_ratio": lam,
            "column_type": col_type,
            "area_m2": self.area,
            "moment_of_inertia_m4": self.I,
            "radius_of_gyration_m": r,
            "safe_load_euler_N": euler / factor_of_safety,
            "safe_load_rankine_N": rankine / factor_of_safety,
            "safe_load_johnson_N": (johnson / factor_of_safety) if johnson else None,
        }
        return results


def plot_critical_loads(results, title="Critical Load Comparison for Different Theories"):
    """Plots a bar chart comparing Euler, Rankine, and Johnson critical loads."""
    labels = ["Euler", "Rankine"]
    values = [results["euler_load_N"], results["rankine_load_N"]]
    colors = ["#1f4fd1", "#f2a134"]

    if results["johnson_valid"]:
        labels.append("Johnson")
        values.append(results["johnson_load_N"])
        colors.append("#2e8b40")

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, values, color=colors)
    plt.title(title)
    plt.xlabel("Buckling Theories")
    plt.ylabel("Critical Load (N)")
    plt.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, val, f"{val:,.0f}",
                  ha="center", va="bottom", fontsize=9)
    if not results["johnson_valid"]:
        plt.figtext(0.5, -0.02,
                     f"Note: Johnson's formula not shown \u2014 slenderness ratio "
                     f"({results['slenderness_ratio']:.1f}) exceeds its valid range "
                     f"(\u03BB < {results['johnson_validity_limit_lambda']:.1f}).",
                     ha="center", fontsize=8, color="gray")
    plt.tight_layout()
    plt.savefig("column_theory_comparison.png", dpi=150, bbox_inches="tight")
    plt.show()


# ======================================================================
# GUI Application
# ======================================================================
class ColumnAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Column Analysis Program")
        self.last_results = None
        self.i_section_widgets = []
        self.create_widgets()

    def create_widgets(self):
        labels = ["Length (m)", "Outer Radius (m)", "Inner Radius (m)",
                  "Modulus (Pa)", "Yield Strength (Pa)"]
        self.entries = {}
        row = 0
        for lab in labels:
            tk.Label(self.master, text=lab + ":").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            e = tk.Entry(self.master)
            e.grid(row=row, column=1, padx=5, pady=3)
            self.entries[lab] = e
            row += 1

        tk.Label(self.master, text="End Condition (pinned, fixed, fixed_pinned, fixed_free):").grid(
            row=row, column=0, sticky="e", padx=5, pady=3)
        self.end_condition_var = tk.StringVar(value="pinned")
        tk.Entry(self.master, textvariable=self.end_condition_var).grid(row=row, column=1, padx=5, pady=3)
        row += 1

        tk.Label(self.master, text="Cross-Section (circular, hollow_circular, i_section):").grid(
            row=row, column=0, sticky="e", padx=5, pady=3)
        self.cross_section_var = tk.StringVar(value="circular")
        cb = ttk.Combobox(self.master, textvariable=self.cross_section_var,
                           values=["circular", "hollow_circular", "i_section"], state="readonly")
        cb.grid(row=row, column=1, padx=5, pady=3)
        cb.bind("<<ComboboxSelected>>", self.on_cross_section_change)
        row += 1

        for lab in ["Rankine Constant", "Factor of Safety"]:
            tk.Label(self.master, text=lab + ":").grid(row=row, column=0, sticky="e", padx=5, pady=3)
            e = tk.Entry(self.master)
            e.grid(row=row, column=1, padx=5, pady=3)
            self.entries[lab] = e
            row += 1

        self.i_section_start_row = row
        self.create_i_section_widgets()

        btn_row = self.i_section_start_row + 4
        tk.Button(self.master, text="Analyze", command=self.analyze_column).grid(
            row=btn_row, column=0, pady=10)
        tk.Button(self.master, text="Plot", command=self.plot_column).grid(
            row=btn_row, column=1, pady=10)

    def create_i_section_widgets(self):
        labels = ["I-Section Height (m)", "Flange Width (m)",
                  "Flange Thickness (m)", "Web Thickness (m)"]
        for i, lab in enumerate(labels):
            r = self.i_section_start_row + i
            lbl = tk.Label(self.master, text=lab + ":")
            ent = tk.Entry(self.master)
            lbl.grid(row=r, column=0, sticky="e", padx=5, pady=3)
            ent.grid(row=r, column=1, padx=5, pady=3)
            self.entries[lab] = ent
            self.i_section_widgets.append((lbl, ent))
        self.on_cross_section_change()

    def on_cross_section_change(self, *args):
        show = self.cross_section_var.get() == "i_section"
        for lbl, ent in self.i_section_widgets:
            if show:
                lbl.grid()
                ent.grid()
            else:
                lbl.grid_remove()
                ent.grid_remove()

    @staticmethod
    def get_float_value(value):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid numeric input: '{value}'")

    def analyze_column(self):
        try:
            length = self.get_float_value(self.entries["Length (m)"].get())
            outer_radius = self.get_float_value(self.entries["Outer Radius (m)"].get() or 0)
            inner_radius_str = self.entries["Inner Radius (m)"].get()
            inner_radius = self.get_float_value(inner_radius_str) if inner_radius_str else 0
            modulus = self.get_float_value(self.entries["Modulus (Pa)"].get())
            yield_strength = self.get_float_value(self.entries["Yield Strength (Pa)"].get())
            end_condition = self.end_condition_var.get().strip()
            cross_section = self.cross_section_var.get().strip()
            rankine_constant = self.get_float_value(self.entries["Rankine Constant"].get())
            factor_of_safety = self.get_float_value(self.entries["Factor of Safety"].get())

            kwargs = {}
            if cross_section == "i_section":
                kwargs["h"] = self.get_float_value(self.entries["I-Section Height (m)"].get())
                kwargs["b"] = self.get_float_value(self.entries["Flange Width (m)"].get())
                kwargs["t_f"] = self.get_float_value(self.entries["Flange Thickness (m)"].get())
                kwargs["t_w"] = self.get_float_value(self.entries["Web Thickness (m)"].get())

            self.column = Column(length, outer_radius, inner_radius, modulus,
                                  yield_strength, end_condition, cross_section, **kwargs)
            self.last_results = self.column.analyze(rankine_constant, factor_of_safety)

            r = self.last_results
            johnson_line = (f"Critical Load (Johnson): {r['johnson_load_N']:.2f} N\n"
                             if r["johnson_valid"] else
                             f"Critical Load (Johnson): N/A (\u03BB exceeds valid range, "
                             f"\u03BB < {r['johnson_validity_limit_lambda']:.1f})\n")
            safe_johnson_line = (f"Safe Load (Johnson): {r['safe_load_johnson_N']:.2f} N"
                                  if r["johnson_valid"] else "Safe Load (Johnson): N/A")

            msg = (
                f"Critical Load (Euler): {r['euler_load_N']:.2f} N\n"
                f"Critical Load (Rankine): {r['rankine_load_N']:.2f} N\n"
                f"{johnson_line}"
                f"Slenderness Ratio: {r['slenderness_ratio']:.2f}\n"
                f"Column Type: {r['column_type']}\n"
                f"Area: {r['area_m2']:.4f} m\u00B2\n"
                f"Moment of Inertia: {r['moment_of_inertia_m4']:.6e} m\u2074\n"
                f"Radius of Gyration: {r['radius_of_gyration_m']:.4f} m\n"
                f"Safe Load (Euler): {r['safe_load_euler_N']:.2f} N\n"
                f"Safe Load (Rankine): {r['safe_load_rankine_N']:.2f} N\n"
                f"{safe_johnson_line}"
            )
            messagebox.showinfo("Analysis Result", msg)

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    def plot_column(self):
        if self.last_results is None:
            messagebox.showwarning("No Data", "Please analyze a column first.")
            return
        plot_critical_loads(self.last_results)


if __name__ == "__main__":
    root = tk.Tk()
    app = ColumnAnalysisApp(root)
    root.mainloop()
