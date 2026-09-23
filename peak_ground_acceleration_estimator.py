"""Domain logic for the Peak Ground Acceleration Estimator tool."""

import math

import matplotlib

matplotlib.use("Agg")

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


SITE_FACTORS = {
    "Rock (Vs30 > 760 m/s)": 1.0,
    "Stiff soil (360–760 m/s)": 1.2,
    "Soft soil (<360 m/s)": 1.5,
}

FAULT_FACTORS = {
    "Strike-slip": 1.0,
    "Reverse": 1.1,
    "Normal": 0.9,
}

SITE_CHOICES = list(SITE_FACTORS.keys())
FAULT_CHOICES = list(FAULT_FACTORS.keys())

MAGNITUDE_MIN = 3.0
MAGNITUDE_MAX = 9.0
DISTANCE_MIN = 0.1
DISTANCE_MAX = 500.0


def classify_pga(pga_g):
    if pga_g < 0.1:
        return "Weak", "#2e7d32"
    if pga_g < 0.3:
        return "Moderate", "#f9a825"
    if pga_g < 0.6:
        return "Strong", "#ef6c00"
    if pga_g < 1.0:
        return "Very Strong", "#c62828"
    return "Extreme", "#b71c1c"


def _invalid(error):
    return {
        "pga_g": 0.0,
        "pga_cm_s2": 0.0,
        "classification": "Invalid",
        "color": "#666666",
        "error": error,
    }


def estimate_pga(magnitude, distance, site_class, fault_style):
    try:
        m = float(magnitude)
        r = float(distance)
    except (TypeError, ValueError):
        return _invalid("Magnitude and distance must be numeric values.")

    if not (math.isfinite(m) and math.isfinite(r)):
        return _invalid("Magnitude and distance must be finite numbers.")

    if m < MAGNITUDE_MIN or m > MAGNITUDE_MAX:
        return _invalid(
            f"Magnitude must be between {MAGNITUDE_MIN} and {MAGNITUDE_MAX}."
        )

    if r < DISTANCE_MIN or r > DISTANCE_MAX:
        return _invalid(
            f"Distance must be between {DISTANCE_MIN} and {DISTANCE_MAX} km."
        )

    if not isinstance(site_class, str) or site_class not in SITE_FACTORS:
        return _invalid("Please select a valid site soil class.")

    if not isinstance(fault_style, str) or fault_style not in FAULT_FACTORS:
        return _invalid("Please select a valid faulting style.")

    try:
        log10_pga = (
            0.249
            + 0.298 * (m - 6.0)
            - 0.00188 * r
            - 0.00046 * m * r
        )

        if not math.isfinite(log10_pga):
            return _invalid("The attenuation calculation produced an invalid value.")

        pga_cm_s2 = 10.0 ** log10_pga

        if not math.isfinite(pga_cm_s2) or pga_cm_s2 < 0.0:
            return _invalid("The PGA calculation produced an invalid value.")

        pga_cm_s2 *= SITE_FACTORS[site_class]
        pga_cm_s2 *= FAULT_FACTORS[fault_style]
        pga_g = pga_cm_s2 / 980.0

        if not math.isfinite(pga_g) or pga_g < 0.0:
            return _invalid("The final PGA calculation produced an invalid value.")

        classification, color = classify_pga(pga_g)

        return {
            "pga_g": pga_g,
            "pga_cm_s2": pga_cm_s2,
            "classification": classification,
            "color": color,
            "error": None,
        }
    except Exception as exc:
        return _invalid(f"Calculation failed: {exc}")


def make_pga_chart(pga_g, error=None, color=None):
    try:
        value = float(pga_g)
    except (TypeError, ValueError):
        value = 0.0

    if not math.isfinite(value) or value < 0.0:
        value = 0.0

    if color is None:
        color = "#666666" if error else "#1976d2"

    fig = Figure(figsize=(6, 2.5))
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)

    ax.barh([0], [value], color=color, edgecolor="black", height=0.45)

    for threshold in (0.1, 0.3, 0.6, 1.0):
        ax.axvline(threshold, linestyle="--", linewidth=1.0, color="#777777")
        ax.text(
            threshold,
            0.48,
            str(threshold),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#333333",
        )

    upper = max(1.2, value * 1.2)
    ax.set_xlim(0.0, upper)
    ax.set_ylim(-0.6, 0.9)
    ax.set_yticks([0])
    ax.set_yticklabels(["PGA"])
    ax.set_xlabel("Peak Ground Acceleration (g)")
    ax.set_title("PGA Estimate (g)")

    if error:
        chart_error = str(error)
        if len(chart_error) > 80:
            chart_error = chart_error[:77] + "..."
        ax.text(
            0.5,
            0.5,
            chart_error,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=9,
            color="#c62828",
        )

    fig.tight_layout()
    return fig
