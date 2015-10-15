# -*- coding: utf-8 -*-

import json
import nose
from nose.tools import *
from app import app, db
from app.mod_profiles.models.Gender import Gender
import unittest


class GenderModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.test_client = app.test_client() # por ahora no lo uso
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_gender_list_get(self):
        g1 = Gender(name='femenino', description='Sexo femenino')
        g2 = Gender(name='masculino', description='Sexo masculino')
        db.session.add_all([g1, g2])
        db.session.commit()
        with self.app.test_request_context(
                '/genders',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            datos = json.loads(res.data)
            eq_(len(datos['resource']), 2)
            self.assertTrue(res.status_code == 200)

    def test_gender_list_post(self):
        with self.app.test_request_context(
                '/genders',
                method='POST',
                data=json.dumps({'name': 'masculino', 'description': 'genero masculino'}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            datos = json.loads(res.data)
            eq_(len(datos), 1)
            self.assertTrue(datos['resource']['name'] == 'masculino')
            self.assertTrue(res.status_code == 201)

    def test_gender_view_get(self):
        g1 = Gender(name='femenino', description='Sexo femenino')
        g2 = Gender(name='masculino', description='Sexo masculino')
        db.session.add_all([g1, g2])
        db.session.commit()
        with self.app.test_request_context(
                '/genders/1',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            assert 'femenino' in res.data
            self.assertTrue(res.status_code == 200)

    def test_gender_view_put(self):
        g1 = Gender(name='femenino', description='Sexo femenino')
        db.session.add_all([g1])
        db.session.commit()
        with self.app.test_request_context(
                '/genders/1',
                method='PUT',
                data=json.dumps({'name': 'femenino', 'description': 'Genero femenino'}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            assert 'Genero' in res.data
            self.assertTrue(res.status_code == 200)

    """
        Faltaría hacer prubas para los otros mensajes de error.
        Probaría un recurso usando user y token (autenticación).
        Pruebas de las fechas para testing de regresión.
        Probar coverage.
        Ver si se puede agregar integración continua.
        Pruebas de carga con alguna herramienta.
    """