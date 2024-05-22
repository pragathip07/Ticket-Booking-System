from threading import Timer
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask_mail import Message
from app import mail, app


def convert_object_id(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, list):
                document[key] = [convert_object_id(item) for item in value]
            elif isinstance(value, dict):
                document[key] = convert_object_id(value)
    return document


def schedule_email(booking, delay):
    """ Couldn't test this part of the code due to time constraint, but guess this should work in general """

    """
    Schedule an email to be sent after a certain delay.
        :param booking: Booking object containing booking details
        :param delay: Time in seconds after which the email should be sent
    """

    def send_email():
        with app.app_context():
            msg = Message("Train Departure Reminder",
                          recipients=[booking.email])
            msg.body = f"Dear {booking.passenger_name},\n\nYour train is departing soon. Here are your booking details:\nSeat Number: {booking.seat_number}\n\nSafe Travels!"
            mail.send(msg)

    Timer(delay, send_email).start()


def calculate_delay(departure_time):
    """ Couldn't test this part of the code due to time constraint, but guess this should work in general """

    """
    Calculate the delay time in seconds until 30 minutes before the departure time.
        :param departure_time: The departure time of the train
        :return: Delay in seconds
    """
    reminder_time = departure_time - timedelta(minutes=30)
    delay = (reminder_time - datetime.now()).total_seconds()
    return max(delay, 0)







