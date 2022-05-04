import psycopg2
import aiohttp
import asyncio
import logging
import os
from configparser import ConfigParser


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
        logging.info('Retrieving access token')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT token, refresh_token FROM users where id ='{user}'"
        )
        token = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')

    return await validate(token[0], token[1])


async def validate(token, refresh_token):
    """ Checks if token is valid and refreshes if needed """
    logging.info('Validating token')

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
            # logging.info(resp)
            if resp.status == 200:
                return token
            else:
                pass

        async with session.post(url + '/token', params=params) as refresh_resp:
            # Requests new access token
            # logging.info(await refresh_resp.json())
            data = await refresh_resp.json()
            new_token = data['access_token']

            # Updates db
            try:
                # read connection parameters
                params = config()

                # connect to the PostgreSQL server
                logging.info('Updating access token')
                conn = psycopg2.connect(**params)

                # create a cursor
                cur = conn.cursor()

                # execute a statement
                cur.execute(
                    f"UPDATE users SET token = '{new_token}' WHERE token = '{token}' AND refresh_token = '{refresh_token}'"
                )

                conn.commit()
                # close the communication with the PostgreSQL
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                logging.error(error)
            finally:
                await session.close()
                if conn is not None:
                    conn.close()
                    logging.info('Database connection closed.')

        return new_token


def init_channels():
    """ Connects to the PostgreSQL database server and initializes the channels list """
    conn = None
    try:
        # read connection parameters
        channels = []
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing channels')
        conn = psycopg2.connect(**params)

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

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def add_channel(channel):
    """ Connects to the PostgreSQL database server and initializes the channels list """
    conn = None
    try:
        # read connection parameters
        channels = []
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info(f'Adding channel {channel} to db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"INSERT INTO channels VALUES ('{channel}')"
        )

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def leave_channel(channel):
    """ Connects to the PostgreSQL database server and initializes the channels list """
    conn = None
    try:
        # read connection parameters
        channels = []
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info(f'Removing channel {channel} to db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""DELETE FROM channels WHERE name=%s""", (channel)
        )

        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
