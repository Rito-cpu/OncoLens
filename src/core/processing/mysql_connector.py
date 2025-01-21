import mysql.connector

from src.core.pyqt_core import *
from src.core.keyword_store import *


class MySQLConnector(QObject):
    def __init__(
        self,
        host: str = None,
        user: str = None,
        password: str = None,
        database: str = None
    ):
        super().__init__()

        self._sql_connection = None
        self._sql_host = host
        self._sql_user = user
        self._sql_password = password
        self._sql_database = database

    def set_host(self, host: str):
        self._sql_host = self.valid_or_none(host)

    def set_user(self, user: str):
        self._sql_user = self.valid_or_none(user)

    def set_password(self, password: str):
        self._sql_password = self.valid_or_none(password)

    def set_database(self, database: str):
        self._sql_database = self.valid_or_none(database)

    def set_sql_information(
        self,
        host: str,
        user: str,
        password: str,
        database: str
    ):
        self._sql_host = self.valid_or_none(host)
        self._sql_user = self.valid_or_none(user)
        self._sql_password =  self.valid_or_none(password)
        self._sql_database = self.valid_or_none(database)

    def establish_connection(self):
        # TODO: SqL DB must be up and running for this to work
        if self.has_none_variable():
            self.close_connection()
            try:
                self._sql_connection = mysql.connector.connect(
                    host=self._sql_host,
                    user=self._sql_user,
                    password=self._sql_password,
                    database=self._sql_database
                )
                print(f'Connection to database succcessful...')
            except Exception as connection_error:
                print(f'Received SQL connection error: \n{str(connection_error)}')
                self._sql_connection = None
        else:
            print('One or more sql values contains a \'None\' value.')

    def close_connection(self):
        if self._sql_connection is not None:
            self._sql_connection.close()
            self._sql_connection = None

    def issue_command(self, command: str):
        if self._sql_connection is not None:
            cursor = self._sql_connection.cursor()
            try:
                cursor.execute(command)
                results = cursor.fetchall()
            except Exception as command_error:
                print(f'Received SQL command error: \n{str(command_error)}')
                results = None
            cursor.close()

            return results
        else:
            print('No SQL connection established.')
            return None

    def select_from_table(self, table: str):
        if table != '' and table is not None:
            command = f'SELECT * FROM {table}'
            self.issue_command(command)

    def has_none_variable(self):
        host_test = self._sql_host is None
        user_test = self._sql_user is None
        password_test = self._sql_password is None
        database_test = self._sql_database is None
        if host_test or user_test or password_test or database_test:
            return False
        else:
            return True

    def valid_or_none(self, input: str):
        if input is not None and input != '':
            return input
        else:
            return None

"""
    self.output_text.clear()
    self.output_text.setPlainText('')
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='DeusFortitudoMea99#',
            database='pyqt_test'
        )

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Person')
        results = cursor.fetchall()
        for result in results:
            per_id, name, gender, age, country = result
            self.output_text.append(f'ID: {per_id}\n\tName: {name}\n\tGender: {gender}\n\tAge: {age}\n\tCountry: {country}')
        # print(f'Gathered Data:\n{str(results)}')
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        self.output_text.append('Error occurred when attempting MySQL connection.')
"""