import requests
import sqlite3
import logging

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
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                latitude FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                name VARCHAR(256) NOT NULL,
                country_a2 VARCHAR(2) NOT NULL,
                state_a2 VARCHAR(2),
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
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
        cursor.execute(abruf, (eigene_laenge, eigene_breite))

        # Ergebnis abrufen
        ergebnis = cursor.fetchone()

        # Nächster Eintrag
        naechster_laenge, naechster_breite, naechster_id = ergebnis



    def close_db_connection(self):
        self.cursor.close()
        self.con.close()