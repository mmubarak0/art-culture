#!/use/bin/env python3
""" Art and culture main views """
from flask import (
    render_template,
    session,
    redirect,
    request,
    current_app as app,
    jsonify,
)
from models import storage
from models.artist import Artist
from models.artwork import Artwork
from models.media import Media
from frontend.views import app_views, login_required
import uuid
import os
import requests


@app_views.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Display the main page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    return render_template(
        "about.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/feed", methods=["GET"], strict_slashes=False)
@login_required
def feed():
    """Display the feed page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    return render_template(
        "feed.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/messages", methods=["GET"], strict_slashes=False)
@login_required
def messages():
    """Display the messages page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    return render_template(
        "messages.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/profile", methods=["GET"], strict_slashes=False)
@login_required
def profile():
    """Display the profile page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    followers = len(session_artist.followers)
    following = len(session_artist.following)
    return render_template(
        "profile.html",
        cache_id=uuid.uuid4(),
        session_artist=session_artist,
        followers=followers,
        following=following,
    )


@app_views.route("/profile_settings", methods=["GET"], strict_slashes=False)
@login_required
def profile_settings():
    """Display the profile settings page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    return render_template(
        "profile_settings.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/create_artwork", methods=["GET", "POST"], strict_slashes=False)
@login_required
def create_artwork():
    """Display the create artwork page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    if request.method == "POST":
        Data = {}
        image_data = []
        data = request.form
        files = request.files.getlist("media")
        if "title" not in data:
            return redirect("/create_artwork")
        for key in data.keys():
            Data[key] = data[key]
        Data["artist_id"] = session_artist.id
        if (
            os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], session_artist.id))
            is False
        ):
            os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], session_artist.id))
        for f in files:
            if f.filename:
                filename = str(uuid.uuid4()) + "_" + f.filename
                image_data.append(
                    {
                        "url": os.path.join(
                            app.config["UPLOAD_FOLDER"][8:],
                            session_artist.id,
                            filename,
                        ),
                        "type": f.mimetype,
                        "name": f.filename,
                    }
                )
                f.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"], session_artist.id, filename
                    )
                )
        new_artwork = requests.post(
            url=app.config["API_URL"] + "api/v1/artworks", json=Data
        )
        if new_artwork.status_code == 201:
            for image in image_data:
                new_image = requests.post(
                    url=app.config["API_URL"]
                    + "api/v1/artworks/"
                    + new_artwork.json().get("id")
                    + "/medias",
                    json=image,
                )

        return redirect("/feed")
    return render_template(
        "create.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/edit_artwork/<artwork_id>", methods=["GET"], strict_slashes=False)
@login_required
def edit_artwork(artwork_id):
    """Display the edit artwork page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    return render_template(
        "edit.html", cache_id=uuid.uuid4(), session_artist=session_artist
    )


@app_views.route("/artists/<artist_id>", methods=["GET"], strict_slashes=False)
def artist(artist_id):
    """Display the artist page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    artist = storage.get(Artist, artist_id)
    followers = len(artist.followers)
    following = len(artist.following)
    print(artist.followers)
    return render_template(
        "artist_detail.html",
        cache_id=uuid.uuid4(),
        session_artist=session_artist,
        artist=artist,
        followers=followers,
        following=following,
        follow=(session_artist in artist.followers),
    )

@app_views.route("/artworks/<artwork_id>", methods=["GET"], strict_slashes=False)
def artwork(artwork_id):
    """Display the artwork page"""
    session_artist = storage.get(Artist, session.get("artist_id"))
    artwork = storage.get(Artwork, artwork_id)
    return render_template(
        "artwork_detail.html",
        cache_id=uuid.uuid4(),
        session_artist=session_artist,
        artwork=artwork,
    )
