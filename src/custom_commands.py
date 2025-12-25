import logging
from datetime import timedelta

from db import get_database_pool
from twitchio.ext import routines

LOGGER: logging.Logger = logging.getLogger("CustomCommands")


### COMMANDS ###
async def get_command(command, channel_id):
    try:
        pool = await get_database_pool()
        
        async with pool.acquire() as connection:
            query = "SELECT text FROM commands WHERE command = ? AND channel_id = ?"
            async with connection.execute(query, (command, channel_id)) as cursor:
                row = await cursor.fetchone()
                return row["text"] if row else None

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return None

async def add_command(command, channel_id, text):
    try:
        pool = await get_database_pool()
        LOGGER.info('Adding new command')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO commands VALUES (?, ?, ?)"
            await connection.execute(query, (command, channel_id, text))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def edit_command(command, channel_id, text):
    try:
        pool = await get_database_pool()
        LOGGER.info('Editing command')
        
        async with pool.acquire() as connection:
            query = "UPDATE commands SET text = ? WHERE command = ? AND channel_id = ?"
            await connection.execute(query, (text, command, channel_id))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def remove_command(command, channel_id):
    try:
        pool = await get_database_pool()
        LOGGER.info('Removing command')
        
        async with pool.acquire() as connection:
            query = "DELETE FROM commands WHERE command = ? AND channel_id = ?"
            await connection.execute(query, (command, channel_id))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


### ROUTINES ###
def routine_factory(channel, seconds, minutes, hours, routine_text):
    @routines.routine(delta=timedelta(seconds=seconds, minutes=minutes, hours=hours), wait_first=False)
    async def temp_routine():
        await channel.send(routine_text)

    return temp_routine


async def add_routine(channel, name, seconds, minutes, hours, routine_text):
    try:
        pool = await get_database_pool()
        LOGGER.info('Adding new routine to db')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO routines VALUES (?, ?, ?, ?, ?, ?)"
            await connection.execute(query, (channel, name, seconds, minutes, hours, routine_text))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def init_routines(bot):
    """ Loads routines from SQLite database """
    routines_db = {}
    try:
        pool = await get_database_pool()
        LOGGER.info('Initializing routines')
        
        async with pool.acquire() as connection:
            query = "SELECT * FROM routines"
            async with connection.execute(query) as cursor:
                async for row in cursor:
                    channel = bot.get_channel(row["channel"])
                    routines_db[row["channel"] + '_' + row["name"]] = routine_factory(
                        channel=channel,
                        seconds=int(row["seconds"]),
                        minutes=int(row["minutes"]),
                        hours=int(row["hours"]),
                        routine_text=row["routine_text"]
                    )
                    routines_db[row["channel"] + '_' + row["name"]].start()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
    
    return routines_db


async def remove_routine(channel, name):
    try:
        pool = await get_database_pool()
        LOGGER.info('Removing routine from db')
        
        async with pool.acquire() as connection:
            query = "DELETE FROM routines WHERE channel = ? AND name = ?"
            await connection.execute(query, (channel, name))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


### COUNTERS ###
async def set_counter(channel_id, counter):
    try:
        pool = await get_database_pool()
        LOGGER.info('Setting counter in db')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO counters (channel, counter) VALUES (?, ?)"
            await connection.execute(query, (channel_id, counter))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def get_counter(channel_id):
    try:
        pool = await get_database_pool()
        LOGGER.info('Getting counter from db')
        
        async with pool.acquire() as connection:
            query = "SELECT counter FROM counters WHERE channel = ?"
            async with connection.execute(query, (channel_id,)) as cursor:
                row = await cursor.fetchone()
                return row["counter"] if row else 0

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return 0


### COOLDOWNS ###
async def get_kappagen_cooldown(channel_id):
    try:
        pool = await get_database_pool()
        LOGGER.info(f'Getting kappagen cooldown for channel {channel_id} from db')
        
        async with pool.acquire() as connection:
            query = "SELECT kappagen_cooldown FROM channels WHERE channel_id = ?"
            async with connection.execute(query, (channel_id,)) as cursor:
                row = await cursor.fetchone()
                return row["kappagen_cooldown"] if row else 0

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return 0


async def set_kappagen_cooldown(channel_id, cooldown):
    try:
        pool = await get_database_pool()
        LOGGER.info('Setting kappagen cooldown in db')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO channels (channel_id, kappagen_cooldown) VALUES (?, ?)"
            await connection.execute(query, (channel_id, cooldown))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


### CHANNEL PROPERTIES ###
async def update_bot_replies(channel_id, bot_reply):
    """Enables or disables automatic bot replies"""
    try:
        pool = await get_database_pool()
        LOGGER.info(f'Updating bot replies for channel {channel_id}')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO channels (channel_id, bot_reply) VALUES (?, ?)"
            await connection.execute(query, (channel_id, bot_reply))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def is_bot_reply(channel_id) -> bool:
    try:
        pool = await get_database_pool()
        LOGGER.info(f'Getting bot reply status for channel {channel_id} from db')
        
        async with pool.acquire() as connection:
            query = "SELECT bot_reply FROM channels WHERE channel_id = ?"
            async with connection.execute(query, (channel_id,)) as cursor:
                row = await cursor.fetchone()
                return row["bot_reply"] if row else True

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return True


async def update_vip_so(channel_id, vip_so):
    """Enables or disables automatic vip shoutouts"""
    try:
        pool = await get_database_pool()
        LOGGER.info(f'Updating auto VIP shoutout for channel {channel_id}')
        
        async with pool.acquire() as connection:
            query = "INSERT OR REPLACE INTO channels (channel_id, vip_so) VALUES (?, ?)"
            await connection.execute(query, (channel_id, vip_so))
            await connection.commit()

    except Exception as error:
        LOGGER.error(f"Database error: {error}")


async def is_vip_so(channel_id) -> bool:
    try:
        pool = await get_database_pool()
        LOGGER.debug(f'Getting vip shoutout status for channel {channel_id} from db')
        
        async with pool.acquire() as connection:
            query = "SELECT vip_so FROM channels WHERE channel_id = ?"
            async with connection.execute(query, (channel_id,)) as cursor:
                row = await cursor.fetchone()
                return row["vip_so"] if row else True

    except Exception as error:
        LOGGER.error(f"Database error: {error}")
        return True
