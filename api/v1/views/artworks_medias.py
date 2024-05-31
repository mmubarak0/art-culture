#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Media """
from models.media import Media
from models.artwork import Artwork
from models import storage
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route("/artworks/<artwork_id>/medias", methods=["GET"], strict_slashes=False)
@swag_from("documentation/medias/get_medias.yml", methods=["GET"])
def get_medias(artwork_id):
    """
    Retrieves the list of all Media objects of an Artwork
    """
    artwork = storage.get(Artwork, artwork_id)

    if not artwork:
        abort(404)

    medias = [media.to_dict() for media in artwork.media]

    return jsonify(medias)


@api_views.route("/medias/<media_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/medias/get_media.yml", methods=["GET"])
def get_media(media_id):
    """
    Retrieves a Media object
    """
    media = storage.get(Media, media_id)
    if not media:
        abort(404)

    return jsonify(media.to_dict())


@api_views.route("/medias/<media_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/medias/delete_medias.yml", methods=["DELETE"])
def delete_media(media_id):
    """
    Deletes a Media Object
    """

    media = storage.get(Media, media_id)

    if not media:
        abort(404)

    storage.delete(media)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route(
    "/artworks/<artwork_id>/medias", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/medias/post_medias.yml", methods=["POST"])
def post_media(artwork_id):
    """
    Creates a Media
    """
    artwork = storage.get(Artwork, artwork_id)

    if not artwork:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "url" not in request.get_json():
        abort(400, description="Missing url")
    if "type" not in request.get_json():
        abort(400, description="Missing type")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()

    data["artwork_id"] = artwork_id
    instance = Media(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@api_views.route("/medias/<media_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/medias/put_medias.yml", methods=["PUT"])
def put_media(media_id):
    """
    Updates a Media
    """
    media = storage.get(Media, media_id)

    if not media:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    accept = ["url", "type", "name"]

    data = request.get_json()
    for key, value in data.items():
        if key in accept:
            setattr(media, key, value)
    storage.save()
    return make_response(jsonify(media.to_dict()), 200)
