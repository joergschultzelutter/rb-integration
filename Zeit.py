"""

Ich habe Längen- und Breitengrad für einen bestimmten Punkt auf der Erde und möchte gerne bestimmen, wann für diesen Punkt die Tages- und Nachtzeiten "Nacht", "Morgen", "Mittag" und "Abend" stattfinden. Für "Nacht" wird 0 Uhr UTC angenommen, für "Morgen" 6 Uhr UTC, "Mittag" 12 Uhr UTC und "Abend" 18 Uhr UTC.  Ziel ist es, für den angegebenen Längen- und Breitengrad die Offsets und die Zeit in lokaler Zeit zu errechnen. Es soll dabei auch Sommer- und Winterzeit berücksichtigt werden. Erstelle bitte Python-Code

"""





import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder


def get_local_times(lat, lon, date):
    # Determine the timezone for the given latitude and longitude
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)

    if timezone_str is None:
        raise ValueError("Could not determine the timezone for the given coordinates.")

    # Get the timezone object
    timezone = pytz.timezone(timezone_str)

    # Define UTC times for "Nacht", "Morgen", "Mittag", and "Abend"
    utc_times = {
        "night": datetime(date.year, date.month, date.day, 0, 0, tzinfo=pytz.utc),
        "morning": datetime(date.year, date.month, date.day, 6, 0, tzinfo=pytz.utc),
        "daytime": datetime(date.year, date.month, date.day, 12, 0, tzinfo=pytz.utc),
        "evening": datetime(date.year, date.month, date.day, 18, 0, tzinfo=pytz.utc),
    }

    # Convert UTC times to local times
    local_times = {}
    for key, utc_time in utc_times.items():
        local_time = utc_time.astimezone(timezone)
        utc_offset = local_time.utcoffset()
        local_times[key] = {
            'local_time_str': local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            'local_time': local_time,
            'utc_offset': utc_offset
        }

    return local_times


# Example usage
latitude = 52.5200  # Example: Berlin
longitude = 13.4050
latitude = 34.03  # Example: Berlin
longitude = -118.24
date = datetime(2024, 5, 19,22,45,00)  # Date for which to calculate the times

local_times = get_local_times(latitude, longitude, date)
for time_of_day, info in local_times.items():
    print(f"{time_of_day}: {info['local_time_str']} {info['local_time']} (UTC offset: {info['utc_offset']})")
