import asqlite
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from twitchio import User

LOGGER: logging.Logger = logging.getLogger("DB")

# Global database pool for shared access
_db_pool: asqlite.Pool = None

async def init_database_pool(db_path: str = "./data/leixbot.db") -> asqlite.Pool:
    """Initialize the database pool and create tables"""
    global _db_pool
    if _db_pool is None:
        _db_pool = await asqlite.create_pool(db_path)
        await create_tables()
    return _db_pool

async def get_database_pool() -> asqlite.Pool:
    """Get the database pool, initializing if necessary"""
    if _db_pool is None:
        return await init_database_pool()
    return _db_pool

async def create_tables():
    """Create all necessary database tables"""
    async with _db_pool.acquire() as connection:   
        # Channels table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                channel_id TEXT PRIMARY KEY,
                name TEXT DEFAULT '',
                kappagen_cooldown INTEGER DEFAULT 0,
                bot_reply BOOLEAN DEFAULT TRUE,
                vip_so BOOLEAN DEFAULT TRUE,
                ads_warning BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Commands table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                command TEXT,
                channel_id TEXT,
                text TEXT,
                PRIMARY KEY (command, channel_id)
            )
        """)
        
        # Routines table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS routines (
                channel TEXT,
                name TEXT,
                seconds INTEGER,
                minutes INTEGER,
                hours INTEGER,
                routine_text TEXT,
                PRIMARY KEY (channel, name)
            )
        """)
        
        # Counters table
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS counters (
                channel TEXT PRIMARY KEY,
                counter INTEGER DEFAULT 0
            )
        """)


async def add_channel(user: User):
    """ Adds a channel to the database if it doesn't exist """
    try:
        pool = await get_database_pool()
        LOGGER.debug(f'Adding channel {user.display_name} to db')
        
        async with pool.acquire() as connection:
            query = "INSERT OR IGNORE INTO channels (channel_id, name) VALUES (?, ?)"
            await connection.execute(query, (user.id, user.display_name))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")

async def get_channel_info(id: str) -> dict:
    """ Gets a channel info from SQLite database """
    try:
        pool = await get_database_pool()
        LOGGER.debug('Getting channel info')
        
        async with pool.acquire() as connection:
            query = "SELECT * FROM channels WHERE channel_id = ?"
            async with connection.execute(query, (id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
                return {}

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return {}
