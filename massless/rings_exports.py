import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import xmltodict
from matplotlib.dates import YearLocator  # type: ignore

RINGS_FILE = pathlib.Path("var/rings.txt")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
START_YEAR = "2019"
# ^^^ Note: string comparison... :-) Before 2017 I only have very limited
# data. Somewhere in 2019 I got the apple watch, so I started collecting more
# data.


def rings_as_xml():
    """Return rings file as somewhat-OK xml"""
    result = '<?xml version="1.0" encoding="UTF-8"?><wrapper>'
    contents = RINGS_FILE.read_text()
    result += contents
    result += "</wrapper>"
    return result


def _cycling_time(row):
    if row["type"] == "HKWorkoutActivityTypeCycling":
        return row["duration"] / 60


def _walking_time(row):
    if row["type"] == "HKWorkoutActivityTypeWalking":
        return row["duration"] / 60

    # Voorbeeld rianne


def main():
    rings_data = xmltodict.parse(rings_as_xml())
    rings_dictlist = rings_data["wrapper"]["ActivitySummary"]
    rings_cleaned_dictlist = [
        {
            "date": d["@dateComponents"],
            "energy_use": float(d["@activeEnergyBurned"]),
            "active_time": float(d["@appleExerciseTime"]) / 60,
        }
        for d in rings_dictlist
        if d["@dateComponents"] > START_YEAR
    ]
    rings = pd.DataFrame(rings_cleaned_dictlist)
    rings.index = pd.to_datetime(rings["date"])
    rings.drop(columns=["date"], inplace=True)

    sample_period = "M"

    rings_per_month = rings.resample(sample_period).mean()
    # rings_per_month["energy_use_rolling"] = rings_per_month["energy_use"].rolling(4).mean()
    # rings_per_month["active_time_rolling"] = rings_per_month["active_time"].rolling(4).mean()
    rings_per_month["energy_use_rolling"] = (
        rings_per_month["energy_use"].ewm(alpha=0.2).mean()
    )
    rings_per_month["active_time_rolling"] = (
        rings_per_month["active_time"].ewm(alpha=0.2).mean()
    )
    print(rings_per_month)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    x = list(rings_per_month.index)
    y = list(rings_per_month["energy_use"])
    y_rolling = list(rings_per_month["energy_use_rolling"])
    y2 = list(rings_per_month["active_time"])
    y2_rolling = list(rings_per_month["active_time_rolling"])
    ax.plot(x, y, "+", color="orange")
    ax.plot(x, y_rolling, linestyle="solid", color="orange", label="Verbruikte energie")
    ax2.plot(x, y2, "+", color="blue")
    ax2.plot(x, y2_rolling, linestyle="solid", color="blue", label="Actieve tijd")

    ax.set_xlabel("Maanden")
    ax.xaxis.set_major_locator(YearLocator())
    ax.set_ylabel("Gemiddelde verbrande kcal/dag")
    ax2.set_ylabel("Gemiddeld aantal actieve uren/dag")

    # ask matplotlib for the plotted objects and their labels
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)
    ax.grid()
    plt.show()


if __name__ == "__main__":
    main()
