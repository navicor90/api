# -*- coding: utf-8 -*-

def is_int(var):
    if not isinstance(var, int):
        raise ValueError("El valor ingresado no es un entero válido")
    else:
        return var

def positive_int(var):
    if is_int(var) <= 0:
        raise ValueError("El valor ingresado debe ser un entero positivo")
    else:
        return var
    """
    elif var <= 0:
        raise ValueError("El valor ingresado debe ser un entero positivo")
    """

def has_int(string):
    for c in string:
        try:
            int(c)
            return True
        except ValueError:
            continue
    return False


def string_without_int(var):
    if has_int(var):
        raise ValueError("El texto no puede contener enteros")
    else:
        return var
        


if __name__ == "__main__":
    num_pos = 23
    num_neg = -1
    string = "hola"
    string_num = "ho12la"
    #print is_int(num_pos)
    #print is_int(string)
    print positive_int(num_pos)
    #print positive_int(num_neg)
    #print positive_int(string)
    print string_without_int(string)
    print string_without_int(string_num)
