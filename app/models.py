from bson.objectid import ObjectId
from datetime import datetime


class Train:
    def __init__(self, train_id, name, seats):
        # self.train_id = train_id
        if ObjectId.is_valid(train_id):
            self.train_id = ObjectId(train_id)
        else:
            self.train_id = train_id

        self.name = name
        self.seats = seats
        self.available_seats = seats
        self.bookings = []

    def to_dict(self):
        return {
            'train_id': str(self.train_id),  # Converting ObjectId to string
            'name': self.name,
            'seats': self.seats,
            'available_seats': self.available_seats,
            'bookings': self.bookings
        }


class Booking:
    def __init__(self, train_id, passenger_name, seat_number, email):
        # self.train_id = ObjectId(train_id)
        if ObjectId.is_valid(train_id):
            self.train_id = ObjectId(train_id)
        else:
            self.train_id = train_id

        self.passenger_name = passenger_name
        self.seat_number = seat_number
        self.email = email
        self.booking_time = datetime.now()

    def to_dict(self):
        return {
            'train_id': str(self.train_id),  # Converting ObjectId to string
            'passenger_name': self.passenger_name,
            'seat_number': self.seat_number,
            'email': self.email,
            'booking_time': self.booking_time
        }



