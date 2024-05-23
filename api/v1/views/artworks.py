#!/usr/bin/python3
"""Artworks view to handle http request related artworks table"""

from flask import Flask, jsonify, request, session
from models import storage
from models.artwork import Artwork
from api.v1.views import api_views


@api_views.route('/artworks', methods=['GET'], strict_slashes=False)
def get_artworks():
    """Retrieves a list of all Artworks objects"""
    artworks = storage.all(Artwork).values()
    result = [artwork.to_dict() for artwork in artworks]
    for idx, artwork in enumerate(artworks):
        result[idx]["likes"] = artwork.number_of_likes
        result[idx]["liked_by"] = artwork.liked_by
        result[idx]["comments"] = artwork.get_comments
        result[idx]["media"] = artwork.get_media
    return jsonify(result)


@api_views.route(
    '/artworks/<artwork_id>', methods=['GET'], strict_slashes=False
)
def get_artwork(artwork_id):
    """Retrieves a specific Artwork object by id"""
    artwork = storage.get(Artwork, artwork_id)

    if artwork is None:
        return jsonify({'error': 'Not found'}), 404
    result = artwork.to_dict()
    result["likes"] = artwork.number_of_likes
    result["liked_by"] = artwork.liked_by
    result["comments"] = artwork.get_comments
    result["media"] = artwork.get_media
    return jsonify(result)


@api_views.route(
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


@api_views.route('/artworks', methods=['POST'], strict_slashes=False)
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
    result = new_artwork.to_dict()
    result["likes"] = new_artwork.number_of_likes
    result["liked_by"] = new_artwork.liked_by
    result["comments"] = new_artwork.get_comments
    result["media"] = new_artwork.get_media
    return jsonify(result), 201


@api_views.route(
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
    result = artwork.to_dict()
    result["likes"] = artwork.number_of_likes
    result["liked_by"] = artwork.liked_by
    result["comments"] = artwork.get_comments
    result["media"] = artwork.get_media
    return jsonify(result)


@api_views.route(
    '/artworks/<artwork_id>/like', methods=['GET'], strict_slashes=False
)
def like_artwork(artwork_id):
    """Like an Artwork object"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        return jsonify({'error': 'Not found'}), 404

    artist = storage.find('Artist', email=session['email'])
    if artist is None:
        return jsonify({"error": "notActive"})
    if artist in artwork.likes:
        artwork.likes.remove(artist)
    else:
        artwork.likes.append(artist)

    storage.save()
    result = artwork.to_dict()
    result["likes"] = artwork.number_of_likes
    result["liked_by"] = artwork.liked_by
    result["comments"] = artwork.get_comments
    result["media"] = artwork.get_media
    return jsonify(result)
