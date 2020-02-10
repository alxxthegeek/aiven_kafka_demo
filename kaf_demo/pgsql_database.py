#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import logging
import logging.config
import configparser
import sys


class postgres_database_handler(object):
    def __init__(self):
        print('starting database handler')
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

    def connect_to_database(self, database_name, database_user, database_password, database_host, database_port):
        con = psycopg2.connect(database=database_name, user=database_user, password=database_password, host=database_host, port=database_port)
        # con = psycopg2.connect(database=database_name)
        print('Connected to database')
        return con

    def connect(self):
        con = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpassword, host=self.dbhost, port=self.dbport)
        # con = psycopg2.connect(database=self.dbname)
        print('Connected to database ')
        return con

    def get_cursor(self, connection):
        return connection.cursor();

    def check_database(self, cursor):
        # query = f'"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.dbname}'"'
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
        '''
        connection.close()
        return

    def get_table_info(self):

        return

    def logging_start(self):
        '''Start logging'''
        self.create_log_file(self.debug_log, logging.DEBUG)
        self.create_log_file(self.info_log, logging.INFO)
        self.create_log_file(self.error_log, logging.ERROR)
        logging.getLogger('').setLevel(logging.DEBUG)
        return

    def create_log_file(self, filename, level):
        """Create log files , set handler and formating """
        handler = logging.handlers.RotatingFileHandler(filename)
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        handler.maxBytes = 256000000
        handler.backupCount = 10
        formatter = logging.Formatter(
            '%(asctime)s-15s [%(levelname)s] %(filename)s %(processName)s %(funcName)s %(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        return


if __name__ == "__main__":
    db = postgres_database_handler()
    conn = db.connect()
    cursor = db.get_cursor(conn)
    db.check_database(cursor)
    db.close_database(conn)
