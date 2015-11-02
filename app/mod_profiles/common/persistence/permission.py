# -*- coding: utf-8 -*-

from app.mod_profiles.models import Analysis, User


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

    # Obtiene el permiso asociado al análisis y al usuario.
    analysis_permission = analysis.permissions.filter_by(user_id=user.id).first()

    # Verifica si hay algún permiso existente para ese usuario con respecto al
    # análisis especificado. Si no lo hay, retorna falso.
    if analysis_permission is None:
        return False

    # Obtiene el tipo de permiso asociado.
    permission_type = analysis_permission.permission_type

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
