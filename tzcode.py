import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder


def get_utc_offsets(lat, lon, date):
    # Determine the timezone for the given latitude and longitude
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)

    if timezone_str is None:
        raise ValueError("Could not determine the timezone for the given coordinates.")

    # Get the timezone object
    timezone = pytz.timezone(timezone_str)

    # Define local times for "Nacht", "Morgen", "Mittag", and "Abend"
    local_times = {
        "Nacht": datetime(date.year, date.month, date.day, 0, 0),
        "Morgen": datetime(date.year, date.month, date.day, 6, 0),
        "Mittag": datetime(date.year, date.month, date.day, 12, 0),
        "Abend": datetime(date.year, date.month, date.day, 18, 0),
    }

    # Convert local times to UTC times
    utc_times = {}
    for key, local_time in local_times.items():
        local_time = timezone.localize(local_time)  # Localize the naive datetime to the timezone
        utc_time = local_time.astimezone(pytz.utc)
        utc_times[key] = utc_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

    return utc_times


# Example usage
latitude = 52.5200  # Example: Berlin
longitude = 13.4050
date = datetime(2024, 5, 17)  # Date for which to calculate the times

utc_times = get_utc_offsets(latitude, longitude, date)
for time_of_day, utc_time in utc_times.items():
    print(f"{time_of_day}: {utc_time}")
