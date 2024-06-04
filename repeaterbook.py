import requests
import logging
import os
import datetime
import json

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)

NA_COUNTRIES = [
    "United States",
    "Canada",
    "Mexico",
]
STATES = {
    "United States": [
        "Alaska",
        "Alabama",
        "Arkansas",
        "Arizona",
        "California",
        "Colorado",
        "Connecticut",
        "District of Columbia",
        "Delaware",
        "Florida",
        "Georgia",
        "Guam",
        "Hawaii",
        "Iowa",
        "Idaho",
        "Illinois",
        "Indiana",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Massachusetts",
        "Maryland",
        "Maine",
        "Michigan",
        "Minnesota",
        "Missouri",
        "Mississippi",
        "Montana",
        "North Carolina",
        "North Dakota",
        "Nebraska",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "Nevada",
        "New York",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Puerto Rico",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Virginia",
        "Virgin Islands",
        "Vermont",
        "Washington",
        "Wisconsin",
        "West Virginia",
        "Wyoming",
    ],
    "Canada": [
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland",
        "Northwest Territories",
        "Nova Scotia",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon Territory",
    ],
    "Mexico": [
        "Aguascalientes",
        "Baja California Sur",
        "Baja California",
        "Campeche",
        "Chiapas",
        "Chihuahua",
        "Coahuila",
        "Colima",
        "Durango",
        "Guanajuato",
        "Guerrero",
        "Hidalgo",
        "Jalisco",
        "Mexico City",
        "Mexico",
        "Michoacán",
        "Morelos",
        "Nayarit",
        "Nuevo Leon",
        "Puebla",
        "Queretaro",
        "Quintana Roo",
        "San Luis Potosi",
        "Sinaloa",
        "Sonora",
        "Tabasco",
        "Tamaulipas",
        "Tlaxcala",
        "Veracruz",
        "Yucatan",
        "Zacatecas",
    ],
}

ROW_COUNTRIES = [
    "Albania",
    "Andorra",
    "Argentina",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Brazil",
    "Bulgaria",
    "Caribbean Netherlands",
    "Cayman Islands",
    "Chile",
    "China",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Curacao",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Dominican Republic",
    "Ecuador",
    "El Salvador",
    "Estonia",
    "Faroe Islands",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guernsey",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Kosovo",
    "Kuwait",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macedonia",
    "Malaysia",
    "Malta",
    "Moldova",
    "Morocco",
    "Namibia",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Norway",
    "Oman",
    "Panama",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Romania",
    "Russia",
    "Saint Kitts and Nevis",
    "Saint Vincent and the Grenadines",
    "San Marino",
    "Serbia",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sri Lanka",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "Trinidad and Tobago",
    "Turkey",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "Uruguay",
    "Venezuela",
]

#COUNTRIES = list(sorted(NA_COUNTRIES + ROW_COUNTRIES))

headers = {
    "User-Agent": f"multi-purpose-aprs-daemon/0.51 (+https://github.com/joergschultzelutter/mpad/)"
}


def get_data(country, state, service: str = ""):
    # Ideally we would be able to pull the whole database, but right
    # now this is limited to 3500 results, so we need to filter and
    # cache by state to stay under that limit.
    fn = "rb%s-%s-%s.json" % (
        service,
        country.lower().replace(" ", "_"),
        state.lower().replace(" ", "_"),
    )
    db_dir = "repeaterbook"
    try:
        os.mkdir(db_dir)
    except FileExistsError:
        pass
    except Exception as e:
        logger.exception("Failed to create %s: %s" % (db_dir, e))
        return
    data_file = os.path.join(db_dir, fn)
    try:
        modified = os.path.getmtime(data_file)
    except FileNotFoundError:
        modified = 0
    modified_dt = datetime.datetime.fromtimestamp(modified)
    interval = datetime.timedelta(days=30)
    if datetime.datetime.now() - modified_dt < interval:
        return data_file
    if modified == 0:
        logger.debug(f"RepeaterBook database {fn} not cached")
    else:
        logger.debug(f"RepeaterBook database {fn} too old.")

    params = {"country": country, "stype": service}
    if country in NA_COUNTRIES:
        export = "export.php"
    else:
        export = "exportROW.php"
    if country in STATES:
        params["state"] = state

    r = requests.get(
        "https://www.repeaterbook.com/api/%s" % export,
        headers=headers,
        params=params,
        stream=True,
    )
    if r.status_code != 200:
        if modified:
            logger.debug("Using cached data")
        logger.debug(f"Got error code {r.status_code} from server")
        return
    tmp = data_file + ".tmp"
    chunk_size = 8192
    probable_end = 3 << 20
    counter = 0
    data = b""
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            data += chunk
            counter += len(chunk)
            logger.debug("Downloading", counter / probable_end * 50)
    try:
        results = json.loads(data)
    except Exception as e:
        logger.exception(f"Invalid JSON in response: {e}")
        return

    if results["count"]:
        try:
            os.rename(tmp, data_file)
        except FileExistsError:
            # Windows can't do atomic rename
            os.remove(data_file)
            os.rename(tmp, data_file)
    else:
        os.remove(tmp)
        logger.debug("No results!")
        return

    logger.debug("Download complete")
    return data_file


if __name__ == "__main__":
    a = get_data("Russia","","")
    logger.debug(a)
