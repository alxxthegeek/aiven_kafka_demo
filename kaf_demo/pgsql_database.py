#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import logging
import logging.config
import configparser
import sys


class postgresDatabaseHandler(object):
    """
    PostgreSQL Database  handler.
    Connects to a specified PostgreSQL database and table
    """
    def __init__(self):
        print('Starting database handler')
        self.config_file = "../kaf_demo.cfg"
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.config_file)
        except configparser.Error as err:
            print(err)
            logging.error("Error %s "), err
            sys.exit(1)
        self.dbhost = self.config.get('postgres', 'db_host')
        self.dbname = self.config.get('postgres', 'db_name')
        self.dbuser = self.config.get('postgres', 'db_user')
        self.dbport = self.config.get('postgres', 'db_port')
        self.dbpassword = self.config.get('postgres', 'db_password')
        self.dbtablename = self.config.get('postgres', 'db_table_name')
        self.info_log = self.config.get('Log', 'event_log')
        self.error_log = self.config.get('Log', 'error_log')
        self.debug_log = self.config.get('Log', 'debug_log')
        self.logging_start()

    def connect(self):
        """
        Connect to the database using the psycogp2 library connect function

        :return conn: Returns a connection object for the database
        """
        con = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpassword, host=self.dbhost,
                               port=self.dbport)
        print('Connected to database ')
        return con

    def get_cursor(self, connection):
        """
        Get cursor

        :param connection: Connection to the database
        """
        return connection.cursor();

    def check_database(self, cursor):
        """
        Connect to the database and check that it exists

        :param cursor:  database cursor
        """
        query = "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'kaf_demo'"
        cursor.execute(query)
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE kaf_demo with '
                           'Owner = aivenadmin',
                           TABLESPACE='pg_default',
                           encoding="UTF-8",
                           )
        return

    def close_database(self, connection):
        '''
        Close the connection (or handle) to the database

        :param connection: database connection
        :return
        '''
        connection.close()
        return

    def logging_start(self):
        '''Start logging'''
        self.create_log_file(self.debug_log, logging.DEBUG)
        self.create_log_file(self.info_log, logging.INFO)
        self.create_log_file(self.error_log, logging.ERROR)
        logging.getLogger('').setLevel(logging.DEBUG)
        return

    def create_log_file(self, filename, level):
        """
        Create log files , set handler and formating

        :param filename: log file name
        :param level: Log level to set
        :return
        """
        handler = logging.handlers.RotatingFileHandler(filename)
        handler.setLevel(level)
        handler.maxBytes = 256000000
        handler.backupCount = 10
        formatter = logging.Formatter(
            '%(asctime)s-15s [%(levelname)s] %(filename)s %(processName)s %(funcName)s %(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        return


if __name__ == "__main__":
    db = postgresDatabaseHandler()
    conn = db.connect()
    cursor = db.get_cursor(conn)
    db.check_database(cursor)
    db.close_database(conn)
