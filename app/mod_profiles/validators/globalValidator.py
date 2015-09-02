# -*- coding: utf-8 -*-

def is_int(var):
    """Valida que el parámetro recibido sea un número entero
    
    >>> is_int(42)
    42

    >>> is_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    if not isinstance(var, int):
        raise ValueError("El valor ingresado no es un entero válido")
    else:
        return var

def positive_int(var):
    """Valida que un entero sea positivo

    >>> positive_int(4)
    4

    >>> positive_int(-4)
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado debe ser un entero positivo

    >>> positive_int('hola')
    Traceback (most recent call last):
        ...
    ValueError: El valor ingresado no es un entero válido
    """
    if is_int(var) <= 0:
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
