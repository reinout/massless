import pathlib
import sys

import matplotlib.pyplot as plt
import pandas as pd
import xmltodict

WORKOUTS_FILE = pathlib.Path("workouts.txt")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
START_YEAR = "2017"  # Before this I only have very limited data.
# ^^^ Note: string comparison... :-)


def workouts_as_xml():
    """Return workouts file as somewhat-OK xml"""
    result = '<?xml version="1.0" encoding="UTF-8"?><wrapper>'
    contents = WORKOUTS_FILE.read_text()
    result += contents.replace(">", " />")
    result += "</wrapper>"
    return result


def _cycling_time(row):
    if row["type"] == "HKWorkoutActivityTypeCycling":
        return row["duration"]


def _walking_time(row):
    if row["type"] == "HKWorkoutActivityTypeWalking":
        return row["duration"]


def main(grouping="month"):
    workouts_data = xmltodict.parse(workouts_as_xml())
    workouts_dictlist = workouts_data["wrapper"]["Workout"]
    workouts_cleaned_dictlist = [
        {
            "date": d["@startDate"],
            "type": d["@workoutActivityType"],
            "duration": float(d["@duration"]),
        }
        for d in workouts_dictlist
        if d["@startDate"] > START_YEAR
    ]
    workouts = pd.DataFrame(workouts_cleaned_dictlist)
    workouts.index = pd.to_datetime(workouts["date"])

    workouts["cycle_time"] = workouts.apply(lambda row: _cycling_time(row), axis=1)
    workouts["walking_time"] = workouts.apply(lambda row: _walking_time(row), axis=1)
    workouts.drop(columns=["date", "type", "duration"], inplace=True)
    workouts_per_day = workouts.resample("D").sum()  # Starts in 2017-03-05

    if grouping == "kwartaal":
        sample_period = "Q"
    else:
        sample_period = "M"

    workouts_per_grouping = workouts_per_day.resample(sample_period).mean()
    ax = workouts_per_grouping.plot(
        kind="bar", stacked=True, ylabel="Gemiddelde duur (min/dag)"
    )

    # Formatting.
    def tick(date):
        if grouping == "kwartaal":
            quarter = int(date.month / 3)
            if quarter == 1:
                return date.strftime(f"Q{quarter} %Y")
            else:
                return f"Q{quarter}"
        elif date.month == 1:
            return date.strftime("%b %Y")
        elif date.year == 2017 and date.month == 3:
            # First column
            return date.strftime("%b %Y")
        elif (date.month % 3) == 1:
            # Only show the quarters.
            return date.strftime("%b")
        else:
            return ""

    # Set all ticks in one go. A bar plot turns dates in to index numbers...
    ax.set_xticklabels([tick(x) for x in workouts_per_grouping.index])

    if grouping == "kwartaal":
        ax.set_xlabel("Kwartalen")
    else:
        ax.set_xlabel("Maanden")

    workouts_per_day["total_time"] = (
        workouts_per_day["cycle_time"] + workouts_per_day["walking_time"]
    )
    total_mean = workouts_per_day["total_time"].mean()
    # workouts_per_day["afwijking"] = workouts_per_day["total_time"] - gemiddelde
    ax.axhline(total_mean)

    plt.show()


if __name__ == "__main__":
    if "kwartaal" in sys.argv:
        main("kwartaal")
    else:
        main()
