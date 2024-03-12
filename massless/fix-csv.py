import datetime
import pathlib
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import typer
from matplotlib.dates import (
    MonthLocator,  # type: ignore
    YearLocator,  # type: ignore
    date2num,  # type: ignore
)

INPUT = "var/hackdiet_db.csv"
EMA_FACTOR = 0.1  # Exponential moving average.
LENGTH = 1.78
TODAY = datetime.date.today()


class Start(str, Enum):
    all = "all"
    high = "high"
    begin = "begin"


# START is the start date of the period
START_DATE = {
    Start.all: datetime.date(1972, 12, 25),
    Start.high: datetime.date(2021, 5, 28),
    Start.begin: datetime.date(2022, 11, 1),  # TODO: nakijken
}
# TARGET is the initial goal: the bottom of the graph.
TARGET = {
    Start.all: 88.0,
    Start.high: 88.0,
    Start.begin: 88.0,
}
# MAX is the top of the graph.
# Max value is 112.3 on 2021-05-28
MAX = {
    Start.all: 113.0,
    Start.high: 113.0,
    Start.begin: 108.0,
}
# Starting value for the exponential moving average.
FIRST_EMA = {
    Start.all: 97.5,
    Start.high: 112.3,
    Start.begin: 107.5,
}


START_2KG = datetime.date(2007, 12, 21)
END_2KG = datetime.date(2008, 9, 19)

# Weird bumb smoothing
RESTART_IN_2019 = datetime.date(2019, 3, 1)
RESTART_IN_2019_EMA = 106.0


def dates_and_values(period):
    input_file = pathlib.Path(INPUT)
    content = input_file.read_text()
    lines = content.split("\n")
    lines = lines[4:]  # Zap metadata lines at the top
    lines = [line for line in lines if line.startswith("2")]
    start_date = START_DATE[period]
    for line in lines:
        parts = line.split(",")
        date = datetime.date.fromisoformat(parts[0])
        if date > TODAY:
            # Strip off empty future dates in the last month.
            return
        if date < start_date:
            # Don't start yet.
            continue
        value = parts[1].strip()
        if not value:
            continue
        value = float(value)
        if START_2KG < date < END_2KG:
            # For 3/4 year I thought a new scale was defective and I
            # subtracted 2kg from the values. I'm adding them again here :-)
            value += 2
        yield date, value


def mass_to_bmi(mass):
    return mass / (LENGTH**2)


def main(period: Start = Start.begin):
    """Generate graph from a hacker's diet csv export.

    As the period you can pass:
    - 'all' for the whole hog since 2007.
    - 'high' starts at the high point of 112.3kg.
    - 'begin' for the start of the current diet in november 2022.

    """
    previous_ema = FIRST_EMA[period]

    dates = []
    values = []
    emas = []
    for date, value in dates_and_values(period):
        if date == RESTART_IN_2019:
            # Smoothen out a weird bump in the graph.
            previous_ema = RESTART_IN_2019_EMA
        dates.append(date)
        values.append(value)
        ema = value * EMA_FACTOR + previous_ema * (1 - EMA_FACTOR)
        emas.append(ema)
        previous_ema = ema

    # Set up the axis
    fig, ax1 = plt.subplots()
    ax2: plt.Axes = ax1.twinx()  # type: ignore
    minimum = TARGET[period]
    maximum = MAX[period]
    ax1.set_ylim(minimum, maximum)
    ax2.set_ylim(mass_to_bmi(minimum), mass_to_bmi(maximum))

    # Add data
    x = np.array(dates)
    ax1.plot(x, np.array(values), "+", color="orange", label="gewicht")
    ax1.plot(x, np.array(emas))

    # Add trend of last 30 days
    dates_as_ints = date2num(dates)
    x30 = np.array(dates_as_ints[-30:])
    y30 = np.array(values[-30:])
    trend = np.polyfit(x30, y30, 1)
    trend_line = np.poly1d(trend)
    # And plot the trend line, but extend it 30 more days.
    x30_plus_month = np.array(list(dates_as_ints[-30:]) + [dates_as_ints[-1] + 30])
    ax1.plot(x30_plus_month, trend_line(x30_plus_month), ":", color="green")

    # Layout
    ax1.set_xlabel("Datum")
    ax1.set_ylabel("Gewicht (kg)")
    ax2.set_ylabel("BMI")
    ax1.grid(True)
    if period == Start.all:
        ax1.xaxis.set_major_locator(YearLocator())
    if period == Start.begin:
        ax1.xaxis.set_major_locator(MonthLocator())

    # From https://matplotlib.org/stable/gallery/ticks/centered_ticklabels.html :
    for label in ax1.get_xticklabels():
        label.set_horizontalalignment("left")

    plt.show()


if __name__ == "__main__":
    typer.run(main)
