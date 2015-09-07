# -*- coding: utf-8 -*-

from re import match, sub
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
    if not match(r'(\d{1,2})[/|-](\d{1,2})[/|-](\d{4})', var): 
        raise ValueError("Formato de fecha no válido")
    else:
        return var

def is_valid_date(var):
    is_valid_date_format(var)
    valid_date_str_list = sub(r'/|-', ' ', var).split()
    try:
        valid_date_object = date(int(valid_date_str_list[2]),
        int(valid_date_str_list[1]), int(valid_date_str_list[0]))
        return valid_date_object
    except ValueError, ve:
        if 'year' in ve.message:
            raise ValueError("La fecha presenta un error en el año")
        elif 'month must' in ve.message:
            raise ValueError("La fecha presenta un error en el mes")
        else:
            raise ValueError("La fecha presenta un error en el día")

if __name__ == '__main__':
    date1 = 'a0/09/1998'
    date2 = '10/09/1998'
    date3 = '123/09/1998'
    date4 = '10/9/1998'
    date5 = '10/09/199'
    date6 = '00/09/1990'
    date7 = '10/00/1990'
    date8 = '10/09/0000'
    date9 = '10/09/2016'
    date10 = '10/09/1914'
    print "_"*30
    #print "La fecha {0} es válida?: {1}".format(date1, is_valid_date(date1))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date2, is_valid_date(date2))
    print "_"*30
    #print "La fecha {0} es válida?: {1}".format(date3, is_valid_date(date3))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date4, is_valid_date(date4))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date5, is_valid_date(date5))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date6, is_valid_date(date6))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date7, is_valid_date(date7))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date8, is_valid_date(date8))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date9, is_valid_date(date9))
    print "_"*30
    print "La fecha {0} es válida?: {1}".format(date10, is_valid_date(date10))
    print "_"*30

