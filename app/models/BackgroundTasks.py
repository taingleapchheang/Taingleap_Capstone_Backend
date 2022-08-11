from math import fabs
import dynamodb_handler as dynamodb
from bs4 import BeautifulSoup
import simplejson as json
from flask import Flask, request,make_response, abort,jsonify
import requests
from threading import Thread
import time
import smtplib

class BackgroundTasks(Thread):

    def __init__(self, is_started):
        Thread.__init__(self)
        self.is_started = is_started

    def execute_scheduled_call(self):

        # data = dynamodb.get_all_items_from_database()

        # if data:
        #     db_data = make_response(json.dumps(data), 200)
        #     db_data.headers["Content-Type"] = "application/json"
        # else:
        #     print("Unable to get the database")

        # headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        # for record in db_data:
        #     url = record["url"]
        #     page = requests.get(url, headers=headers)
        #     soup = BeautifulSoup(page.content, 'html.parser')
        #     current_price = soup.find(id="corePrice_feature_div").get_text()
        #     print(current_price)
        #     if current_price != record["price"]:
        #         for email in record["users"]:
        #             self.send_mail(email, url)
        #             dynamodb.update_price_in_watchList(record["asin"], {"price": current_price})
        #             print("Price has been updated")

        print("Executing background job..")


    def send_mail(self, email, url):
        server = smtplib.SMTP('smtp@gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('chheangtaingleap@gmail.com', 'cgjqwdfudrwwdtta')

        subject = "Price changes !"
        body= f"Check the Amazon link {url}"
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail('chheangtaingleap@gmail.com', email, msg)
        print("The email has been sent")

        server.quit()

    def run(self):
        print("Starting the background job")
        while self.is_started:
            self.execute_scheduled_call()
            time.sleep(3)

    def get_is_started(self):
        return self.is_started

    def pause_scheduled_job(self):
        self.is_started = False
    def resume_scheduled_job(self):
        self.is_started = True








