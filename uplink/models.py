from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

try:
    from __main__ import db
except ImportError:
    from uplink import db

__all__ = ['Rank', 'Division', 'Generation', 'Merit',
           'Personnel', 'PersonnelEnlistment', 'PersonnelAccount', 'PersonnelMerit']

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


class Personnel(db.Model):
    def __init__(self, pid, active, rankID=0, divisionID=0):
        self.pid = pid
        self.active = active
        self.rankID = rankID
        self.divisionID = divisionID

    pid = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128)) 
    active = db.Column(db.Boolean)
    rankID = db.Column(db.Integer, db.ForeignKey(Rank.id))
    rank = db.relationship('Rank', foreign_keys=rankID)
    divisionID = db.Column(db.Integer, db.ForeignKey(Division.id))
    division = db.relationship('Division', foreign_keys=divisionID)

    def hash_password(self, password):
       self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        if not self.password_hash:
            return False
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            'pid': self.pid,
            'active': self.active,
            'rank': "None" if (self.rank is None) else self.rank.name,
            'division': "None" if (self.rank is None) else self.division.name,
            'accounts': [ account.to_dict() for account in self.accounts ],
            'enlistments': [ enlistment.to_dict() for enlistment in self.enlistments ],
            'merits': [ merit.to_dict() for merit in self.merits ]
        }

class PersonnelEnlistment(db.Model):
    def __init__(self, pid, joinDate, generationID):
        self.pid = pid
        self.joinDate = datetime.strptime(joinDate, '%Y-%m-%d %H:%M:%S')
        self.generationID = generationID

    id = db.Column(db.Integer, primary_key=True)
    joinDate = db.Column(db.DateTime)
    pid = db.Column(db.Integer, db.ForeignKey(Personnel.pid))
    personnel = db.relationship('Personnel', backref='enlistments')
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

class PersonnelAccount(db.Model):
    def __init__(self, pid, UUID, username, displayName, status):
        self.pid = pid
        self.UUID = UUID
        self.username = username
        self.displayName = displayName
        self.status = status

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey(Personnel.pid))
    personnel = db.relationship('Personnel', backref='accounts')
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

class PersonnelMerit(db.Model):
    def __init__(self, pid, meritID, dateAcquired, description):
        self.pid = pid
        self.meritID = meritID
        self.dateAcquired = datetime.strptime(dateAcquired, '%Y-%m-%d %H:%M:%S')
        self.description = description

    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey(Personnel.pid))
    personnel = db.relationship('Personnel', backref='merits')
    meritID = db.Column(db.Integer, db.ForeignKey(Merit.id))
    merit = db.relationship('Merit', foreign_keys=meritID)
    dateAcquired = db.Column(db.DateTime)
    description = db.Column(db.String(256))

    def to_dict(self):
        return {
            'pid': self.pid,
            'merit': self.merit.name,
            'dateAcquired': self.dateAcquired,
            'description': self.description
        }
