from quart_db import Connection


async def migrate(connection: Connection) -> None:
    await connection.execute(
        """CREATE TABLE tickets(
                counter INTEGER PRIMARY KEY,
                litera CHAR(1) NOT NULL,
                id INTEGER NOT NULL,
                room CHAR(5) NOT NULL,
                status INTEGER NOT NULL
        )""",
    )


async def valid_migration(connection: Connection) -> bool:
    return True