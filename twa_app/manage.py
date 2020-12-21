from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "../twa_app")
sys.path.append(topdir)

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()