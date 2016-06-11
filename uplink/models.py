from datetime import datetime

try:
    from __main__ import db
except ImportError:
    from uplink import db

class Rank(db.Model):
    def __init__(self, name, description, textureUUID):
        self.name = name
        self.description = description
        self.textureUUID = textureUUID

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    textureUUID = db.Column(db.String(36))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'textureUUID': self.textureUUID
        }

class Division(db.Model):
    def __init__(self, name, description, textureUUID):
        self.name = name
        self.description = description
        self.textureUUID = textureUUID

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    textureUUID = db.Column(db.String(36))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'textureUUID': self.textureUUID
        }

class Generation(db.Model):
    def __init__(self, name, description, textureUUID):
        self.name = name
        self.description = description
        self.textureUUID = textureUUID

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    textureUUID = db.Column(db.String(36))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'textureUUID': self.textureUUID
        }

class Merit(db.Model):
    def __init__(self, name, description, textureUUID):
        self.name = name
        self.description = description
        self.textureUUID = textureUUID

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(256))
    textureUUID = db.Column(db.String(36))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'textureUUID': self.textureUUID
        }

class Account(db.Model):
    def __init__(self, pid, UUID, username, displayName, status):
        self.pid = pid
        self.UUID = UUID
        self.displayName = displayName
        self.status = status

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    UUID = db.Column(db.String(36))
    username = db.Column(db.String(32))
    displayName = db.Column(db.String(32))
    status = db.Column(db.String(4))

    def to_dict(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'UUID': self.UUID,
            'username': self.username,
            'displayName': self.displayName,
            'status': self.status
        }

class PersonnelEnlistment(db.Model):
    def __init__(self, pid, joinDate, generationID):
        self.pid = pid
        self.joinDate = datetime.strptime(joinDate, '%Y-%m-%d %H:%M:%S')
        self.generationID = generationID

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    joinDate = db.Column(db.DateTime)
    generationID = db.Column(db.Integer, db.ForeignKey(Generation.id))
    generation = db.relationship('Generation', foreign_keys=generationID)

    def to_dict(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'joinDate': self.joinDate,
            'generationID': self.generationID,
            'generation': self.generation.name
        }

class Personnel(db.Model):
    def __init__(self, password, active, accessLevel, pid, rankID=0, divisionID=0):
        self.password = password
        self.active = active
        self.accessLevel = accessLevel
        self.pid = pid
        self.rankID = rankID
        self.divisionID = divisionID

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    active = db.Column(db.String(3))
    accessLevel = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    rankID = db.Column(db.Integer, db.ForeignKey(Rank.id))
    rank = db.relationship('Rank', foreign_keys=rankID)
    divisionID = db.Column(db.Integer, db.ForeignKey(Division.id))
    division = db.relationship('Division', foreign_keys=divisionID)

    def to_dict(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'active': self.active,
            'rank': self.rank.name,
            'division': self.division.name,
        }


