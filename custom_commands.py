import logging
import os
import psycopg2
from db import config

commands = {}


def init_commands():
    """ Connects to the PostgreSQL database server and initializes the custom commands dict """
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing commands')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT * FROM commands"
        )
        commands_raw = cur.fetchall()

        for command in commands_raw:
            commands[(command[0], command[1])] = command[2]

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def find_command(message):
    command = message.content.split()[0]
    channel = message.author.channel.name

    command_text = commands.get((command, channel))

    return command_text


def add_command(command, channel, text):
    commands[(command, channel)] = text

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing commands')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"INSERT INTO commands VALUES ('{command}', '{channel}', '{text}')"
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def edit_command(command, channel, text):
    commands[(command, channel)] = text

    # Now updates db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing commands')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"UPDATE commands SET text='{text}' WHERE command='{command}' AND channel='{channel}' "
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def remove_command(command, channel):
    commands.pop((command, channel))

    # Now updates db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing commands')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM commands WHERE command='{command}' AND channel='{channel}'"
        )

        conn.commit()

        for command in commands_raw:
            logging.info(command[1])
            commands[(command[0], command[1])] = command[2]

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
