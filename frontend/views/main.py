#!/use/bin/env python3
""" Art and culture main views """
from flask import render_template, session, redirect, request, current_app as app
from models import storage
from models.artist import Artist
from frontend.views import app_views, login_required
import uuid
import os

@app_views.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Display the main page"""
    return render_template("about.html", cache_id=uuid.uuid4())


@app_views.route("/feed", methods=["GET"], strict_slashes=False)
@login_required
def feed():
    """Display the feed page"""
    artist_name = ""
    artist = storage.get(Artist, session["artist_id"])
    artist_name = artist.first_name + " " + artist.last_name
    bio = artist.bio
    return render_template("feed.html", cache_id=uuid.uuid4(), artistName=artist_name, bio=bio)


@app_views.route("/messages", methods=["GET"], strict_slashes=False)
@login_required
def messages():
    """Display the messages page"""
    return render_template("messages.html", cache_id=uuid.uuid4())


@app_views.route("/profile", methods=["GET"], strict_slashes=False)
@login_required
def profile():
    """Display the profile page"""
    return render_template("profile.html", cache_id=uuid.uuid4())


@app_views.route("/profile_settings", methods=["GET"], strict_slashes=False)
@login_required
def profile_settings():
    """Display the profile settings page"""
    return render_template("profile_settings.html", cache_id=uuid.uuid4())

@app_views.route("/create_artwork", methods=["GET", "POST"], strict_slashes=False)
@login_required
def create_artwork():
    """Display the create artwork page"""
    if request.method == "POST":
        if request.form.get("title") == "":
            return redirect("/create_artwork")
        artist_id = request.form.get("artist_id")
        media = request.files.getlist('media')
        for m in media:
            if len(m.filename):
                if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], artist_id)) is False:
                    os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], artist_id))
                m.save(os.path.join(app.config["UPLOAD_FOLDER"], artist_id, m.filename))
        return redirect("/feed")
    return render_template("create.html", cache_id=uuid.uuid4())