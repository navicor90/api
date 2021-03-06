# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.parser import parse
from pytz import UTC

from app import config


def is_int(var):
    """Valida que el parámetro recibido sea un número entero.

    > is_int('42')
    42

    > is_int('-2')
    -2

    > is_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido.
    """
    try:
        return int(var)
    except ValueError:
        raise ValueError("El valor ingresado no es un entero válido.")


def positive_int(var):
    """Valida que un entero sea positivo.

    > positive_int('4')
    4

    > positive_int('-4')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado debe ser un entero positivo.

    > positive_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido.
    """
    int_var = is_int(var)
    if int_var <= 0:
        raise ValueError("El valor ingresado debe ser un entero positivo.")
    else:
        return int_var


def has_int(string):
    """Determina si una cadena de caracteres contiene un número.

    > has_int('hola')
    False

    > has_int('ho12la')
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
    """Valida que una cadena de caracteres no tenga números.

    > string_without_int('hola')
    'hola'

    > string_without_int('ho12la')
    Traceback (most recent call last):
        ...
    ValueError: El texto no puede contener números.
    """
    if has_int(var):
        raise ValueError("El texto no puede contener números.")
    else:
        return var


def is_valid_id(var):
    int_var = positive_int(var)
    return int_var


def is_valid_date(var):
    """Valida si la fecha ingresada es válida.

    Luego de comprobar si la fecha tiene un formato válido, valida si es posible construir un
    objeto fecha en formato ISO8601.

    > is_valid_date('1990-06-20')
    datetime.date(1990, 6, 20)

    > is_valid_date('1990-09-00')
    Traceback (most recent call last):
        ...
    ValueError: day is out of range for month

    > is_valid_date('1990-00-10')
    Traceback (most recent call last):
        ...
    ValueError: month must be in 1..12

    > is_valid_date('0000-09-10')
    Traceback (most recent call last):
        ...
    ValueError: month must be in 1..12
    """
    date_var = parse(var).date()
    return date_var


def is_valid_previous_date(var):
    """Valida que la fecha sea previa a la fecha actual.

    > is_valid_previous_date('1990-06-20')
    datetime.date(1990, 6, 20)

    > is_valid_previous_date('1899-06-20')
    Traceback (most recent call last):
        ...
    ValueError: La fecha ingresada no puede ser anterior al año 1900.

    > is_valid_previous_date('3016-09-10')
    Traceback (most recent call last):
        ...
    ValueError: La fecha ingresada debe ser anterior a la fecha actual.
    """
    date_var = is_valid_date(var)
    if date_var.year < 1900:
        raise ValueError("La fecha ingresada no puede ser anterior al año 1900.")
    elif date_var > date.today():
        raise ValueError("La fecha ingresada no debe ser posterior a la fecha actual.")
    else:
        return date_var


def is_valid_datetime(var):
    """Valida que tanto fecha como hora sean válidos.

    > is_valid_datetime("2015-09-12T13:32:22.386348")
    datetime.datetime(2015, 9, 12, 13, 32, 22, 386348)

    > is_valid_datetime("2015-09-12T24:32:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: hour must be in 0..23

    > is_valid_datetime("2015-09-12T13:70:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: minute must be in 0..59

    > is_valid_datetime("2015-09-12T13:32:60.386348")
    Traceback (most recent call last):
        ...
    ValueError: second must be in 0..59
    """
    datetime_var = parse(var)

    # Comprueba si el valor de fecha y hora tiene información acerca de la zona
    # horaria. Si es así, convierte la existente a UTC.
    if (datetime_var.tzinfo is not None
          and datetime_var.tzinfo.utcoffset(datetime_var) is not None):
        datetime_var = datetime_var.astimezone(UTC)

    # Se quita la información de zona horaria, para su almacenamiento como UTC.
    datetime_var = datetime_var.replace(tzinfo=None)

    return datetime_var


def is_valid_previous_datetime(var):
    """Valida que la fecha y hora sea previa a la actual.

    > is_valid_previous_datetime("2001-09-21T23:33:22.386348")
    datetime.datetime(2001, 9, 21, 23, 33, 22, 386348)

    > is_valid_previous_datetime("1899-09-21T23:33:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: La fecha y hora ingresada no puede ser anterior al año 1900.

    > is_valid_previous_datetime("3016-09-21T23:33:22.386348")
    Traceback (most recent call last):
        ...
    ValueError: La fecha y hora ingresada no debe ser posterior a la fecha y hora actual.
    """
    datetime_var = is_valid_datetime(var)
    if datetime_var.year < 1900:
        raise ValueError("La fecha y hora ingresada no puede ser anterior al año 1900.")
    elif datetime_var > datetime.utcnow():
        raise ValueError("La fecha y hora ingresada no debe ser posterior a la fecha y hora actual.")
    else:
        return datetime_var


def is_valid_image_file(var):
    filename = var.filename
    if not ('.' in filename and filename.rsplit('.', 1)[1] in config['ALLOWED_IMG_EXTENSIONS']):
        raise ValueError("El formato de archivo no corresponde, pruebe con \"jpg\"")
    return var


def is_boolean(var):
    true_values = ['true', '1']
    false_values = ['false', '0']

    var = str(var).lower()
    if var in true_values:
        return True
    elif var in false_values:
        return False

    raise ValueError("El valor ingresado debe ser booleano.")
