# -*- coding: utf-8 -*-

from re import match, split
from calendar import monthrange
from datetime import date, time, datetime


def is_int(var):
    """Valida que el parámetro recibido sea un número entero
    
    >>> is_int('42')
    42

    >>> is_int('-2')
    -2

    >>> is_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    try:
        return int(var)
    except ValueError: 
        raise ValueError("El valor ingresado no es un entero válido")


def positive_int(var):
    """Valida que un entero sea positivo

    >>> positive_int('4')
    4

    >>> positive_int('-4')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado debe ser un entero positivo

    >>> positive_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    int_var = is_int(var)
    if int_var <= 0:
        raise ValueError("El valor ingresado debe ser un entero positivo")
    else:
        return int_var


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
    if not match(r'(\d{4})[-](\d{1,2})[-](\d{1,2})$', var):
        raise ValueError("Formato de fecha no válido")
    else:
        return var


def is_valid_date(var):
    """ Luego de comprobar si la fecha tiene un formato válido, valida si es posible construir un objeto
    fecha en formato iso 8601
    >>> is_valid_date('1990-06-20')
    datetime.date(1990, 6, 20)

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
    list_var = split(r'-', var)
    if not (int(list_var[0]) in range(1, date.max.year)):
        raise ValueError("La fecha presenta un error en el año")
    elif not (int(list_var[1]) in range(1, 13)):
        raise ValueError("La fecha presenta un error en el mes")
    elif not (int(list_var[2]) in range(1, monthrange(int(list_var[0]), int(list_var[1]))[1] + 1)):
        raise ValueError("La fecha presenta un error en el día")
    else:
        return date(int(list_var[0]), int(list_var[1]), int(list_var[2]))


def is_valid_previous_date(var):
    """ Valida que la fecha previa sea correcta
    >>> is_valid_previous_date('1990-06-20')
    datetime.date(1990, 6, 20)

    >>> is_valid_previous_date('1914-06-20')
    Traceback (most recent call last):
        ...
    ValueError: No es una fecha previa correcta

    >>> is_valid_previous_date('2016-09-10')
    Traceback (most recent call last):
        ...
    ValueError: No es una fecha previa correcta

    """
    date_var = is_valid_date(var)
    min_date = date(1915, 1, 1)
    if not (min_date < date_var < date.today()):
        raise ValueError("No es una fecha previa correcta")
    else:
        return date_var


def is_valid_id(var):
    int_var = positive_int(var)
    return int_var


def is_valid_time_format(var):
    """ Valida que el formato de tiempo sea correcto
    >>> is_valid_time_format('13:32:22.386348')
    [13, 32, 22, 386348]

    >>> is_valid_time_format('113:32:22.386348')
    Traceback (most recent call last):
        ...
    ValueError: El formato del tiempo no es válido
    """
    var = match(r'\d{1,2}:\d{1,2}:\d{1,2}.\d{1,6}$', var)
    if not var:
        raise ValueError("El formato del tiempo no es válido")
    else:
        list_var = split(r'[:|.]', var.group())
        return [int(i) for i in list_var]


def is_valid_time(var):
    list_var = is_valid_time_format(var)
    if not 0 <= list_var[0] < 24:
        raise ValueError("Error en la hora de la fecha")
    elif not 0 <= list_var[1] < 60:
        raise ValueError("Error en los minutos de la fecha")
    elif not 0 <= list_var[2] < 60:
        raise ValueError("Error en los segundos de la fecha")
    elif not (0 <= list_var[3] < 1000000):
        raise ValueError("Error en los microsegundos de la fecha")
    else:
        return time(list_var[0], list_var[1], list_var[2], list_var[3])


def is_valid_datetime(var):
    """Valida que tanto fecha como hora sean correctos
    >>> is_valid_datetime("2015-09-12T13:32:22.386348")
    datetime.datetime(2015, 9, 12, 13, 32, 22, 386348)

    >>> is_valid_datetime("2015-09-12T24:32:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: Error en la hora de la fecha

    >>> is_valid_datetime("2015-09-12T13:70:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: Error en los minutos de la fecha

    >>> is_valid_datetime("2015-09-12T13:32:60.386348")
    Traceback (most recent call last):
        ...
    ValueError: Error en los segundos de la fecha

    >>> is_valid_datetime("2015-09-12T13:32:22.1000000")
    Traceback (most recent call last):
        ...
    ValueError: El formato del tiempo no es válido

    """
    matching = match(r'(^[\d-]{8,10})[^0-9-:.]([\d:.]*$)', var)
    date_var = is_valid_date(matching.group(1))
    time_var = is_valid_time(matching.group(2))
    return datetime(date_var.year, date_var.month, date_var.day, time_var.hour, time_var.minute, time_var.second,
                    time_var.microsecond)
