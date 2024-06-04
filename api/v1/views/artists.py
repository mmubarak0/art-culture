#!/usr/bin/python3
"""Artwork view."""

import models
from api.v1.views import api_views, path_join
from flask import jsonify, request, abort, make_response
from models import storage
from models.artist import Artist
from flasgger.utils import swag_from
import os


@api_views.route("/artists", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artists/get_artists.yml", methods=["GET"])
def get_artists():
    """Retrieves a list of all Artists objects"""
    artists = storage.all(Artist).values()
    result = []
    for artist in artists:
        artist = artist.to_dict()
        result.append(artist)
    return jsonify(result)


@api_views.route("/artists/<artist_id>/artworks", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artists/get_artworks_from_artist.yml", methods=["GET"])
def list_artworks_from_artist(artist_id):
    """Artworks from artist route."""
    artist = storage.get(Artist, artist_id)
    if artist:
        artworks = artist.artworks
        result = []
        for artwork in artworks:
            artwork = artwork.to_dict()
            result.append(artwork)
        return jsonify(result)
    return abort(404, description="Artist not found")


@api_views.route("/artists/<artist_id>", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artists/get_artist.yml", methods=["GET"])
def get_artist_by_id(artist_id):
    """Artist by id route."""
    artist = storage.get(Artist, artist_id)
    if artist:
        return jsonify(artist.to_dict())
    return abort(404, description="Artist not found")


@api_views.route("/artists/<artist_id>", methods=["DELETE"], strict_slashes=False)
@swag_from("documentation/artists/delete_artist.yml", methods=["DELETE"])
def delete_artist_by_id(artist_id):
    """Delete Artist by id route."""
    artist = storage.get(Artist, artist_id)
    if artist:
        for artwork in artist.artworks:
            for m in artwork.media:
                if os.path.exists(path_join("frontend/", m.url)):
                    os.remove(path_join("frontend/", m.url))
                storage.delete(m)
            for comment in artwork.comments:
                storage.delete(comment)
            storage.delete(artwork)
        for comment in artist.comments:
            storage.delete(comment)
        if artist.profile_picture and artist.profile_picture != "":
            if os.path.exists(path_join("frontend/", artist.profile_picture)):
                os.remove(path_join("frontend/", artist.profile_picture))
        storage.delete(artist)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404, description="Artist not found")


@api_views.route("/artist", methods=["POST"], strict_slashes=False)
@swag_from("documentation/artists/post_artist.yml", methods=["POST"])
def create_artist():
    """Creates a new Artist object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    if "first_name" not in data:
        abort(400, description="Missing first_name")
    artist = Artist(**data)
    artist.save()
    return make_response(jsonify(artist.to_dict()), 201)


@api_views.route("/artists/<artist_id>", methods=["PUT"], strict_slashes=False)
@swag_from("documentation/artists/put_artist.yml", methods=["PUT"])
def alter_artist_by_id(artist_id):
    """Alter Artist by id route."""
    artist = storage.get(Artist, artist_id)
    if artist:
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(artist, key, value)
        artist.save()
        return make_response(jsonify(artist.to_dict()), 200)
    return abort(404, description="Artist not found")


@api_views.route("/artists/<artist_id>/follow", methods=["POST"], strict_slashes=False)
@swag_from("documentation/artists/follow_artist.yml", methods=["POST"])
def follow_artist(artist_id):
    """Follow an artist."""
    artist = storage.get(Artist, artist_id)
    if artist:
        if not request.get_json():
            abort(400, description="Not a JSON")
        data = request.get_json()
        if "artist_id" not in data:
            abort(400, description="Missing artist_id")
        following_id = data["artist_id"]
        following_artist = storage.get(Artist, following_id)
        print(artist.followers)
        if following_artist:
            if following_artist in artist.followers:
                artist.followers.remove(following_artist)
                artist.save()
                return make_response(jsonify({}), 200)
            else:
                artist.followers.append(following_artist)
                artist.save()
                return make_response(jsonify({}), 200)
        return abort(404, description="artist not found")
    return abort(404, description="Artist you want to follow/unfollow not found")


@api_views.route("/artists/<artist_id>/followers", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artists/get_followers.yml", methods=["GET"])
def get_followers(artist_id):
    """Get followers of an artist."""
    artist = storage.get(Artist, artist_id)
    if artist:
        followers = artist.followers
        result = []
        for follower in followers:
            follower = follower.to_dict()
            result.append(follower)
        return jsonify(result)
    return abort(404, description="Artist not found")


@api_views.route("/artists/<artist_id>/following", methods=["GET"], strict_slashes=False)
@swag_from("documentation/artists/get_following.yml", methods=["GET"])
def get_following(artist_id):
    """Get following of an artist."""
    artist = storage.get(Artist, artist_id)
    if artist:
        following = artist.following
        result = []
        for follow in following:
            follow = follow.to_dict()
            result.append(follow)
        return jsonify(result)
    return abort(404, description="Artist not found")


@api_views.route("/artists/<artist_id>/follower_messages", methods=["POST"], strict_slashes=False)
@swag_from("documentation/artists/follower_messages.yml", methods=["POST"])
def get_follower_messages(artist_id):
    """TODO - Get messages between two artists."""
    pass
