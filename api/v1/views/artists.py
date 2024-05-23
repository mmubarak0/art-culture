#!/usr/bin/python3
"""Artwork view."""

import models
from api.v1.views import api_views
from flask import jsonify, request, redirect, session
from models.engine.db_storage import classes
from models import storage
from models.artist import Artist
from models.artwork import Artwork


@api_views.route('/api_login', methods=['GET', 'POST'], strict_slashes=False)
def api_login_view():
    """Login view"""
    if request.method == 'POST':
        data = request.get_json()
        if 'email' not in data:
            return jsonify({"error": "missing email"})
        if 'password' not in data:
            return jsonify({"error": "missing password"})
        artist = models.storage.find(Artist, **data)
        if artist:
            session["email"] = data["email"]
            print('Logged in successfully.')
            return jsonify({"login_status": True})
        return jsonify({"login_status": False})
    if 'email' in session:
        email = session['email']
        return jsonify({"login_status": True})
    return jsonify({"login_status": False})

@api_views.route('/artists', methods=['GET'], strict_slashes=False)
def get_artists():
    """Retrieves a list of all Artists objects"""
    artists = storage.all(Artist).values()
    return jsonify([artist.to_dict() for artist in artists])


@api_views.route('/artists/<artist_id>/artworks', methods=['GET'])
def list_artworks_from_artist(artist_id):
    """Cities from artist route."""
    artist = models.storage.get(Artist, artist_id)
    if artist:
        artworks = [artwork.to_dict() for artwork in artist.artworks]
        if artworks:
            return jsonify(artworks)
        return jsonify([])
    return jsonify({"error": "Not found"}), 404


@api_views.route('/artists/<artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    """Artist by id route."""
    artist = models.storage.get(Artist, artist_id)
    if artist:
        return jsonify(artist.to_dict())
    return jsonify({"error": "Not found"}), 404


@api_views.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist_by_id(artist_id):
    """Delete Artist by id route."""
    artist = models.storage.get(Artist, artist_id)
    if artist:
        models.storage.delete(artist)
        models.storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@api_views.route('/artist', methods=['POST'], strict_slashes=False)
def create_artist():
    """Creates a new Artist object"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400
    elif 'artist_id' not in data:
        return jsonify({'error': 'Missing artist_id'}), 400

    new_artist = Artist(**data)
    new_artist.save()
    return jsonify(new_artist.to_dict()), 201


@api_views.route('/artists/<artist_id>', methods=['PUT'])
def alter_artist_by_id(artist_id):
    """Alter Artist by id route."""
    artist = models.storage.get(Artist, artist_id)
    if artist:
        data = {}
        try:
            data = request.get_json()
            dont_touch = ["id", "state_id", "created_at", "updated_at"]
            filtered_data = {
                key: data[key] for key in list(
                    filter(
                        lambda key: key not in dont_touch, data
                    )
                )
            }
            if type(data) is dict:
                for key, value in filtered_data.items():
                    setattr(artist, key, value)
                artist.save()
                return jsonify(artist.to_dict()), 200
        except Exception:
            return jsonify({"error": "Not a JSON"}), 400
    return jsonify({"error": "Not found"}), 404
