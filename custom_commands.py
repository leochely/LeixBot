from db import config
from twitchio.ext import routines
import psycopg2
import os
import logging


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
            f"""INSERT INTO commands VALUES (%s, %s, %s)""",
            (command, channel, text)
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
            f"""UPDATE commands SET text=%s WHERE command=%s AND channel=%s """,
            (command, channel, text)
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


### ROUTINES ###
def add_routine(
        channel, name, seconds, minutes,
        hours, routine_text):

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Adding new routine to db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""INSERT INTO routines VALUES (%s, %s, %s, %s, %s, %s)""",
            (channel, name, seconds, minutes, hours, routine_text)
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


def init_routines(bot):
    """ Connects to the PostgreSQL database server and initializes the custom commands dict """
    conn = None
    routines_db = {}
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Initializing routines')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"SELECT * FROM routines"
        )
        routines_raw = cur.fetchall()

        for routine in routines_raw:
            chan = bot.get_channel(routine[0])

            @routines.routine(seconds=int(routine[2]), minutes=int(routine[3]), hours=int(routine[4]), wait_first=False)
            async def temp_routine():
                await chan.send(routine[5])
            routines_db[routine[0] + '_' + routine[1]] = temp_routine
            routines_db[routine[0] + '_' + routine[1]].start()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
        return routines_db


def remove_routine(channel, name):
    # Now updates db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Removing routine from db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"DELETE FROM routines WHERE channel=%s AND name=%s",
            (channel, name)
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


### COUNTERS ###
def set_counter(channel, counter):

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Setting counter in db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""INSERT INTO counters VALUES (%(channel)s, %(counter)s) ON CONFLICT (channel) DO UPDATE SET counter=%(counter)s""",
            {'counter': counter, 'channel': channel}
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


def get_counter(channel):

    # Now adds it to db
    conn = None
    try:
        # read connection parameters
        params = config(filename='database_commands.ini')

        # connect to the PostgreSQL server
        logging.info('Getting counter from db')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(
            f"""SELECT counter FROM counters WHERE channel=%s """,
            (channel,)
        )
        counter = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
        if counter:
            return counter[0]
        else:
            return 0
