from flask_script import Manager, Command

from uplink import create_app

manager = Manager(create_app)

if __name__ == '__main__':
    manager.run()
