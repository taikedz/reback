# Lookup/register pings

import sqlite3

DB_FILE = "reback-pings.sqlite"


def save_ping(mac, ip, hostname, data):
    """
    Save in simple SQLite database

    table:Pings -> ID, timestamp, mac, ip, hostname, data(string)
    """


def query_ping(criterea:dict):
    """ lookup based on ip, mac, hostname and/or data content...
    """


