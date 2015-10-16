# -*- coding: utf-8 -*-
import unittest
from app import app, db
from app.mod_profiles.models.Analysis import Analysis
from app.mod_profiles.models.Gender import Gender
from app.mod_profiles.models.MeasurementSource import MeasurementSource
from app.mod_profiles.models.MeasurementType import MeasurementType
from app.mod_profiles.models.MeasurementUnit import MeasurementUnit
from app.mod_profiles.models.Profile import Profile
from app.mod_profiles.models.User import User
from app.mod_profiles.models.Measurement import Measurement
import json


class MeasurementResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_measurement_post(self):
        g1 = Gender(name='femenino', description='Sexo femenino.')
        p1 = Profile(last_name='Correa', first_name='Laura', birthday='1998-08-20', gender_id='1')
        ms1 = MeasurementSource(name='Manual', description='Ingreso manual de la medida.')
        mu1 = MeasurementUnit(name='Kilogramo', symbol='kg', suffix='True')
        mt1 = MeasurementType(name='Peso', description='Medida de peso de una persona')
        u1 = User(username='lcorrea', password='l5ur4', email='lcorrea@yesdoc.com', profile_id='1')
        a1 = Analysis(datetime='2015-10-15 22:58:11.963369', description='Primer toma de medidas de peso',
                      profile_id='1')
        #m1 = Measurement(datetime='2015-10-15 23:05:52.393670', value='74', analysis_id='1', profile_id='1', measurement_source_id='1', measurement_type_id='1', measurement_unit_id='1')
        db.session.add_all([g1, p1, ms1, mu1, mt1, u1, a1])
        db.session.commit()
        #print u1.password_hash
        #print u1.generate_auth_token()
        with self.app.test_request_context(
                '/measurement_sources/1',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            datos = json.loads(res.data)
            print datos
            self.assertTrue(res.status_code == 200)
