# -*- coding: utf-8 -*-

from app.mod_profiles.models.StorageLocation import StorageLocation


def get_by_name(name):
    storage_locations = StorageLocation.query.all()
    for storage_location in storage_locations:
        if storage_location.name == name:
            return storage_location
    raise ValueError("No se encuentra una ubicación con la denominación especificada.")
