ShopSmart: Back-end Layer

**Setup**
The goal for setup is to cover all of the set up needed at the beginning of this project, which includes:
1. Forking and cloning
2. Managing dependencies
3. Setting up a .env file

Requirements
Fork and Clone
Fork this project repo to your own personal account
Clone this new forked project

Managing Dependencies
Create a virtual environment:
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ # You're in activated virtual environment!
Install dependencies (we've already gathered them all into a requirements.txt file):

(venv) $ pip install -r requirements.txt

Creating a .env File
Create a file named .env.
Create five environment variables that will hold your database URLs.

AWS_ACCESS_KEY_ID to hold your AWS Access Key ID
AWS_SECRET_ACCESS_KEY to hold your AWS Secret Access Key ID
REGION_NAME to hold your AWS region
RAINFOREST_API_KEY to hold your Rainforest API Key
GOOGLE_PASSWORD to hold your Google App key 



