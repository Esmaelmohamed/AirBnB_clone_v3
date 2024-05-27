#!/usr/bin/python3
"""places_reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def list_reviews_of_place(place_id):
    ''' Retrieves a list of all Review objects for a Place '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''Creates a Review'''
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_review = Review(text=text, place_id=place_id, user_id=user_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Retrieves a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    '''Updates a Review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')
    review.text = text
    storage.save()
    return jsonify(review.to_dict()), 200
