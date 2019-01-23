import psycopg2
import psycopg2.extras
from pprint import pprint
import os
from project.server import bcrypt, app
import datetime, jwt

class DatabaseConnection:
    def __init__(self):
        if os.getenv('DB_NAME') == 'ireporter_db_test':
            self.db_name = 'ireporter_db_test'
        else:
            self.db_name = 'ireporter_db'

        try:
            self.connection = psycopg2.connect(
                dbname='ireporter_db_test', user='postgres', host='localhost', password='2SweijecIf', port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        except:
            pprint('Failed to connect to the database.')

    def create_user_table(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS users (userId SERIAL PRIMARY KEY,
                        firstname varchar(32) NOT NULL,
                        lastname varchar(32) NOT NULL,
                        othernames varchar(64) NULL,
                        username varchar(32) NOT NULL,
                        email varchar(128) NOT NULL UNIQUE,
                        password varchar(128) NOT NULL,
                        phone_number varchar(15) NOT NULL,
                        registered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        is_admin BIT NOT NULL DEFAULT '0');
                    """
            self.cursor.execute(query)
            print("Succesfully created users table.")
        except Exception as e:
            pprint(e)

    def create_incidents_table(self):
        try:
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
            print("Successfully created incidents table.")
        except Exception as e:
            pprint(e)

    def create_user(self, **kwargs):
        try:
            query = """
                    INSERT INTO users (firstname, lastname, othernames, username,
                    email, password, phone_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING userid
                    """
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

    def  check_user(self, email):
        try:
            query = "SELECT * FROM users WHERE email = '%s'" % email
            self.cursor.execute(query)
            user = dict(self.cursor.fetchone())
            return user
        except Exception as e:
            pprint(e)
            return None

    def create_incident(self, **kwargs):
        try:
            query = """
                    INSERT INTO incidents (created_by, type, location,
                    images, videos, comment) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING incident_id
                    """
            self.cursor.execute(query, (kwargs['created_by'], kwargs['type'],
                kwargs['location'], kwargs['images'],
                kwargs['videos'], kwargs['comment']))
            incident_id = dict(self.cursor.fetchone())['incident_id']
            return incident_id
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
            incident = dict(self.cursor.fetchone())
            return incident
        except Exception as e:
            pprint(e)

    def generate_auth_token(self, user_id):
        """
        Generates the auth token string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


    def get_incidents(self):
        try:
            query = "SELECT * FROM incidents"
            self.cursor.execute(query)
            incidents = self.cursor.fetchall()
            return incidents
        except Exception as e:
            pprint(e)
    
    def get_redflags(self):
        try:
            query = "SELECT * FROM incidents WHERE type = 'red-flag'"
            self.cursor.execute(query)
            incidents = self.cursor.fetchall()
            return incidents
        except Exception as e:
            pprint(e)
    
    def edit_incident_location(self, id, location):
        try:
            query = """
                    UPDATE incidents
                    SET location = %s
                    WHERE incident_id = %s
                    """
            self.cursor.execute(query, (location, id))
        except Exception as e:
            pprint(e)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def edit_incident_comment(self, id, comment):
        try:
            query = """
                    UPDATE incidents
                    SET comment = %s
                    WHERE incident_id = %s
                    """
            self.cursor.execute(query, (comment, id))
        except Exception as e:
            pprint(e)

    def delete_all_users(self):
        try:
            query = "DELETE FROM  users"
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

    def delete_all_incidents(self):
        try:
            query = 'DELETE FROM incidents'
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)
    
    def drop_user_table(self):
        try:
            query = 'DROP TABLE users'
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

    def drop_incident_table(self):
        try:
            query = 'DROP TABLE incidents'
            self.cursor.execute(query)
        except Exception as e:
            pprint(e)

if __name__ == '__main__':
    db_name = DatabaseConnection()
    # db_name.delete_all_incidents()
    # db_name.create_incident(created_by=3, type='kjshkj',
                            # location='skljlk', comment='sjkjljks',
                            # videos="a.mp4", images="a.jpg")
    # db_name.get_incident(8)
    # print('Create a user')
    # user_id = db_name.create_user(firstname='benjamin', lastname='mayanja',
    #                         othernames='', username='v1b3m', email='v122e@gmi.com',
    #                         password='1234', phone_number='2309908' )
    user = db_name.check_user('v122e@gmi.com')
    print(user['userid'])
    
