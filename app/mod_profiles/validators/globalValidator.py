# -*- coding: utf-8 -*-

import re
import calendar
from datetime import date


def is_int(var):
    """Valida que el parámetro recibido sea un número entero
    
    >>> is_int('42')
    '42'

    >>> is_int('-2')
    '-2'

    >>> is_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    try:
        int(var)
        return var
    except ValueError: 
        raise ValueError("El valor ingresado no es un entero válido")


def positive_int(var):
    """Valida que un entero sea positivo

    >>> positive_int('4')
    '4'

    >>> positive_int('-4')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado debe ser un entero positivo

    >>> positive_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    if int(is_int(var)) <= 0:
        raise ValueError("El valor ingresado debe ser un entero positivo")
    else:
        return var


def has_int(string):
    """Determina si una cadena de caracteres contiene un número
    >>> has_int('hola')
    False

    >>> has_int('ho12la')
    True
    """
    for c in string:
        try:
            int(c)
            return True
        except ValueError:
            continue
    return False


def string_without_int(var):
    """Valida que una cadena de caracteres no tenga números
    >>> string_without_int('hola')
    'hola'

    >>> string_without_int('ho12la')
    Traceback (most recent call last):
        ...
    ValueError: El texto no puede contener enteros
    """
    if has_int(var):
        raise ValueError("El texto no puede contener enteros")
    else:
        return var


def is_valid_date_format(var):
    """ Valida que el formato de la fecha sea válido
    >>> is_valid_date_format('1990-06-20')
    '1990-06-20'

    >>> is_valid_date_format('20-06-1990')
    Traceback (most recent call last):
        ...
    ValueError: Formato de fecha no válido

    >>> is_valid_date_format('1998-09-a0')
    Traceback (most recent call last):
        ...
    ValueError: Formato de fecha no válido

    >>> is_valid_date_format('1998-09-123')
    Traceback (most recent call last):
        ...
    ValueError: Formato de fecha no válido
    """
    if not re.match(r'(\d{4})[-](\d{1,2})[-](\d{1,2})$', var):
        raise ValueError("Formato de fecha no válido")
    else:
        return var


def is_valid_date(var):
    """ Luego de comprobar si la fecha tiene un formato válido, valida si es posible construir un objeto
    fecha en formato iso 8601
    >>> is_valid_date('1990-06-20')
    '1990-06-20'

    >>> is_valid_date('1990-09-00')
    Traceback (most recent call last):
        ...
    ValueError: La fecha presenta un error en el día

    >>> is_valid_date('1990-00-10')
    Traceback (most recent call last):
        ...
    ValueError: La fecha presenta un error en el mes

    >>> is_valid_date('0000-09-10')
    Traceback (most recent call last):
        ...
    ValueError: La fecha presenta un error en el año
    """
    is_valid_date_format(var)
    str_var = re.split(r'-', var)
    if not (int(str_var[0]) in range(1, date.max.year)):
        raise ValueError("La fecha presenta un error en el año")
    elif not (int(str_var[1]) in range(1, 12)):
        raise ValueError("La fecha presenta un error en el mes")
    elif not (int(str_var[2]) in range(1, calendar.monthrange(int(str_var[0]), int(str_var[1]))[1])):
        raise ValueError("La fecha presenta un error en el día")
    else:
        return var


def is_valid_previous_date(var):
    """ Valida que la fecha previa sea correcta
    >>> is_valid_previous_date('1990-06-20')
    '1990-06-20'

    >>> is_valid_previous_date('1914-06-20')
    Traceback (most recent call last):
        ...
    ValueError: No es una fecha previa correcta

    >>> is_valid_previous_date('2016-09-10')
    Traceback (most recent call last):
        ...
    ValueError: No es una fecha previa correcta

    """
    is_valid_date(var)
    min_date = date(1915, 1, 1)
    str_date = re.split(r'-', var)
    current_date = date(int(str_date[0]), int(str_date[1]), int(str_date[2]))
    if not (min_date < current_date < date.today()):
        raise ValueError("No es una fecha previa correcta")
    else:
        return var


def is_valid_id(var):
    positive_int(var)