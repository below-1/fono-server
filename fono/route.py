import json
from flask import (
    Blueprint,
    request,
    current_app
)
import pymongo
from bson.objectid import ObjectId
from fono.mongo import mongo_db
from fono.config import Encoder
from math import (
    floor
)


bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route('kata-tokens/<kata>', methods=['GET'])
def find_kata_tokens(kata : str):
    result = mongo_db.data.find_one({
        'word': kata
    })
    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

@bp.route('kata/<kata>', methods=['GET'])
def find_kata(kata : str):
    query_obj = {
        'word': {
            '$regex': '^' + kata + '.*'
        }
    }
    projection_obj = {
        'word': 1
    }
    result = list( mongo_db.data.find(query_obj, projection_obj).sort('word', pymongo.ASCENDING).limit(10) )
    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp


@bp.route('letters/<tag>', methods=['GET'])
def chars(tag: str):
    query = {
        'tag': tag
    }
    result = list( mongo_db.counter.find(query).sort('letter', pymongo.ASCENDING) )
    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

@bp.route("fiturs/<tag>", methods=['GET'])
def fiturs(tag: str):
    query = {
        'tag': tag
    }
    result = list( mongo_db.fiturs.find(query).sort('idx', pymongo.ASCENDING) )
    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

@bp.route("homograf/<id>", methods=['DELETE'])
def v2_homograf_remove(id: str):
    query = {
        '_id': ObjectId(id)
    }
    result = mongo_db.homograf.delete_one(query)
    resp = current_app.response_class(
        response=json.dumps({
            'deleted': result.deleted_count
        }, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

@bp.route('homograf', methods=['GET'])
def v2_homograf_list():
    page = int(request.args['page'])
    perPage = int(request.args['perPage'])

    totalData = mongo_db.homograf.count_documents({})
    totalPage = floor(totalData / perPage)
    skip = perPage * page

    items = list(mongo_db.homograf.find({}, skip=skip, limit=perPage, sort=[( 'word', pymongo.ASCENDING )]))
    print(items[:10])
    result = {
        'totalData': totalData,
        'totalPage': totalPage,
        'items': items
    }

    resp = current_app.response_class(
        response=json.dumps(result, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp

@bp.route('homograf', methods=['POST'])
def v2_homograf_add():
    homograf_data = request.get_json()
    result = mongo_db.homograf.insert_one(homograf_data)
    
    resp = current_app.response_class(
        response=json.dumps({
            'id': result.inserted_id
        }, cls=Encoder),
        status=200,
        mimetype='application/json'
    )
    return resp
