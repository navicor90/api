# -*- coding: utf-8 -*-

from app.mod_profiles.models import Profile


def get_encryption_percentage(profile):
    """Calcula el porcentaje de archivos encriptados del perfil, y lo retorna.

    Recorre todos los archivos de análisis de los análisis del perfil
    especificado, y calcula el porcentaje de los mismos que se encuentran
    encriptados.

    :param profile: Perfil de usuario a relevar.
    :return: Porcentaje de archivos encriptados del perfil, o "-1.0" si no
    tiene archivos de análisis.
    """

    # Valida que el perfil sea correcto.
    if not isinstance(profile, Profile):
        raise ValueError("El perfil especificado es incorrecto.")

    # Obtiene los análisis del perfil.
    profile_analyses = profile.analyses.all()

    # Inicializa los contadores.
    encrypted_analysis_files = 0
    total_analysis_files = 0

    for analysis in profile_analyses:
        for analysis_file in analysis.analysis_files.all():
            total_analysis_files += 1
            if analysis_file.is_encrypted:
                encrypted_analysis_files += 1

    if total_analysis_files > 0:
        encryption_percentage = (encrypted_analysis_files * 100.0) / total_analysis_files
    else:
        encryption_percentage = -1

    return encryption_percentage
