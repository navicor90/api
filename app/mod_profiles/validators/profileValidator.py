# -*- coding: utf-8 -*-

from globalValidator import is_valid_date
from datetime import date, timedelta

def is_valid_birthday(var):
    valid_date_object = is_valid_date(var)
    if valid_date_object > date.today():
        raise ValueError("La fecha de nacimiento no puede ser mayor a la fecha actual")
    elif valid_date_object < date.today() - timedelta(36500):
        raise ValueError("La fecha es demasiado antigua")
    else:
        return valid_date_object
