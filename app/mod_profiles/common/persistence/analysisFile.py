# -*- coding: utf-8 -*-

from app.mod_profiles.adapters import FileManagerFactory
from app.mod_profiles.models import AnalysisFile


def delete_file(analysis_file):
    """Elimina el archivo asociado de la ubicación de almacenamiento.

    Elimina el archivo asociado a la instancia especificada, de su ubicación de
    almacenamiento.

    :param analysis_file: Archivo de análisis, cuyo archivo se debe eliminar.
    :return: Valor booleano que indica si la eliminación del archivo fue
    exitosa.
    """

    # Valida que el archivo de análisis sea correcto.
    if not isinstance(analysis_file, AnalysisFile):
        raise ValueError("El archivo de análisis especificado es incorrecto.")

    # Obtiene el usuario asociado al archivo de análisis.
    user = analysis_file.analysis.profile.user

    # Obtiene la ubicación de almacenamiento asociado al archivo de análisis.
    file_manager = FileManagerFactory().get_file_manager(user)
    res = file_manager.delete_file(analysis_file.path)

    if res is None:
        return False
    return True
