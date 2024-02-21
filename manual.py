from geopy.geocoders import Nominatim

# Initialize the geocoder (Nominatim from OpenStreetMap)
geolocator = Nominatim(user_agent="mtfc muthu dogs")
location = "Columbus, OH"
print(
    geolocator.geocode(location).latitude,
    geolocator.geocode(location).longitude,
)
