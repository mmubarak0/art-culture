""" objects that handle all default RestFul API actions for Messages"""

from models.message import Message
from models.artist import Artist
from models import storage
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route("/artists/<artist_id>/messages", methods=["GET"])
@swag_from("documentation/message/get_messages.yml", methods=["GET"])
def get_messages(artist_id):
    """
    Retrieves the list of all Message objects
    """
    messages = [message.to_dict() for message in storage.all(Message).values()]
    return jsonify(messages)


@api_views.route("/messages/<message_id>", methods=["GET"])
@swag_from("documentation/message/get_message.yml", methods=["GET"])
def get_message(message_id):
    """
    Retrieves a Message object
    """
    message = storage.get(Message, message_id)
    if not message:
        abort(404, description="Message not found")
    return jsonify(message.to_dict())


@api_views.route("/messages/<message_id>", methods=["DELETE"])
@swag_from("documentation/message/delete_message.yml", methods=["DELETE"])
def delete_message(message_id):
    """
    Deletes a Message Object
    """
    message = storage.get(Message, message_id)
    if not message:
        abort(404, description="Message not found")
    storage.delete(message)
    storage.save()
    return make_response(jsonify({}), 200)


@api_views.route("/artists/<artist_id>/messages", methods=["POST"])
@swag_from("documentation/message/post_message.yml", methods=["POST"])
def post_message(artist_id):
    """
    Creates a Message
    """
    if storage.get(Artist, artist_id) is None:
        abort(404, description="Artist not found")
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "receiver_id" not in request.get_json():
        abort(400, description="Missing receiver_id")
    if "content" not in request.get_json():
        abort(400, description="Missing content")

    data = request.get_json()

    if storage.get(Artist, data["receiver_id"]) is None:
        abort(404, description="Receiver not found")

    data["sender_id"] = artist_id
    message = Message(**data)
    message.save()
    return make_response(jsonify(message.to_dict()), 201)

@api_views.route("/messages/<message_id>", methods=["PUT"])
@swag_from("documentation/message/put_message.yml", methods=["PUT"])
def put_message(message_id):
    """
    Updates a Message
    """
    message = storage.get(Message, message_id)
    if not message:
        abort(404, description="Message not found")
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key in ["content"]:
            setattr(message, key, value)
    message.save()
    return make_response(jsonify(message.to_dict()), 200)
