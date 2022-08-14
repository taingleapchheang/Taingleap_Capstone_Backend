from email import header
from sched import scheduler
import smtplib
from flask import Flask, request,make_response, abort,jsonify
from flask_cors import CORS
import simplejson as json
import requests
import boto3
import os
from dotenv import load_dotenv
from decimal import Decimal
from bs4 import BeautifulSoup
from sqlalchemy import true
from app.models.BackgroundTasks import BackgroundTasks


load_dotenv()
rainforest_key = os.environ.get("RAINFOREST_API_KEY")
redcircle_key = os.environ.get("REDCIRCLE_API_KEY")

app = Flask(__name__)
CORS(app)

import dynamodb_handler as dynamodb

scheduler = BackgroundTasks(True)
scheduler.start()

@app.route("/<search_input>", methods = ["GET"])
def get_search_result(search_input):
    
    response = requests.get(
        "https://api.rainforestapi.com/request",
        params={"api_key": rainforest_key, "type": "search", "amazon_domain": "amazon.com", "search_term":search_input} 
    )

    # response = requests.get(
    #     "https://api.redcircleapi.com/request", 
    #     params={"api_key": redcircle_key, "type": "search", "search_term":"tv"}
    # )

    products = response.json()["search_results"]
    return jsonify(products)


@app.route("/offers/<asin>", methods = ["GET"])
def get_offer_for_one_product_result(asin):

    response = requests.get(
        "https://api.rainforestapi.com/request",
        params={"api_key": rainforest_key, "type": "offers", "amazon_domain": "amazon.com", "asin":asin} 
    )
    offers = response.json()["offers"]
    return jsonify(offers)
    

@app.route('/table')
def root_route():
    dynamodb.create_a_productList_table()
    return 'Hello World'


@app.route('/watchlist', methods=['POST'])
def add_a_product():

    data = request.get_json()
    db_data = json.loads(json.dumps(data), parse_float=Decimal)

    item = dynamodb.get_an_item_from_watchList(db_data["asin"])

    if item: 
        item['users'] = list(set(item['users'] + db_data['users']))
        del item['product'], item['price'], item['url']
        response = dynamodb.add_user_to_watchList(db_data['asin'], item)
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            abort(make_response({"msg": "User has been successfully added to the existing watchlist"}, 200))
        abort(make_response({"msg": "Some error occcured", "response": response}, 400))
    else:
        response = dynamodb.add_an_item_to_watchlist(db_data['asin'], db_data['product'], db_data['price'], db_data['url'], db_data['users'])    
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            abort(make_response({"msg": "Item has been successfully added to watchlist"}, 201))
        abort(make_response({"msg": "Some error occcured", "response": response}, 400))

@app.route('/watchlist/<string:asin>', methods=['GET'])
def get_a_product_from_watchlist(asin):
    item = dynamodb.get_an_item_from_watchList(asin)
    print(f"This is the response {item}")
        
    if item:
        response = make_response(json.dumps(item), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        abort(make_response({"msg": "Item not found"}, 404))


@app.route('/watchlist/<string:asin>', methods=['PUT'])
def add_users_to_existing_watchlist(asin):

    data = request.get_json()

    response = dynamodb.add_user_to_watchList(asin, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        abort(make_response({"msg": "Updated Successfully","ModifiedAttributes": response['Attributes'],"response": response['ResponseMetadata']}, 200))

    abort(make_response({"msg": "Some error occcured", "response": response}, 400))


@app.route('/watchlist/<string:asin>', methods=['DELETE'])
def delete_an_item(asin):

    response = dynamodb.delete_an_item_from_watchlist(asin)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }

    abort(make_response({"msg": "Some error occcured", "response": response}, 400))


@app.route('/products', methods=['GET'])
def get_all_items():

    item = dynamodb.get_all_items_from_database()

    if item:
        response = make_response(json.dumps(item), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        abort(make_response({"msg": "Item not found"}, 404))


@app.route('/products/<string:asin>', methods=['PUT'])
def update_an_item_price(asin):

    data = request.get_json()

    response = dynamodb.update_price_in_watchList(asin, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        abort(make_response({"msg": "Updated Successfully","ModifiedAttributes": response['Attributes'],"response": response['ResponseMetadata']}, 200))

    abort(make_response({"msg": "Some error occcured", "response": response}, 400))


@app.route('/scheduler/resume', methods=['POST'])
def resume_scheduled_job():
    global scheduler 
    if scheduler.get_is_started():
        return("The scheduled job has already been started ")
    else:
        scheduler = BackgroundTasks(true)
        scheduler.start()
        abort(make_response({"msg": "Successfully resumed the scheduled job"}, 200))

@app.route('/scheduler/stop', methods=['POST'])
def pause_scheduled_job():
    scheduler.pause_scheduled_job()
    abort(make_response({"msg": "Successfully paused the scheduled job"}, 200))
