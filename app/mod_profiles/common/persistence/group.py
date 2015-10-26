# -*- coding: utf-8 -*-

from app.mod_profiles.models import Group, User


def is_group_admin(group, user):
    """Indica si el usuario es administrador del grupo.

    Retorna el valor booleano que indica si el usuario tiene una membresía de
    administrador en el grupo especificado.

    :param group: Instancia de grupo sobre la que se determina si el usuario es
    administrador.
    :param user: Instancia de usuario por el que se corrobora su estado de
    membresía.
    :return: Valor booleano que indica si el usuario tiene una membresía de
    administrador en el grupo especificado.
    """

    # Valida que el grupo sea correcto.
    if not isinstance(group, Group):
        raise ValueError("El grupo especificado es incorrecto.")

    # Valida que el usuario sea correcto.
    if not isinstance(user, User):
        raise ValueError("El usuario especificado es incorrecto.")

    # Obtiene todas las membresías del grupo.
    group_memberships = group.memberships.all()

    # Verifica cada membresía, determinando si pertenece al usuario
    # especificado.
    for membership in group_memberships:
        if membership.profile.user.first().id == user.id:
            # Si la membresía pertenece al usuario, devuelve el valor del
            # atributo que determina si es administrador del grupo.
            return membership.is_admin

    return False


def is_group_member(group, user):
    """Indica si el usuario es miembro del grupo.

    Retorna el valor booleano que indica si el usuario tiene una membresía en
    el grupo especificado.

    :param group: Instancia de grupo sobre la que se determina si el usuario es
    miembro.
    :param user: Instancia de usuario por el que se corrobora su estado de
    membresía.
    :return: Valor booleano que indica si el usuario tiene una membresía en el
    grupo especificado.
    """

    # Valida que el grupo sea correcto.
    if not isinstance(group, Group):
        raise ValueError("El grupo especificado es incorrecto.")

    # Valida que el usuario sea correcto.
    if not isinstance(user, User):
        raise ValueError("El usuario especificado es incorrecto.")

    # Obtiene todas las membresías del grupo.
    group_memberships = group.memberships.all()

    # Verifica cada membresía, determinando si pertenece al usuario
    # especificado.
    for membership in group_memberships:
        if membership.profile.user.first().id == user.id:
            # Si la membresía pertenece al usuario, devuelve verdadero.
            return True

    return False