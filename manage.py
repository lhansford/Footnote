#!env/bin/python
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from footnote import app, migrate

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()