# manage.py


import os
import unittest
import coverage

from project.server import app
from db import DatabaseConnection

db_name = DatabaseConnection()

if __name__ == '__main__':
    app.run()
