import pandas as pd
from geopy.geocoders import Nominatim

# Load your spreadsheet
df = pd.read_excel("cities.xlsx")

# Initialize the geocoder (Nominatim from OpenStreetMap)
geolocator = Nominatim(user_agent="mtfc muthu dogs")


# Function to get the coordinates for each row and save the updated DataFrame
def get_coordinates(index, row):
    # get location from geolocator
    location = geolocator.geocode(f"{row['City']}, {row['State']}")
    # If the location is found, update the DataFrame
    if location:
        df.at[index, "Latitude"] = location.latitude
        df.at[index, "Longitude"] = location.longitude
        print(
            f"Coordinates for {row['City']}, {row['State']} found: {location.latitude}, {location.longitude}"
        )
    # Save the updated DataFrame to an Excel file
    df.to_excel("cities_with_coordinates.xlsx", index=False)
    return row


# Apply the geocoding function and save after each row
df.apply(lambda row: get_coordinates(row.name, row), axis=1)
