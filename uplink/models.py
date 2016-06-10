try:
    from __main__ import db
except ImportError:
    from uplink import db


class GenericModel(db.Model):
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

class Rank(GenericModel):
    pass

class Division(GenericModel):
    pass

class Generation(GenericModel):
    pass

class Merit(GenericModel):
    pass

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

class Personnel(db.Model):
    def __init__(self, password, active, generationID, pid, rankID=0, divisionID=0):
        self.password = password
        self.active = active
        self.generationID = generationID
        self.pid = pid
        self.rankID = rankID
        self.divisionID = divisionID
        self.generationID = generationID

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    active = db.Column(db.String(3))
    accessLevel = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    rankID = db.Column(db.Integer, db.ForeignKey(Rank.id))
    divisionID = db.Column(db.Integer, db.ForeignKey(Division.id))
    generationID = db.Column(db.Integer, db.ForeignKey(Generation.id))

    def to_dict(self):
        return {
            'id': self.id,
            'pid': self.pid,
            'active': self.active,
            'rankID': self.rankID,
            'divisionID': self.divisionID,
            'generationID': self.generationID
        }