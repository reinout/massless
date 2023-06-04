import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import xmltodict

ALCOHOL_FILE = pathlib.Path("alcohol.txt")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
ROLLING_PERIOD = 21


def alcohol_as_xml():
    """Return alcohol file as somewhat-OK xml"""
    result = '<?xml version="1.0" encoding="UTF-8"?><wrapper>'
    contents = ALCOHOL_FILE.read_text()
    result += contents.replace(">", " />")
    result += "</wrapper>"
    return result


def _value_to_glasses(value):
    """Return 'alcohol unit' value as number of Dutch glasses.

    1 AU is defined as 10ml pure alcohol in the UK (where the app comes from).
    In NL it is 12.7ml.
    """
    return float(value) / 1.27


def main(grouping="month"):
    alcohol_data = xmltodict.parse(alcohol_as_xml())
    alcohol_dictlist = alcohol_data["wrapper"]["Record"]
    alcohol_cleaned_dictlist = [
        {
            "date": d["@startDate"],
            "glasses": _value_to_glasses(d["@value"]),
        }
        for d in alcohol_dictlist
    ]
    alcohol = pd.DataFrame(alcohol_cleaned_dictlist)
    alcohol.index = pd.to_datetime(alcohol["date"])
    alcohol.drop(columns=["date"], inplace=True)
    alcohol_per_day = alcohol.resample("D").sum()
    alcohol_per_day["gemiddelde"] = (
        alcohol_per_day["glasses"].rolling(ROLLING_PERIOD).mean()
    )

    x = list(alcohol_per_day.index)
    y = list(alcohol_per_day["glasses"])
    y2 = list(alcohol_per_day["gemiddelde"])
    fig, ax = plt.subplots()
    ax.plot(x, y, "+", color="orange")
    ax.plot(x, y2, linestyle="solid", color="blue", label="gemiddelde")

    ax.set_ylabel("Glazen/dag")
    ax.grid(True)

    # total_mean = alcohol_per_day["glasses"].mean()
    # ax.axhline(total_mean)

    plt.show()


if __name__ == "__main__":
    main()
