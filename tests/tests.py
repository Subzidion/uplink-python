import os
import json
import unittest
import tempfile

from uplink import create_app, db
from uplink.models import Generation

from .createDatabase import create_database

class UplinkTestCases(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        create_database(db)
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        db.session.close()
        self.context.pop()

    def testGetIndex(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testGetNonExistentPersonnelByPID(self):
        response = self.client.get('/personnel/1')
        self.assertEqual(response.status_code, 404)

    def testGetNonExistentPersonnelByUsername(self):
        response = self.client.get('/personnel/I_DO_NOT_EXIST')
        self.assertEqual(response.status_code, 404)

    def testGetPersonnelByPID(self):
        response = self.client.get('/personnel/2')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['personnel']['pid'], 2)
        self.assertEqual(data['personnel']['accounts'][0]['username'], 'main.resident')

    def testGetPersonnelByUsername(self):
        response = self.client.get('/personnel/main.resident')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['personnel']['pid'], 2)
        self.assertEqual(data['personnel']['accounts'][0]['username'], 'main.resident')

    def testGetPersonnelAttrByPID(self):
        response = self.client.get('/personnel/2/rankID')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rankID'], 1)

    def testGetPersonnelAttrByUsername(self):
        response = self.client.get('/personnel/main.resident/rankID')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rankID'], 1)

    def testGetNonExistentGeneration(self):
        response = self.client.get('/generation/0')
        self.assertEqual(response.status_code, 404)

    def testGetGeneration(self):
        response = self.client.get('/generation/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['generation']['name'], 'The Generation')
    
    def testGetNonExistentDivision(self):
        response = self.client.get('/division/99')
        self.assertEqual(response.status_code, 404)

    def testGetDivision(self):
        response = self.client.get('/division/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['division']['name'], 'The Division')

    def testGetNonExistentRank(self):
        response = self.client.get('/rank/99')
        self.assertEqual(response.status_code, 404)

    def testGetRank(self):
        response = self.client.get('/rank/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rank']['name'], 'Rank I')

    def testGetNonExistentAccountByID(self):
        response = self.client.get('/account/0')
        self.assertEqual(response.status_code, 404)

    def testGetNonExistentAccountByUsername(self):
        response = self.client.get('/account/I_DO_NOT_EXIST')
        self.assertEqual(response.status_code, 404)

    def testGetAccountByID(self):
        response = self.client.get('/account/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['account']['username'], 'main.resident')

    def testGetAccountByUsername(self):
        response = self.client.get('/account/main.resident')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['account']['username'], 'main.resident')

    def testBadRequest(self):
        response = self.client.post('/division')
        self.assertEqual(response.status_code, 400)
