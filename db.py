import psycopg2
import psycopg2.extras
from pprint import pprint
import os
from project.server import bcrypt, app

class DatabaseConnection:
    def __init__(self):
        if os.getenv('APP_SETTINGS') == 'project.server.config.DevelopmentConfig':
            self.db_name = 'ireporter_db'
            self.password = '2SweijecIf'
        elif os.getenv('APP_SETTINGS') == 'project.server.config.TravisConfig':
            self.db_name = 'travis_ci_test'
            self.password = ''
        elif os.getenv('APP_SETTINGS') == 'project.server.config.TestingConfig':
            self.db_name = 'ireporter_db_test'
            self.password = '2SweijecIf'

        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name, user='postgres', host='localhost', password=self.password, port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # create users table
            query = """CREATE TABLE IF NOT EXISTS users (userId SERIAL PRIMARY KEY,
                        firstname varchar(32) NOT NULL,
                        lastname varchar(32) NOT NULL,
                        othernames varchar(64) NULL,
                        username varchar(32) NOT NULL,
                        email varchar(128) NOT NULL UNIQUE,
                        password varchar(128) NOT NULL,
                        phone_number varchar(15) NOT NULL,
                        registered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        is_admin boolean NOT NULL DEFAULT '0');
                    """
            self.cursor.execute(query)

            # create incidents table
            query = """
                    CREATE TABLE IF NOT EXISTS incidents (
                        incident_id SERIAL PRIMARY KEY,
                        created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        created_by int,
                        type varchar(16) NOT NULL,
                        location varchar(32) NOT NULL,
                        status varchar(16) NOT NULL DEFAULT 'Pending',
                        images varchar(256) NOT NULL,
                        videos varchar(256) NOT NULL,
                        comment varchar(256) NOT NULL,
                        FOREIGN KEY (created_by) REFERENCES users(userId)
                    )
                    """
            self.cursor.execute(query)

            # create blacklist table
            query = """CREATE TABLE IF NOT EXISTS blacklist (
                    token_id SERIAL PRIMARY KEY,
                    token varchar(500) NOT NULL UNIQUE,
                    blacklisted_on TIMESTAMP NOT NULL DEFAULT
                    CURRENT_TIMESTAMP)"""
            self.cursor.execute(query)
        except:
            pprint('Failed to connect to the database.')

    def blacklist_token(self, token):
        """
        This module will blacklist a token
        """
        try:
            query = """INSERT INTO blacklist (token) VALUES ('%s')
                    """ % token
            self.cursor.execute(query)
            return True
        except Exception as e:
            pprint(e)

    def create_user(self, **kwargs):
        try:
            query = """INSERT INTO users (firstname, lastname, othernames,
                    username,email, password, phone_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING userid"""
            password = bcrypt.generate_password_hash(
                kwargs['password'], app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode()
            self.cursor.execute(query, (kwargs['firstname'], kwargs['lastname'],
                            kwargs['othernames'], kwargs['username'], kwargs['email'],
                            password, kwargs['phone_number']))
            user_id = (self.cursor.fetchone())['userid']
            return user_id
        except Exception as e:
            pprint(e)

    def check_user(self, email):
        try:
            query = "SELECT * FROM users WHERE email = '%s'" % email
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            if user:
                return dict(user)
            return None
        except Exception as e:
            pprint(e)
            return None

    def create_incident(self, **kwargs):
        try:
            query = """INSERT INTO incidents (created_by, type, location,
                    images, videos, comment) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING incident_id"""
            self.cursor.execute(query, (kwargs['created_by'], kwargs['type'],
                kwargs['location'], kwargs['images'],
                kwargs['videos'], kwargs['comment']))
            incident_id = self.cursor.fetchone()
            if incident_id:
                return dict(incident_id)['incident_id']
        except Exception as e:
            pprint(e)

    def is_admin(self, user_id):
        try:
            query="SELECT * FROM users WHERE userid = %d" % user_id
            self.cursor.execute(query)
            user = self.cursor.fetchone()
            if user:
                if dict(user)['is_admin']:
                    return True
                return False
        except Exception as e:
            pprint(e)

    def delete_incident(self, id):
        try:
            query = "DELETE FROM incidents WHERE incident_id = %d" % id
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

    def get_incident(self, id):
        try:
            query = "SELECT * FROM incidents WHERE incident_id = %d" % id
            self.cursor.execute(query)
            incident = self.cursor.fetchone()
            if incident:
                return dict(incident)
            return None
        except Exception as e:
            pprint(e)

    def get_incidents(self):
        try:
            query = "SELECT * FROM incidents"
            self.cursor.execute(query)
            incidents = self.cursor.fetchall()
            if incidents:
                return incidents
            return None
        except Exception as e:
            pprint(e)

    def get_interventions(self):
        try:
            query = "SELECT * FROM incidents WHERE type = 'intervention'"
            self.cursor.execute(query)
            incidents = self.cursor.fetchall()
            if incidents:
                return incidents
            return None
        except Exception as e:
            pprint(e)
    
    def get_redflags(self):
        try:
            query = "SELECT * FROM incidents WHERE type = 'red-flag'"
            self.cursor.execute(query)
            incidents = self.cursor.fetchall()
            if incidents:
                return incidents
            return None
        except Exception as e:
            pprint(e)

    def check_blacklist(self, auth_token):
        """Checks the blacklist table for a token"""
        try:
            query = "SELECT * FROM blacklist WHERE token = '%s'" % auth_token
            self.cursor.execute(query)
            token = self.cursor.fetchone()
            if token:
                return token
            return None
        except Exception as e:
            pprint(e)

    def edit_incident(self, id, column, data):
        try:
            if column == 'status':
                query = """UPDATE incidents SET status = %s
                        WHERE incident_id = %s"""
            elif column == 'comment':
                query = """UPDATE incidents SET comment = %s
                    WHERE incident_id = %s"""
            elif column == 'location':
                query = """UPDATE incidents SET location = %s
                    WHERE incident_id = %s"""
            self.cursor.execute(query, (data, id))
        except Exception as e:
            pprint(e)

    def delete_from_table(self, table):
        try:
            if table == 'users':
                query = "DELETE FROM  users"
            elif table == 'incidents':
                query = 'DELETE FROM incidents'
            elif table == 'blacklist':
                query = 'DELETE FROM blacklist'
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

    def make_admin(self, id):
        try:
            query="""UPDATE users SET is_admin='t'
                    WHERE userid = %d""" % id
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

if __name__ == '__main__':
    db_name = DatabaseConnection()
    