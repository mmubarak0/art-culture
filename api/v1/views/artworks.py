#!/usr/bin/python3
"""Artworks view to handle http request related artworks table"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.artwork import Artwork
from models.artist import Artist
from api.v1.views import api_views
from flasgger.utils import swag_from


@api_views.route("/artworks", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artworks/get_artworks.yml", methods=["GET"])
def get_artworks():
    """Retrieves a list of all Artworks objects"""
    artworks = storage.all(Artwork).values()
    result = []
    for artwork in artworks:
        artwork = artwork.to_dict()
        result.append(artwork)
    return jsonify(result)


@api_views.route("/artworks/<artwork_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artworks/get_artwork.yml", methods=["GET"])
def get_artwork(artwork_id):
    """Retrieves a specific Artwork object by id"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        abort(404, description="Artwork not found")
    result = artwork.to_dict()
    return jsonify(result)


@api_views.route("/artworks/<artwork_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/artworks/delete_artwork.yml", methods=["DELETE"])
def delete_artwork(artwork_id):
    """Deletes an Artwork object by ID"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        abort(404, description="Artwork not found")
    storage.delete(artwork)
    storage.save()
    return make_response(jsonify({}), 200)


@api_views.route("/artworks", methods=["POST"], strict_slashes=False)
@swag_from("documentation/artworks/post_artwork.yml", methods=["POST"])
def create_artwork():
    """Creates a new Artwork object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "artist_id" not in data:
        abort(400, description="Missing artist_id")
    if "title" not in data:
        abort(400, description="Missing title")

    artwork = Artwork(**data)
    artwork.save()
    result = artwork.to_dict()
    return make_response(jsonify(result), 201)


@api_views.route("/artworks/<artwork_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/artworks/put_artwork.yml", methods=["PUT"])
def update_artwork(artwork_id):
    """Updates a Artwork object by ID"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        abort(404, description="Artwork not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "__class__"]:
            setattr(artwork, key, value)
    artwork.save()
    result = artwork.to_dict()
    return jsonify(result)


@api_views.route("/artworks/<artwork_id>/like", methods=["POST"], strict_slashes=False)
@swag_from("documentation/artworks/like_artwork.yml", methods=["POST"])
def like_artwork(artwork_id):
    """Like an Artwork object"""
    artwork = storage.get(Artwork, artwork_id)
    if artwork is None:
        abort(404, description="Artwork not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "artist_id" not in data:
        abort(400, description="Missing artist_id")
    artist = storage.get(Artist, data["artist_id"])
    if artist is None:
        abort(404, description="Artist not found")
    if artist in artwork.likes:
        artwork.likes.remove(artist)
    else:
        artwork.likes.append(artist)

    artwork.save()
    result = artwork.to_dict()
    return jsonify(result)
