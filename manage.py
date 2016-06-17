import os
import subprocess
import sys

from flask_script import Manager, Command

from uplink import create_app

manager = Manager(create_app)

@manager.command
def createdb():
    """Create database from file"""
    from uplink import createDatabase

@manager.command
def test():
    """Run tests"""
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        #make testing true when you call db config
        pass
    manager.run()
