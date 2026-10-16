import requests
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Heavy thunderstorm with hail",
}


def get_city_coordinates(city):
    """Find a city's latitude and longitude."""
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=15,
    )
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        return None

    return results[0]


def get_weather(city):
    """Fetch current weather for the requested city."""
    place = get_city_coordinates(city)

    if place is None:
        print(f"\nCity '{city}' was not found.")
        print("Check the spelling and try again.")
        return

    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "is_day,"
            "precipitation,"
            "weather_code,"
            "cloud_cover,"
            "pressure_msl,"
            "wind_speed_10m,"
            "wind_direction_10m"
        ),
        "timezone": "auto",
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=15,
    )
    response.raise_for_status()

    data = response.json()
    current = data.get("current", {})
    units = data.get("current_units", {})

    weather_code = current.get("weather_code")
    description = WEATHER_CODES.get(
        weather_code,
        "Unknown conditions",
    )

    # Build the location name without repeating identical parts.
    location_parts = [
        place.get("name"),
        place.get("admin1"),
        place.get("country"),
    ]
    location = ", ".join(
        dict.fromkeys(
            part for part in location_parts if part
        )
    )

    print("\n" + "=" * 45)
    print("           CURRENT WEATHER REPORT")
    print("=" * 45)
    print(f"Location       : {location}")
    print(f"Local time     : {current.get('time', 'N/A')}")
    print(f"Conditions     : {description}")
    print(
        f"Temperature    : {current.get('temperature_2m', 'N/A')} "
        f"{units.get('temperature_2m', '°C')}"
    )
    print(
        f"Feels like     : {current.get('apparent_temperature', 'N/A')} "
        f"{units.get('apparent_temperature', '°C')}"
    )
    print(
        f"Humidity       : {current.get('relative_humidity_2m', 'N/A')}%"
    )
    print(
        f"Wind speed     : {current.get('wind_speed_10m', 'N/A')} "
        f"{units.get('wind_speed_10m', 'km/h')}"
    )
    print(
        f"Wind direction : {current.get('wind_direction_10m', 'N/A')}°"
    )
    print(
        f"Cloud cover    : {current.get('cloud_cover', 'N/A')}%"
    )
    print(
        f"Precipitation  : {current.get('precipitation', 'N/A')} "
        f"{units.get('precipitation', 'mm')}"
    )
    print(
        f"Pressure       : {current.get('pressure_msl', 'N/A')} "
        f"{units.get('pressure_msl', 'hPa')}"
    )
    print("=" * 45)


def main():
    print("===================================")
    print("       WEATHER REPORT APP")
    print("===================================")

    while True:
        city = input(
            "\nEnter city name (or type 'exit' to quit): "
        ).strip()

        if city.lower() in ("exit", "quit"):
            print("Thank you for using the Weather App!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            get_weather(city)
        except requests.RequestException as error:
            print("\nUnable to retrieve weather data.")
            print(f"Details: {error}")
            print("Check your internet connection and try again.")
        except (KeyError, ValueError, TypeError) as error:
            print("\nUnexpected weather data format.")
            print(f"Details: {error}")


if __name__ == "__main__":
    main()


