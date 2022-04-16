import psycopg2
import requests
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


def get_token(user):
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

    return validate(token[0], token[1])


def validate(token, refresh_token):
    """ Checks if token is valid and refreshes if needed """
    url = 'https://id.twitch.tv/oauth2/validate'
    auth = "Bearer " + token
    id = os.environ['CLIENT_ID']
    headers = {
        "Client-Id": id,
        "Authorization": auth
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return token
    else:
        # Requests new access token
        refresh_url = f"https://id.twitch.tv/oauth2/token?grant_type=refresh_token&client_id={os.environ['CLIENT_ID']}&client_secret={os.environ['CLIENT_SECRET']}&refresh_token={refresh_token}"
        refresh_resp = requests.post(refresh_url)
        new_token = refresh_resp.json().get('access_token')

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
        logging.info(channels)

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
        logging.info('Initializing channels')
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
        logging.info(channels)

        return channels

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
