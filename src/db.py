from datetime import datetime

import psycopg2
import psycopg2.extras


class Postgres:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.dbname,
            user=self.user,
            password=self.password,
            cursor_factory=psycopg2.extras.DictCursor
        )

    def get_muted_channels(self, server_id: str):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM muted_channels WHERE server_id = %s",
                    (str(server_id),)
                )

                return cur.fetchall()

    def channel_is_muted(self, server_id: str, channel_id: str):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM muted_channels WHERE server_id = %s AND channel_id = %s",
                    (str(server_id), str(channel_id))
                )

                mute = cur.fetchone()

                if mute is None:
                    return False

                if mute["ends_at"] is None:
                    return True

                if mute["ends_at"] > datetime.now():
                    self.delete_mute(server_id, channel_id)
                    return True

    def create_mute(self, server_id: str, channel_id: str):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO muted_channels (server_id, channel_id) VALUES (%s, %s)",
                    (str(server_id), str(channel_id))
                )

    def delete_mute(self, server_id: str, channel_id: str):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM muted_channels WHERE server_id = %s AND channel_id = %s",
                    (str(server_id), str(channel_id))
                )
