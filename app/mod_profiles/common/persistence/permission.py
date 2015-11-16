# -*- coding: utf-8 -*-

from app.mod_profiles.models import Analysis, User
from .group import has_shared_analysis


def get_permission_by_user(analysis, user, action):
    """Indica si el usuario puede efectuar una acción sobre un análisis.

    Retorna el valor booleano que indica si el usuario puede efectuar la acción
    indicada sobre un análisis específico.

    :param analysis: Instancia de análisis sobre la que se debe ejecutar la
    acción.
    :param user: Instancia de usuario que pretende ejecutar la acción.
    :param action: Acción a ejecutar por el usuario, sobre el análisis. Los
    valores posibles son 'view_analysis_files', 'edit_analysis_files',
    'view_comments', 'edit_comments', 'view_measurements' y
    'edit_measurements'.
    :return: Valor booleano que indica si el usuario puede efectuar la acción
    indicada sobre un análisis específico.
    """

    # Valida que el análisis sea correcto.
    if not isinstance(analysis, Analysis):
        raise ValueError("El análisis especificado es incorrecto.")

    # Valida que el usuario sea correcto.
    if not isinstance(user, User):
        raise ValueError("El usuario especificado es incorrecto.")

    # Verifica que el usuario sea el dueño del análisis especificado. Si es
    # así, retorna verdadero.
    if user.id == analysis.profile.user.first().id:
        return True

    # Recopila los tipos de permiso sobre el análisis, tanto de usuario como de
    # grupo, existentes para el usuario.
    permission_types = []

    # Obtiene el permiso asociado al análisis y al usuario.
    analysis_permission = analysis.permissions.filter_by(user_id=user.id).first()
    if analysis_permission is not None:
        # Añade el tipo de permiso asociado, a la lista de tipos de permiso.
        analysis_permission_type = analysis_permission.permission_type
        permission_types.append(analysis_permission_type)

    # Obtiene las membresías de grupo, del perfil del usuario.
    profile_group_memberships = user.profile.memberships.all()
    # Recorre las membresías, en busca de aquellos grupos que tengan compartido
    # el análisis.
    for membership in profile_group_memberships:
        group = membership.group
        # Verifica que el grupo tenga compartido el análisis.
        if has_shared_analysis(group, analysis):
            # Añade el tipo de permiso asociado, a la lista de tipos de permiso.
            group_permission_type = membership.permission_type
            permission_types.append(group_permission_type)

    # Recorre los tipos de permiso recopilados, en busca de alguno que permita
    # la acción requerida.
    for permission_type in permission_types:
        if get_permission_from_type(permission_type, action):
            return True

    return False


def get_permission_from_type(permission_type, action):
    # Crea la lista de permisos especificados por el tipo de permiso.
    permissions = {
        'view_analysis_files': permission_type.can_view_analysis_files,
        'view_comments': permission_type.can_view_comments,
        'view_measurements': permission_type.can_view_measurements,
        'edit_analysis_files': permission_type.can_edit_analysis_files,
        'edit_comments': permission_type.can_edit_comments,
        'edit_measurements': permission_type.can_edit_measurements,
    }

    # Obtiene el permiso correspondiente a la acción.
    # En vez de usar el parámetro del método 'get' para indicar el valor por
    # defecto en caso de que la acción sea incorrecta, se utiliza una
    # comparación con 'False'. Esta solución permite resolver los casos en que
    # el permiso del diccionario 'permissions' retorne 'None', y lo considera
    # como 'False'.
    permission = permissions.get(action.lower()) or False
    return permission
