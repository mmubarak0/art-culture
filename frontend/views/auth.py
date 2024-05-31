#!/use/bin/env python3
""" Art and culture authentication views """
from flask import render_template, redirect, session, request, url_for
from models import storage
from models.artist import Artist
from frontend.views import app_views


@app_views.route("/login", methods=["POST", "GET"], strict_slashes=False)
def login():
    """Login the user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return redirect("/login")
        for user in storage.all(Artist).values():
            if user.email == email:
                break
        else:
            return redirect("/login")
        if user.password != password:
            return render_template("auth/login.html", forget_password=True)
        session["artist_id"] = user.id
        return redirect("/feed")
    else:
        return render_template("auth/login.html")


@app_views.route("/signup", methods=["POST", "GET"], strict_slashes=False)
def signup():
    """Sign up the user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        bio = request.form.get("bio")
        if not email or not password:
            return redirect("/signup")
        for user in storage.all(Artist).values():
            if user.email == email:
                return redirect("/signup")
        user = Artist(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )
        storage.new(user)
        storage.save()
        session["artist_id"] = user.id
        return redirect("/feed")
    else:
        return render_template("auth/signup.html")


@app_views.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    """Logout the user"""
    session.pop("artist_id", None)
    return redirect("/")


@app_views.route("/reset_password", methods=["POST", "GET"], strict_slashes=False)
def reset_password():
    """Reset the user password"""
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return redirect("/reset_password")
        for user in storage.all(Artist).values():
            if user.email == email:
                break
        else:
            return redirect("/reset_password")
        return render_template("auth/reset_password.html", email=email)
    else:
        return render_template("auth/reset_password.html")
