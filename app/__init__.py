from flask import Flask
from flask_mail import Mail
from pymongo import MongoClient


app = Flask(__name__)
app.config.from_object('app.config.Config')

mail = Mail(app)
client = MongoClient(app.config['MONGO_URL'])
db = client['ticket_bookings_db']

from app import routes

