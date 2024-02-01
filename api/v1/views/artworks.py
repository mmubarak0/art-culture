#!/usr/bin/python3
"""Artworks view to handle http request related artworks table"""

from flask import Flask, jsonify, request
from models import storage
from models.artwork import Artwork
from api.v1.views import app_views


@app_views.route('/artworks', methods=['GET'], strict_slashes=False)
def get_artworks():
    """Retrieves a list of all Artworks objects"""
    artworks = storage.all(Artwork).values()
    return jsonify([artwork.to_dict() for artwork in artworks])


@app_views.route(
    '/artworks/<artwork_id>', methods=['GET'], strict_slashes=False
)
def get_artwork(artwork_id):
    """Retrieves a specific Artwork object by id"""
    artwork = storage.get(Artwork, artwork_id)

    if artwork is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(artwork.to_dict())


@app_views.route(
    '/artworks/<artwork_id>', methods=['DELETE'], strict_slashes=False
)
def delete_artwork(artwork_id):
    """Deletes an Artwork object by ID"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        return jsonify({'error': 'Not found'}), 404
    storage.delete(artwork)
    storage.save()
    return jsonify({})


@app_views.route('/artworks', methods=['POST'], strict_slashes=False)
def create_artwork():
    """Creates a new Artwork object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400
    elif 'artist_id' not in data:
        return jsonify({'error': 'Missing artist_id'}), 400

    new_artwork = Artwork(**data)
    new_artwork.save()
    return jsonify(new_artwork.to_dict()), 201


@app_views.route(
    '/artworks/<artwork_id>', methods=['PUT'], strict_slashes=False
)
def update_artwork(artwork_id):
    """Updates a Artwork object by ID"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    for key, value in data.items():
        setattr(artwork, key, value)

    storage.save()
    return jsonify(artwork.to_dict())
