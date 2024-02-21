import requests
import pandas as pd
import json

# Load your spreadsheet
df = pd.read_excel("cities.xlsx")

def get_coordinates(index, row):

    data = json.loads(response.text)
    weatherdf = pd.DataFrame(data)

    coordinates = f"{df.at[index, "Latitude"]}, {df.at[index, "Longitude"]}"
    date = df.at[index, "DateAPI"]
    azurePK = "dbmHvhR94mRMlP0MflDiAmtEW5zr0BjjDem5QXK0zho"
    api_url = f"https://atlas.microsoft.com/weather/historical/actuals/daily/json?api-version=1.1&query={coordinates}&startDate={date}&endDate={date}&subscription-key={azurePK}"

    response = requests.get(api_url)
    response.raise_for_status()

    df.at[index, "Precipitation"] = weatherdf['results'][0]['precipitation']['value']
    df.at[index, "Snowfall"] = weatherdf['results'][0]['snowfall']['value']

    # Save the updated DataFrame to an Excel file
    df.to_excel("cities_with_weather.xlsx", index=False)
    return row


# Apply the geocoding function and save after each row
df.apply(lambda row: get_coordinates(row.name, row), axis=1)
