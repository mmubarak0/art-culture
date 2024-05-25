#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Comments """
from models.comment import Comment
from models.artwork import Artwork
from models.artist import Artist
from models import storage
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route(
    "/artworks/<artwork_id>/comments", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/comments/get_comments.yml", methods=["GET"])
def get_comments(artwork_id):
    """
    Retrieves the list of all Comment objects of an Artwork
    """
    artwork = storage.get(Artwork, artwork_id)

    if not artwork:
        abort(404)

    comments = [comment.to_dict() for comment in artwork.comments]

    return jsonify(comments)


@api_views.route("/comments/<comment_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/comments/get_comment.yml", methods=["GET"])
def get_comment(comment_id):
    """
    Retrieves a Comment object
    """
    comment = storage.get(Comment, comment_id)
    if not comment:
        abort(404)

    return jsonify(comment.to_dict())


@api_views.route("/comments/<comment_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/comments/delete_comments.yml", methods=["DELETE"])
def delete_comment(comment_id):
    """
    Deletes a Comment Object
    """

    comment = storage.get(Comment, comment_id)

    if not comment:
        abort(404)

    storage.delete(comment)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route(
    "/artworks/<artwork_id>/comments", methods=["POST"], strict_slashes=False
)
@swag_from("documentation/comments/post_comments.yml", methods=["POST"])
def post_comment(artwork_id):
    """
    Creates a Comment
    """
    artwork = storage.get(Artwork, artwork_id)

    if not artwork:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "artist_id" not in request.get_json():
        abort(400, description="Missing artist_id")

    data = request.get_json()
    artist = storage.get(Artist, data["artist_id"])

    if not artist:
        abort(404)

    if "content" not in request.get_json():
        abort(400, description="Missing content")

    data["artwork_id"] = artwork_id
    instance = Comment(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@api_views.route("/comments/<comment_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/comments/put_comments.yml", methods=["PUT"])
def put_comment(comment_id):
    """
    Updates a Comment
    """
    comment = storage.get(Comment, comment_id)

    if not comment:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    accept = ["content", "artist_id"]

    data = request.get_json()
    for key, value in data.items():
        if key in accept:
            setattr(comment, key, value)
    storage.save()
    return make_response(jsonify(comment.to_dict()), 200)
