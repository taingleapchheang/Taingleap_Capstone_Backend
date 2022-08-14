# import boto3
from operator import attrgetter
from boto3 import client, resource
from decouple import config
from decimal import Decimal



AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")
# AWS_SESSION_TOKEN     = config("AWS_SESSION_TOKEN")

client = client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
    # aws_session_token     = AWS_SESSION_TOKEN,
)

resource = resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
    # aws_session_token     = AWS_SESSION_TOKEN,
)

def create_a_productList_table():
    client.create_table(
    TableName='ProductList',
    KeySchema=[
        {
            'AttributeName': 'asin',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'asin',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    })

ProductListTable = resource.Table('ProductList')
def add_an_item_to_watchlist(asin, product, price, url, user):
    response = ProductListTable.put_item(
    Item={
        'asin': asin,
        'product': product,
        'price': price,
        'url': url,
        'users': user,
    }
)
    return response

def get_an_item_from_watchList(asin):

    response = ProductListTable.get_item(
        Key = {
            'asin': asin
        },
        # AttributesToGet=[
        #     'product', 'price', 'url', 'users'
        # ]
    )
    item = response.get('Item')
    return item

def get_all_items_from_database():

    response = ProductListTable.scan(
    )
    result = response.get("Items")
    return result

def add_user_to_watchList(asin, data:dict):

    response = ProductListTable.update_item(
        Key = {
            'asin': asin
        },
        AttributeUpdates={
            'users': {
                'Value'  : data['users'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    print(data['users'])
    return response

def update_price_in_watchList(asin, data:dict):

    response = ProductListTable.update_item(
        Key = {
            'asin': asin
        },
        AttributeUpdates={
            'price': {
                'Value'  : Decimal(str(data['price'])),
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    return response

def delete_an_item_from_watchlist(asin):

    response = ProductListTable.delete_item(
        Key = {
            'asin': asin
        }
    )

    return response



