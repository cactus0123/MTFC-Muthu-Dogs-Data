import requests
import pandas as pd
import json
import config

# Load your spreadsheet
df = pd.read_excel("newData.xlsx")


def get_weather(index, row):
    rainfallTotal = 0
    cloudTotal = 0

    latitude = df.at[index, "lat"]
    longitude = df.at[index, "lng"]

    api_url = f"https://history.openweathermap.org/data/2.5/aggregated/year?lat={latitude}&lon={longitude}&appid={config.OPENWEATHER_API_KEY}"
    response = requests.get(api_url)
    response.raise_for_status()

    data = json.loads(response.text)
    weatherdf = pd.DataFrame(data)

    for i in range(len(weatherdf["result"])):
        rainfallTotal += weatherdf["result"][i]["precipitation"]["mean"]
        cloudTotal += weatherdf["result"][i]["clouds"]["mean"]

    df.at[index, "Average Precipitation"] = rainfallTotal / 365
    df.at[index, "Average Clouds"] = cloudTotal / 365

    print(
        f"\nAverage precipitation for {row['city']}, {row['state_id']} is {rainfallTotal / 365} inches\n"
    )

    # Save the updated DataFrame to an Excel file
    df.to_excel("scriptData.xlsx", index=False)
    return row


# Apply the geocoding function and save after each row
df.apply(lambda row: get_weather(row.name, row), axis=1)
