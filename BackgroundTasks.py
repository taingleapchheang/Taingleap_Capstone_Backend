
import dynamodb_handler as dynamodb
from decimal import Decimal
from bs4 import BeautifulSoup
import simplejson as json
from flask import Flask, request,make_response, abort,jsonify
import requests
from threading import Thread
import time
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
rainforest_key = os.environ.get("RAINFOREST_API_KEY")
redcircle_key = os.environ.get("REDCIRCLE_API_KEY")
password = os.environ.get("GOOGLE_PASSWORD")

class BackgroundTasks(Thread):

    def __init__(self, is_started):
        Thread.__init__(self)
        self.is_started = is_started

    def execute_scheduled_call(self):
        data = dynamodb.get_all_items_from_database()

        if not data:
            print("Unable to get the database")

        for record in data:
            print(record)
            print(record["asin"])
            result = requests.get( "https://api.rainforestapi.com/request", params={"api_key": rainforest_key, "type": 
            "search", "amazon_domain": "amazon.com", "search_term":record["asin"]})

            current_price = result.json()["search_results"][0]["prices"][0]["value"]
            print(current_price)

            if int(record["price"]) != int(current_price):
                for email in record["users"]:
                    self.send_mail(email, record["url"])
                    dynamodb.update_price_in_watchList(record["asin"], {"price": current_price})
        print("Ending background job ! See you later :)")



    def send_mail(self, email, url):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('chheangtaingleap@gmail.com', password)

        subject = "Price changes !"
        body= f"Dear ShopSmart Customer ! \n\nCheck the Amazon link {url} for the latest price update"
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail('chheangtaingleap@gmail.com', email, msg)
        print("The email has been sent")

        server.quit()

    def run(self):
        print("Starting the background job")
        while self.is_started:
            self.execute_scheduled_call()
            time.sleep(259200)

    def get_is_started(self):
        return self.is_started

    def pause_scheduled_job(self):
        self.is_started = False
    def resume_scheduled_job(self):
        self.is_started = True







