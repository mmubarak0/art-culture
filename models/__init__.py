#!/usr/bin/python3
"""Package initialization script."""

from models.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()
