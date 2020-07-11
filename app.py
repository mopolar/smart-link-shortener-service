#!/usr/local/bin/python3
from flask import Flask, jsonify, render_template, abort, request
from mongoframes import *
from pymongo import MongoClient
import random
import string
from model import *

app = Flask(__name__)
app.mongo = MongoClient('mongodb+srv://m_gamal:polar147@task.npwty.azure.mongodb.net/task?retryWrites=true&w=majority')
Frame._client = app.mongo


def get_single_short_link(slug):
    response = get_link_by_slug(slug)
    if response is None:
        abort(404)
    return jsonify(response.to_json_type())


def get_all_short_links():
    return jsonify(get_all_links())


def generate_new_slug():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


def add_new_short_link(request):
    if 'slug' in request:
        new_slug = request['slug']

        if get_link_by_slug(new_slug):
            response = {
                "status": "failed",
                "slug": new_slug,
                "message": "slug already exists"
            }
            return jsonify(response), 400
    else:
        new_slug = generate_new_slug()
        while get_link_by_slug(new_slug):
            new_slug = generate_new_slug()

    new_short_link = ShortLink(
        slug=new_slug,
        web=request['web'],
        android=DeviceLink(
            primary=request['android']['primary'],
            fallback=request['android']['fallback']
        ),
        ios=DeviceLink(
            primary=request['ios']['primary'],
            fallback=request['ios']['fallback']
        )
    )
    add_short_link(new_short_link)
    response = {
        "status": "successful",
        "slug": new_slug,
        "message": "created successfully"
    }
    return jsonify(response), 201


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/<slug>')
def short_link_slug(slug):
    return get_single_short_link(slug)


@app.route('/shortlinks', methods=['GET', 'POST'])
def short_links():
    if request.method == 'GET':
        return get_all_short_links()
    else:
        return add_new_short_link(request.json)


@app.errorhandler(500)
def bad_request(e):
    return jsonify({}), 500


@app.errorhandler(400)
def bad_request(e):
    response = {
        "status": "failed",
        "message": "Bad Request"
    }
    return jsonify(response), 400


@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(e):
    response = {
        "status": "failed",
        "message": "not found"
    }
    return jsonify(response), 404



if __name__ == '__main__':
    app.run(debug=True)
