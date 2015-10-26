# -*- coding: utf-8 -*-

import json
from nose.tools import *
import unittest

from app import app, db
from app.mod_profiles.models import Gender


class GenderModelTestCase(unittest.TestCase):

    # Preparación del entorno para la ejecución de los tests.
    def setUp(self):
        self.app = app                                  # Seteo de la aplicación
        self.test_client = app.test_client()            # Cliente test de flask, por ahora no lo uso
        self.app_context = self.app.app_context()       # Seteo del contexto de la aplicación
        self.app_context.push()                         # Enlaza el contexto de la aplicación con la aplicación actual
        db.create_all()                                 # Crea las tablas correspondientes a nuestros modelos en la
                                                        # base de datos

    # Limpieza luego de la ejecución de los tests
    def tearDown(self):
        db.session.remove()                             # Quita la sesión
        db.drop_all()                                   # Elimina todas las tablas de la base de datos
        self.app_context.pop()                          # Saca el contexto de la aplicación

    #Test del recurso get
    def test_gender_list_get(self):
        g1 = Gender(name='femenino', description='Sexo femenino')
        g2 = Gender(name='masculino', description='Sexo masculino')
        db.session.add_all([g1, g2])
        db.session.commit()
        with self.app.test_request_context(             # Crea un ambiente WSGI a partir de los argumentos dados.
                '/genders',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()      # Despacha el request y ejecuta request pre y postprocesamiento,
                                                        # cacheo de excepciones HTTP y manejo de errores. El despacho
                                                        # consiste en matchear la URL y devolver un valor de la vista o
                                                        # un manejador de error.
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
            self.assertTrue(datos['resource']['description'] == 'genero masculino')
            self.assertTrue(res.status_code == 201)

    def test_gender_view_get(self):
        g1 = Gender(name='femenino', description='Sexo femenino')
        db.session.add_all([g1])
        db.session.commit()
        with self.app.test_request_context(
                '/genders/1',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            datos = json.loads(res.data)
            self.assertTrue(datos['resource']['name'] == 'femenino')
            self.assertTrue(datos['resource']['description'] == 'Sexo femenino')
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
            datos = json.loads(res.data)
            self.assertTrue(datos['resource']['description'] == 'Genero femenino')
            self.assertTrue(res.status_code == 200)

    def test_gender_view_get_404(self):
        with self.app.test_request_context(
                '/genders/1',
                method='GET',
                data=json.dumps({}),
                headers={'Content-Type': 'application/json'}):
            res = self.app.full_dispatch_request()
            self.assertTrue(res.status_code == 404)
