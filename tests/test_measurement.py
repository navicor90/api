# -*- coding: utf-8 -*-

import json
import unittest

from app import app, db
from app.mod_profiles.models import Analysis, Gender, Measurement, MeasurementSource, \
    MeasurementType, MeasurementUnit, Profile, User


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
        p1 = Profile(last_name='Correa', first_name='Laura', birthday='1998-08-20', gender_id='1', is_health_professional=False)
        ms1 = MeasurementSource(name='Manual', description='Ingreso manual de la medida.')
        mu1 = MeasurementUnit(name='Kilogramo', symbol='kg', suffix='True', )
        mt1 = MeasurementType(name='Peso', description='Medida de peso de una persona')
        u1 = User(username='lcorrea', password='l5ur4', email='lcorrea@yesdoc.com', profile_id='1')
        a1 = Analysis(datetime='2015-10-15 22:58:11.963369', description='Primer toma de medidas de peso',
                      profile_id='1')
        m1 = Measurement(datetime='2015-10-15 23:05:52.393670', value='74', analysis_id='1', profile_id='1',
                         source_id='1', type_id='1', unit_id=1)
        db.session.add_all([g1, p1, ms1, mu1, mt1, u1, a1, m1])
        db.session.commit()
        mt1.measurement_units.append(mu1)
        db.session.add(mt1)
        db.session.commit()
        with self.app.test_request_context(
                '/measurements/1',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            datos = json.loads(res.data)
            self.assertTrue(res.status_code == 200)
