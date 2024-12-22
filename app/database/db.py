import os
import pathlib
import sqlite3
from typing import Any, Dict, List, Optional


class DB:
    connection: Optional[sqlite3.Connection] = None
    current_dir = pathlib.Path(__file__).parent.resolve()
    last_row_id: Optional[int] = None

    @classmethod
    def get_db(cls):
        """
        Connect to the application's configured database.
        The connection is a singleton.
        """
        if not cls.connection:
            cls.connection = sqlite3.connect(
                os.path.join(cls.current_dir, 'doctors.sqlite'),
                detect_types=sqlite3.PARSE_DECLTYPES,
                isolation_level=None,
                check_same_thread=False
            )

        return cls.connection

    @classmethod
    def close_db(cls):
        """
        Close the connection when needed to avoid file lock problems.
        """
        if cls.connection:
            cls.connection.close()

        cls.connection = None

    @classmethod
    def init_db(cls):
        """
        Clear existing data and create new tables.
        """
        db = cls.get_db()

        with open(os.path.join(cls.current_dir, 'schema.sql'), 'r') as f:
            db.executescript(f.read())

    @classmethod
    def seed(cls):
        """
        Insert some starter data.
        """
        db = cls.get_db()

        with open(os.path.join(cls.current_dir, 'seed_data.sql'), 'r') as f:
            db.executescript(f.read())

    @classmethod
    def init_if_needed(cls):
        """
        Check if there are tables, and if not init and then seed.
        """
        cursor = cls.get_db().cursor()

        result = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()

        if not result:
            cls.init_db()
            cls.seed()

    @classmethod
    def execute(cls, query: str, params: List[Any] = []) -> List[Dict[str, Any]]:
        """
        The API for sqlite3 is a bit unfriendly - this wrapper simplifies the interactions.
        """
        cursor = cls.get_db().cursor()

        result = cursor.execute(
            query,
            tuple(params)
        ).fetchall()

        # sqlite returns lists of tuples, annoyingly
        # parse into more useful dictionaries
        result_dicts = [
            dict(zip([key[0] for key in cursor.description], row)) for row in result
        ]

        # admittedly a bit hacky, but this is a very MVP ORM
        cls.last_row_id = cursor.lastrowid

        cursor.close()

        return result_dicts
