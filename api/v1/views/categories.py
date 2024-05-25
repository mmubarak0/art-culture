#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Categorys"""
from models.category import Category
from models import storage
from api.v1.views import api_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@api_views.route('/categories', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/category/get_categories.yml', methods=['GET'])
def get_categories():
    """
    Retrieves the list of all Category objects
    """

    categories = [category.to_dict() for category in storage.all(Category).values()]

    return jsonify(categories)


@api_views.route('/categories/<category_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/category/get_category.yml', methods=['GET'])
def get_category(category_id):
    """
    Retrieves a Category object
    """
    category = storage.get(Category, category_id)
    if not category:
        abort(404)

    return jsonify(category.to_dict())


@api_views.route('/categories/<category_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/category/delete_category.yml', methods=['DELETE'])
def delete_category(category_id):
    """
    Deletes a Category Object
    """

    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    storage.delete(category)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route('/categories', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/category/post_category.yml', methods=['POST'])
def post_category():
    """
    Creates a Category
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    instance = Category(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@api_views.route('/categories/<category_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/category/put_category.yml', methods=['PUT'])
def put_category(category_id):
    """
    Updates a Category
    """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    accept = ['name']

    for key, value in data.items():
        if key in accept:
            setattr(category, key, value)
    storage.save()
    return make_response(jsonify(category.to_dict()), 200)
