from flask import Flask, jsonify, request
from sqlalchemy.orm import joinedload
from doctor_model import db, app, Doctor, Review

db.create_all()

@app.route('/')
def hello_world():
    print('this function for hello world executed')
    response = { 'text' : 'Hello, World!' }
    return jsonify(response)

@app.route('/doctors/', methods=['GET', 'POST'])
def get_or_post_doctor():
    if request.method == 'GET':
        return get_all_doctors()
    elif request.method == 'POST':
        return post_doctor(request)

def get_all_doctors():
    query = Doctor.query.all()
    return str(query)

def post_doctor(request):
    # input validation
    data = {}
    try:
        data = request.form['doctor']
    except KeyError:
        error = {"error": "invalid post, must have doctor field"}
        return jsonify(error)

    # adds doctor to database
    doctor = Doctor(name=data['name'])
    db.session.add(doctor)
    db.session.commit()

    response = {
        'id': data['id'],
        'name': doctor.id
    }

    return jsonify(response)

@app.route('/doctors/<int:id>', methods=['GET', 'DElETE'])
def get_or_delete_doctor(id):
    if request.method == 'GET':
        return get_one_doctor(id)
    if request.method == 'DELETE':
        return delete_one_doctor(id)

def get_one_doctor(id):
    # input validation
    doctor = Doctor.query.get(id)
    if doctor:
        response = {
            'id': doctor.id,
            'name': doctor.name
        }
        return jsonify(response)
    else:
        error = {'error': 'doctor_{} could not be found'.format(id)}
        return jsonify(error)

def delete_one_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor is None:
        error = {'invalid_doctor_id' : 'Doctor does not exist and thus cannot be deleted'}
        return jsonify(error)
    db.session.delete(doctor)
    db.session.commit()

    response = { 'success' : 'The doctor was succesffuly deleted'}
    return jsonify(response)

@app.route('/doctors/<int:id>/reviews', methods=['GET', 'POST'])
def get_all_reviews_or_post_review(id):
    if request.method == 'GET':
        return get_all_reviews(id)
    if request.method == 'POST':
        return post_review(request, id)

def get_all_reviews(id):
    # input validation
    doctor = Doctor.query.get(id)
    response = {}
    if doctor:
        response['id'] = doctor.id,
        response['name'] = doctor.name,
        response['reviews'] = {}
    else:
        error = {'invalid_doctor_id': 'doctor could not be found'}
        return jsonify(error)

    reviews = Doctor.query.joinedload('reviews')
    for review in reviews:
        response['reviews'][review.id] = review.desription

    return jsonify(response)

def post_review(request, doctor_id):
    try:
        comment = request.form['review']
        error = {}
        if 'description' not in comment:
            error['no_description'] = 'No description present'
        if 'doctor_id' not in comment:
            error['no_doctor_id'] = 'No doctor_id present'
        if 'doctor_id' in comment and not Doctor.query.get(comment['doctor_id']):
            error['invalid_doctor_id'] = 'Doctor does not exist'
        if error:
            return jsonify(error)

        review = Review(doctor_id=comment['doctor_id'], description=comment['description'])
        db.session.add(review)
        db.session.commit()

        response = {**review, 'id' : review.id}
        return jsonify(response)

    except KeyError:
        error = {'error': 'Review not present in post request'}
        return jsonify(error)

@app.route('/doctors/<int:doctor_id>/reviews/<int:review_id>')
def get_or_delete_review(doctor_id, review_id):
    error = {}
    doctor = Doctor.query.get(doctor_id)
    review = Review.query.get(review_id)
    if doctor is None:
        error['invalid_doctor_id'] = 'Doctor does not exist'
    if review is None:
        error['invalid_review_id'] = 'Review does not exist'
    if error:
        return jsonify(error)

    if request.method == 'GET':
        return get_one_review(doctor, review)
    if doctor.method == 'DELETE':
        return delete_one_review(doctor, review)

def get_one_review(doctor, review):
    response = {**doctor, **review}
    return jsonify(response)

def delete_one_review(doctor, review):
    db.session.delete(review)
    db.session.commit()
    response = { 'success' : 'Review was succesffuly deleted' }
    return jsonify(response)
