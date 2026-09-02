"""Generate branded README visuals for the HealthConnect project."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "healthconnect_appointment_data.csv"
IMAGE_DIR = ROOT / "images"

DARK = "#0d0d0d"
OFF_WHITE = "#f4f0e8"
GREY = "#a9a7a2"
GOLD = "#c69a4b"
GRID = "#333333"


def finish_chart(fig: plt.Figure, path: Path) -> None:
    """Save a chart with consistent spacing and resolution."""
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def style_axis(ax: plt.Axes) -> None:
    """Apply the Wilson Moses dark visual system to one axis."""
    ax.set_facecolor(DARK)
    ax.tick_params(colors=OFF_WHITE, labelsize=10)
    ax.xaxis.label.set_color(GREY)
    ax.yaxis.label.set_color(GREY)
    ax.title.set_color(OFF_WHITE)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.65)
    ax.set_axisbelow(True)


def create_social_preview() -> None:
    """Create a 1280 × 640 GitHub social-preview card."""
    fig = plt.figure(figsize=(8, 4), dpi=160, facecolor=DARK)
    canvas = fig.add_axes((0, 0, 1, 1))
    canvas.set_axis_off()
    canvas.add_patch(
        plt.Rectangle((0.065, 0.12), 0.008, 0.76, transform=canvas.transAxes, color=GOLD)
    )

    fig.text(0.10, 0.77, "HEALTHCARE ANALYTICS  |  WEEK 4", color=GOLD, fontsize=12, weight="bold")
    fig.text(0.10, 0.58, "HEALTHCONNECT", color=OFF_WHITE, fontsize=29, weight="bold")
    fig.text(0.10, 0.45, "NO-SHOW PREDICTION", color=OFF_WHITE, fontsize=23, weight="bold")
    fig.text(
        0.10,
        0.30,
        "5,000 appointments  •  problem definition  •  responsible AI",
        color=GREY,
        fontsize=10,
    )
    fig.text(0.10, 0.17, "WILSON MOSES  |  DATA SCIENCE × AI ENGINEERING", color=GOLD, fontsize=10)
    fig.text(0.88, 0.48, "WM", color=GOLD, fontsize=38, weight="bold", ha="center")

    fig.savefig(IMAGE_DIR / "social-preview.png", facecolor=DARK)
    plt.close(fig)


def create_outcome_chart(data: pd.DataFrame) -> None:
    """Visualise appointment outcomes in a deliberate display order."""
    order = ["Attended", "No-Show", "Cancelled"]
    counts = data["appointment_outcome"].value_counts().reindex(order)
    rates = counts.div(len(data)).mul(100)

    fig, ax = plt.subplots(figsize=(9, 5), facecolor=DARK)
    bars = ax.bar(order, counts.values, color=[GREY, GOLD, "#686868"], width=0.58)
    style_axis(ax)
    ax.set_title("Appointment outcome distribution", fontsize=17, weight="bold", pad=18)
    ax.set_ylabel("Appointments")
    ax.set_ylim(0, counts.max() * 1.22)

    for bar, count, rate in zip(bars, counts.values, rates.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + counts.max() * 0.03,
            f"{count:,}  ({rate:.2f}%)",
            ha="center",
            color=OFF_WHITE,
            fontsize=10,
            weight="bold",
        )

    finish_chart(fig, IMAGE_DIR / "appointment-outcomes.png")


def create_quality_snapshot(data: pd.DataFrame) -> None:
    """Create a compact card of the verified initial quality findings."""
    appointment_dates = pd.to_datetime(data["appointment_date"], format="%m/%d/%Y")
    age_summary = data.groupby("patient_id")["age"].agg(["min", "max"])
    values = {
        "Exact duplicate rows": int(data.duplicated().sum()),
        "Duplicate appointment IDs": int(data["appointment_id"].duplicated().sum()),
        "Missing distance values": int(data["distance_to_clinic_km"].isna().sum()),
        "Missing waiting-time values": int(data["waiting_time_minutes"].isna().sum()),
        "Sunday appointments": int(appointment_dates.dt.dayofweek.eq(6).sum()),
        "Patient IDs with age span > 2 years": int(((age_summary["max"] - age_summary["min"]) > 2).sum()),
    }

    fig = plt.figure(figsize=(10, 5.6), facecolor=DARK)
    canvas = fig.add_axes((0, 0, 1, 1))
    canvas.set_axis_off()
    fig.text(0.08, 0.86, "Initial data-quality snapshot", color=OFF_WHITE, fontsize=20, weight="bold")
    fig.text(0.08, 0.80, "Verified observations from the 5,000-record source dataset", color=GREY, fontsize=10)

    positions = [(0.08, 0.60), (0.54, 0.60), (0.08, 0.37), (0.54, 0.37), (0.08, 0.14), (0.54, 0.14)]
    for (label, value), (x, y) in zip(values.items(), positions):
        canvas.add_patch(
            plt.Rectangle((x, y), 0.38, 0.16, transform=canvas.transAxes, facecolor="#171717", edgecolor="#333333")
        )
        fig.text(x + 0.025, y + 0.095, f"{value:,}", color=GOLD, fontsize=21, weight="bold")
        fig.text(x + 0.025, y + 0.045, label, color=OFF_WHITE, fontsize=9)

    fig.savefig(IMAGE_DIR / "initial-data-quality.png", dpi=160, facecolor=DARK)
    plt.close(fig)


def main() -> None:
    """Generate all HealthConnect README assets."""
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(DATA_PATH, keep_default_na=False)
    for column in ["distance_to_clinic_km", "waiting_time_minutes"]:
        data[column] = pd.to_numeric(data[column].replace("", pd.NA), errors="coerce")
    create_social_preview()
    create_outcome_chart(data)
    create_quality_snapshot(data)


if __name__ == "__main__":
    main()
