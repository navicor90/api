# -*- coding: utf-8 -*-

from app.mod_profiles.models import Measurement, MeasurementType, Profile


def get_by_profile(profile, source_id=None, type_id=None, unit_id=None):
    """Retorna las mediciones asociadas a un perfil específico.

    Retorna todas las instancias existentes de medición, asociadas a un perfil
    específico, ordenadas por fecha y hora de la medición, y filtradas por
    fuente, tipo y unidad de medición.

    :param profile: Perfil asociado a las mediciones requeridas.
    :param source_id: Identificador único de la fuente de medición, para
    filtrar las mediciones del perfil.
    :param type_id: Identificador único del tipo de medición, para filtrar las
    mediciones del perfil.
    :param unit_id: Identificador único de la unidad de medición, para filtrar
    las mediciones del perfil.
    :return: Listado de mediciones asociadas al perfil especificado, ordenado
    por fecha y hora de la medición, y filtradas por fuente, tipo y unidad de
    medición.
    """

    # Valida que el perfil sea correcto.
    if not isinstance(profile, Profile):
        raise ValueError("El perfil especificado es incorrecto.")

    # Obtiene todas las mediciones asociadas al perfil.
    measurements = profile.measurements

    # Filtra las mediciones por fuente de medición.
    if source_id is not None:
        measurements = measurements.filter_by(measurement_source_id=source_id)
    # Filtra las mediciones por tipo de medición.
    if type_id is not None:
        measurements = measurements.filter_by(measurement_type_id=type_id)
    # Filtra las mediciones por unidad de medición.
    if unit_id is not None:
        measurements = measurements.filter_by(measurement_unit_id=unit_id)

    # Ordena las mediciones por fecha y hora, y las retorna.
    measurements = measurements.order_by(Measurement.datetime).all()
    return measurements


def get_latest_by_profile(profile):
    """Retorna las últimas mediciones asociadas a un perfil específico.

    Retorna la última medición de cada tipo de medición, asociadas a un
    perfil específico.

    :param profile: Perfil asociado a las mediciones requeridas.
    :return: Listado conformado por la última medición de cada tipo de
    medición, asociadas al perfil especificado.
    """

    # Valida que el perfil sea correcto.
    if not isinstance(profile, Profile):
        raise ValueError("El perfil especificado es incorrecto.")

    # Obtiene todas las mediciones asociadas al perfil, y las ordena en forma
    # descendente por fecha y hora de medición.
    measurements = profile.measurements.order_by(Measurement.datetime.desc())

    # Obtiene todos los tipos de medición.
    measurement_types = MeasurementType.query.all()

    # Crea una lista vacía para almacenar las últimas mediciones.
    latest_measurements = []

    # Recorre todos los tipos de medición.
    for measurement_type in measurement_types:
        # Filtra las mediciones por el tipo de medición, y obtiene la primera
        # medición (que es la última en fecha y hora de medición, por haber
        # ordenado la lista en forma descendente).
        latest_from_type = measurements.filter_by(measurement_type_id=measurement_type.id).first()
        if latest_from_type is not None:
            # Añade la medición a la lista de últimas mediciones
            latest_measurements.append(latest_from_type)

    return latest_measurements
