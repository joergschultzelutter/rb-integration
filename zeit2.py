import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder


def get_timezone(lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)

    if timezone_str is None:
        raise ValueError("Could not determine the timezone for the given coordinates.")

    return pytz.timezone(timezone_str)


def get_local_and_utc_times(lat, lon, base_date):
    # Ermittlung der Zeitzone
    timezone = get_timezone(lat, lon)

    # Definition der lokalen Zeiten
    local_times = {
        "Nacht": datetime(base_date.year, base_date.month, base_date.day, 0, 0),
        "Morgen": datetime(base_date.year, base_date.month, base_date.day, 6, 0),
        "Mittag": datetime(base_date.year, base_date.month, base_date.day, 12, 0),
        "Abend": datetime(base_date.year, base_date.month, base_date.day, 18, 0),
    }

    local_and_utc_times = {}
    for key, local_time in local_times.items():
        local_time = timezone.localize(local_time)  # Lokalisierung der lokalen Zeit
        utc_time = local_time.astimezone(pytz.utc)  # Konvertierung in UTC
        utc_offset = local_time.utcoffset()

        local_and_utc_times[key] = {
            'local_time': local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            'utc_time': utc_time,
            'utc_offset': utc_offset
        }

    return local_and_utc_times


def find_best_matching_time(target_utc_time, weather_data):
    min_diff = timedelta.max
    best_entry = None

    for entry in weather_data:
        current_diff = entry['timestamp'] - target_utc_time
        if current_diff.total_seconds() >= 0 and current_diff < min_diff:
            min_diff = current_diff
            best_entry = entry

    return best_entry


# Beispiel-Liste mit Zeitstempeln in UTC (Stunden- und 6-Stunden-Rhythmus)
import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder


def get_timezone(lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)

    if timezone_str is None:
        raise ValueError("Could not determine the timezone for the given coordinates.")

    return pytz.timezone(timezone_str)


def get_local_and_utc_times(lat, lon, base_date):
    # Ermittlung der Zeitzone
    timezone = get_timezone(lat, lon)

    # Definition der lokalen Zeiten
    local_times = {
        "Nacht": datetime(base_date.year, base_date.month, base_date.day, 0, 0),
        "Morgen": datetime(base_date.year, base_date.month, base_date.day, 6, 0),
        "Mittag": datetime(base_date.year, base_date.month, base_date.day, 12, 0),
        "Abend": datetime(base_date.year, base_date.month, base_date.day, 18, 0),
    }

    local_and_utc_times = {}
    for key, local_time in local_times.items():
        local_time = timezone.localize(local_time)  # Lokalisierung der lokalen Zeit
        utc_time = local_time.astimezone(pytz.utc)  # Konvertierung in UTC
        utc_offset = local_time.utcoffset()

        local_and_utc_times[key] = {
            'local_time': local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            'utc_time': utc_time,
            'utc_offset': utc_offset
        }

    return local_and_utc_times


def find_best_matching_time(target_utc_time, weather_data):
    half_max_gap = timedelta(hours=3)
    best_entry = None
    min_diff = timedelta.max

    for entry in weather_data:
        current_diff = entry['timestamp'] - target_utc_time
        if abs(current_diff) < min_diff:
            min_diff = abs(current_diff)
            best_entry = entry

    if min_diff <= half_max_gap:
        return best_entry  # Return the closest entry within the half max gap

    # If no close entry found within half max gap, find the next greater or smaller entry based on the time difference
    next_greater_entry = None
    next_smaller_entry = None

    for entry in weather_data:
        if entry['timestamp'] >= target_utc_time:
            next_greater_entry = entry
            break
        next_smaller_entry = entry

    # Return the appropriate entry based on the condition
    if next_greater_entry and next_smaller_entry:
        if (next_greater_entry['timestamp'] - target_utc_time) < (target_utc_time - next_smaller_entry['timestamp']):
            return next_greater_entry
        else:
            return next_smaller_entry
    elif next_greater_entry:
        return next_greater_entry
    elif next_smaller_entry:
        return next_smaller_entry
    else:
        return None  # No matching entry found


# Beispiel-Liste mit Zeitstempeln in UTC (Stunden- und 6-Stunden-Rhythmus)
weather_data = [
    {'timestamp': datetime(2024, 5, 15, 0, 0, tzinfo=pytz.utc), 'index': 0},
    {'timestamp': datetime(2024, 5, 15, 6, 0, tzinfo=pytz.utc), 'index': 1},
    {'timestamp': datetime(2024, 5, 15, 12, 0, tzinfo=pytz.utc), 'index': 2},
    {'timestamp': datetime(2024, 5, 15, 18, 0, tzinfo=pytz.utc), 'index': 3},
    {'timestamp': datetime(2024, 5, 16, 0, 0, tzinfo=pytz.utc), 'index': 4},
    {'timestamp': datetime(2024, 5, 16, 6, 0, tzinfo=pytz.utc), 'index': 5},
    {'timestamp': datetime(2024, 5, 16, 12, 0, tzinfo=pytz.utc), 'index': 6},
    {'timestamp': datetime(2024, 5, 16, 18, 0, tzinfo=pytz.utc), 'index': 7},
    {'timestamp': datetime(2024, 5, 17, 0, 0, tzinfo=pytz.utc), 'index': 8},
    {'timestamp': datetime(2024, 5, 17, 1, 0, tzinfo=pytz.utc), 'index': 9},
    {'timestamp': datetime(2024, 5, 17, 2, 0, tzinfo=pytz.utc), 'index': 10},
    {'timestamp': datetime(2024, 5, 17, 3, 0, tzinfo=pytz.utc), 'index': 11},
    {'timestamp': datetime(2024, 5, 17, 4, 0, tzinfo=pytz.utc), 'index': 12},
    {'timestamp': datetime(2024, 5, 17, 5, 0, tzinfo=pytz.utc), 'index': 13},
    {'timestamp': datetime(2024, 5, 17, 6, 0, tzinfo=pytz.utc), 'index': 14},
    {'timestamp': datetime(2024, 5, 17, 7, 0, tzinfo=pytz.utc), 'index': 15},
    {'timestamp': datetime(2024, 5, 17, 8, 0, tzinfo=pytz.utc), 'index': 16},
    {'timestamp': datetime(2024, 5, 17, 9, 0, tzinfo=pytz.utc), 'index': 17},
    {'timestamp': datetime(2024, 5, 17, 10, 0, tzinfo=pytz.utc), 'index': 18},
    {'timestamp': datetime(2024, 5, 17, 11, 0, tzinfo=pytz.utc), 'index': 19},
    {'timestamp': datetime(2024, 5, 17, 12, 0, tzinfo=pytz.utc), 'index': 20},
    {'timestamp': datetime(2024, 5, 17, 13, 0, tzinfo=pytz.utc), 'index': 21},
    {'timestamp': datetime(2024, 5, 17, 14, 0, tzinfo=pytz.utc), 'index': 22},
    {'timestamp': datetime(2024, 5, 17, 15, 0, tzinfo=pytz.utc), 'index': 23},
    {'timestamp': datetime(2024, 5, 17, 16, 0, tzinfo=pytz.utc), 'index': 24},
    {'timestamp': datetime(2024, 5, 17, 17, 0, tzinfo=pytz.utc), 'index': 25},
    {'timestamp': datetime(2024, 5, 17, 18, 0, tzinfo=pytz.utc), 'index': 26},
    {'timestamp': datetime(2024, 5, 17, 19, 0, tzinfo=pytz.utc), 'index': 27},
    {'timestamp': datetime(2024, 5, 17, 20, 0, tzinfo=pytz.utc), 'index': 28},
    {'timestamp': datetime(2024, 5, 17, 21, 0, tzinfo=pytz.utc), 'index': 29},
    {'timestamp': datetime(2024, 5, 17, 22, 0, tzinfo=pytz.utc), 'index': 30},
    {'timestamp': datetime(2024, 5, 17, 23, 0, tzinfo=pytz.utc), 'index': 31},
    {'timestamp': datetime(2024, 5, 18, 0, 0, tzinfo=pytz.utc), 'index': 32},
    {'timestamp': datetime(2024, 5, 18, 6, 0, tzinfo=pytz.utc), 'index': 33},
    {'timestamp': datetime(2024, 5, 18, 12, 0, tzinfo=pytz.utc), 'index': 34},
    {'timestamp': datetime(2024, 5, 18, 18, 0, tzinfo=pytz.utc), 'index': 35},
    # Weitere Einträge ...
]
# Beispielnutzung
latitude = 52.5200  # Beispiel: Berlin
longitude = 13.4050
base_date = datetime(2024, 5, 17)  # Datum, für das die Zeiten berechnet werden sollen

times = get_local_and_utc_times(latitude, longitude, base_date)

"""
for time_of_day, info in times.items():
    print(f"{time_of_day}:")
    print(f"  Local Time: {info['local_time']}")
    print(f"  UTC Time: {info['utc_time'].strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    print(f"  UTC Offset: {info['utc_offset']}\n")

    best_entry = find_best_matching_time(info['utc_time'], weather_data)
    if best_entry:
        print(f"  Best Matching Entry: {best_entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S %Z%z')} (Index: {best_entry['index']})\n")
    else:
        print("  No matching entry found\n")
"""

# Beispielnutzung
latitude = 52.5200  # Beispiel: Berlin
longitude = 13.4050
base_date = datetime(2024, 5, 17)  # Datum, für das die Zeiten berechnet werden sollen

times = get_local_and_utc_times(latitude, longitude, base_date)

for time_of_day, info in times.items():
    print(f"{time_of_day}:")
    print(f"  Local Time: {info['local_time']}")
    print(f"  UTC Time: {info['utc_time'].strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    print(f"  UTC Offset: {info['utc_offset']}\n")

    best_entry = find_best_matching_time(info['utc_time'], weather_data)
    if best_entry:
        print(f"  Best Matching Entry: {best_entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S %Z%z')} (Index: {best_entry['index']})\n")
    else:
        print("  No matching entry found\n")
