import psycopg
import aiohttp
import asyncio
import logging
import os
from configparser import ConfigParser

LOGGER: logging.Logger = logging.getLogger("DB")

def config(filename='./database_auth.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


async def get_token(user):
    """ Connects to the PostgreSQL database server and returns user token """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        LOGGER.info('Retrieving access token')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT token, refresh_token FROM users where id ='{user}'"
        )
        token = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')

    return await validate(token[0], token[1])


async def validate(token, refresh_token):
    """ Checks if token is valid and refreshes if needed """
    LOGGER.info('Validating token')

    url = 'https://id.twitch.tv/oauth2'
    auth = "Bearer " + token
    id = os.environ['CLIENT_ID']
    headers = {
        "Client-Id": id,
        "Authorization": auth
    }
    params = {
        'grant_type': 'refresh_token',
        'client_id': os.environ['CLIENT_ID'],
        'client_secret': os.environ['CLIENT_SECRET'],
        'refresh_token': refresh_token
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url + '/validate', headers=headers) as resp:
            if resp.status == 200:
                return token
            else:
                pass

        async with session.post(url + '/token', params=params) as refresh_resp:
            # Requests new access token
            # LOGGER.info(await refresh_resp.json())
            data = await refresh_resp.json()
            new_token = data['access_token']

            # Updates db
            try:
                # read connection parameters
                params = config()

                # connect to the PostgreSQL server
                LOGGER.info('Updating access token')
                conn = psycopg.connect(**params)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                cur.execute(
                    f"UPDATE users SET token = '{new_token}' WHERE token = '{token}' AND refresh_token = '{refresh_token}'"
                )

                conn.commit()
                # close the communication with the PostgreSQL
                cur.close()
            except (Exception, psycopg.DatabaseError) as error:
                LOGGER.error(error)
            finally:
                await session.close()
                if conn is not None:
                    conn.close()
                    LOGGER.info('Database connection closed.')

        return new_token


def init_channels():
    """ Connects to the PostgreSQL database server and initializes the channels list """
    conn = None
    try:
        # read connection parameters
        channels = []
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        LOGGER.info('Initializing channels')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT name FROM channels"
        )
        channels_raw = cur.fetchall()
        for channel in channels_raw:
            channels.append(channel[0])

        # close the communication with the PostgreSQL
        cur.close()

        return channels

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')


def add_channel(channel, id):
    """ Connects to the PostgreSQL database server and adds a channel"""
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        LOGGER.info(f'Adding channel {channel} to db')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            "INSERT INTO channels (name, id) VALUES (%s, %s),", (channel, id)
        )

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')


def leave_channel(channel):
    """ Connects to the PostgreSQL database server and removes a channel"""
    conn = None
    try:
        # read connection parameters
        channels = []
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        LOGGER.info(f'Removing channel {channel} to db')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            "DELETE FROM channels WHERE name=%s", (channel, )
        )

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')


def get_channels_info()->dict:
    """ Connects to the PostgreSQL database server and removes a channel"""
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        LOGGER.info(f'Getting channel ids')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            "SELECT id, name FROM channels"
        )

        infos = cur.fetchall()
        di = {}
        for id, name in infos:
            di.setdefault(id, name)
        
        # close the communication with the PostgreSQL
        cur.close()

        return di

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')


def update_name(id: int, channel: str):
    """ Connects to the PostgreSQL database server and removes a channel"""
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        LOGGER.info(f'Updating channel {id} with name {channel}')
        conn = psycopg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            "UPDATE channels SET name=%s WHERE id=%s", (channel, id)
        )

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg.DatabaseError) as error:
        LOGGER.error(error)
    finally:
        if conn is not None:
            conn.close()
            LOGGER.info('Database connection closed.')
