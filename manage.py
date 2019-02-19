from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import Config
from app import app, db

# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(Config)

migrate = Migrate(app, db)
manager = Manager(app)
# jwt = JWTManager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
