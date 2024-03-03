import requests
import pandas as pd
import json
import config

# Load your spreadsheet
df = pd.read_excel("newData.xlsx")

dates = [
    "2023-01-01",
    "2023-01-31",
    "2023-02-01",
    "2023-02-28",
    "2023-03-01",
    "2023-03-31",
    "2023-04-01",
    "2023-04-30",
    "2023-05-01",
    "2023-05-31",
    "2023-06-01",
    "2023-06-30",
    "2023-07-01",
    "2023-07-31",
    "2023-08-01",
    "2023-08-31",
    "2023-09-01",
    "2023-09-30",
    "2023-10-01",
    "2023-10-31",
    "2023-11-01",
    "2023-11-30",
    "2023-12-01",
    "2023-12-31",
]

counter = 0


def get_precip(index, row):
    rainfallTotal = 0
    snowfallTotal = 0
    coordinates = f"{df.at[index, 'lat']}, {df.at[index, 'lng']}"

    for i in range(0, len(dates), 2):
        startDate = dates[i]
        endDate = dates[i + 1]
        api_url = f"https://atlas.microsoft.com/weather/historical/actuals/daily/json?api-version=1.1&query={coordinates}&startDate={startDate}&endDate={endDate}&subscription-key={config.AZURE_API_KEY}"

        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Error on row {index}: {response.status_code}")
            df.to_excel("scriptData.xlsx", index=False)
            return row

        data = json.loads(response.text)
        weatherdf = pd.DataFrame(data)
        for i in range(len(weatherdf["results"])):
            if weatherdf["results"][i].get("precipitation") is not None:
                rainfallTotal += weatherdf["results"][i]["precipitation"]["value"]
            if weatherdf["results"][i].get("snowfall") is not None:
                snowfallTotal += weatherdf["results"][i]["snowfall"]["value"]
        print(
            f"Row {index}: Weather for {row['city']}, {row['state_id']} from {startDate} to {endDate} found: {rainfallTotal} inches of precipitation"
        )

    df.at[index, "Average Precipitation"] = rainfallTotal / 365
    df.at[index, "Average Snowfall"] = snowfallTotal / 365

    print(
        f"\nAverage precipitation for {row['city']}, {row['state_id']} is {rainfallTotal / 365} inches\n"
    )

    if counter <= 100:
        counter += 1
    else:
        counter = 0
        df.to_excel("scriptData.xlsx", index=False)

    return row


df.apply(lambda row: get_precip(row.name, row), axis=1)
df.to_excel("scriptData.xlsx", index=False)
