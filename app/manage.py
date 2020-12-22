from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import sys

from app import app, db

if len(sys.argv) == 3:
    MIGRATION_DIR = None
else:
    MIGRATION_DIR = os.path.join('app', 'migrations')
    
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()