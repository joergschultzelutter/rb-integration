import requests
import sqlite3
import logging
from iso3166 import countries

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(module)s -%(levelname)s- %(message)s"
)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.con = sqlite3.connect("repeater.db")
        self.cursor = self.con.cursor()
        self.create_repeater_table()  # Create table if missing

    def create_repeater_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS repeater (
                rptr_id INTEGER PRIMARY KEY NOT NULL,
                state_id INTEGER,
                frequency REAL,
                input_freq REAL,
                nearest_city TEXT,
                landmark TEXT,
                state TEXT,
                country TEXT,
                lat REAL,
                lon REAL,
                precise INT,
                callsign TEXT,
                use TEXT,
                operational_status TEXT,
                ares INT,
                races INT,
                skywarn INT,
                canwarn INT,
                allstar_node TEXT,
                echolink_node TEXT,
                irlp_node TEXT,
                wires_node TEXT,
                fm_analog INT,
                dmr INT,
                dmr_color_code TEXT,
                dmr_id TEXT,
                dstar int,
                nxdn INT,
                apco_p25 INT,
                p25_nac TEXT,
                m17 INT,
                m17_can TEXT,
                tetra INT,
                tetra_mcc TEXT,
                tetra_mnc TEXT,
                system_fusion INT,
                ysf_dg_id_uplink TEXT,
                ysf_dg_id_downlink TEXT,
                ysf_dsc TEXT,
                notes TEXT,
                last_update TEXT
            );
            """
        )
        self.con.commit()

    def insert_repeater_record(
        self, latitude: float, longitude: float, name: str, country: str, state: str
    ):


#        cursor.executemany("""
#        INSERT INTO daten (laenge, breite) VALUES (?, ?)
#        """, [(laenge, breite) for laenge, breite in daten])
        
        
        self.cursor.execute(
            "INSERT INTO repeater(latitude, longitude, name, country_a2, state_a2) VALUES(?, ?, ?, ?, ?)",
            (latitude, longitude, name, country, state),
        )
        self.con.commit()

    def get_nearest_repeater(self,latitude: float, longitude: float):
        abruf = """
        SELECT id, latitude, longitude
        FROM daten
        ORDER BY
          (
            6371 * acos(
              cos(radians(?)) * cos(radians(longitude)) * cos(radians(?) - radians(latitude)) +
              sin(radians(?)) * sin(radians(longitude))
            )
          ) ASC
        LIMIT 1;
        """

        # Abruf mit eigenen Koordinaten ausführen
        cursor.execute(abruf, (latitude, longitude))

        # Ergebnis abrufen
        ergebnis = cursor.fetchone()

        # Nächster Eintrag
        naechster_laenge, naechster_breite, naechster_id = ergebnis



    def close_db_connection(self):
        self.cursor.close()
        self.con.close()

if __name__ == "__main__":
    a = countries.get("United States")
    pass