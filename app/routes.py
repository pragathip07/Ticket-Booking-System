from flask import request, jsonify
from app import app, db
from app.models import Train, Booking
from bson.objectid import ObjectId
from datetime import datetime
from app.utils import schedule_email, calculate_delay, convert_object_id


@app.route('/trains', methods=['POST'])
def add_train():
    data = request.get_json()

    # Validate train_id
    train_id = data.get('train_id')
    if not train_id or not str(train_id).isdigit() or len(str(train_id)) != 4:
        return jsonify({"message": "Train ID must be a 4-digit number"}), 400

    # Check if train_id is unique
    if db.trains.find_one({'train_id': train_id}):
        return jsonify({"message": "Train ID already exists"}), 400

    train = Train(train_id=train_id, name=data['name'], seats=data['seats'])
    db.trains.insert_one(train.to_dict())
    return jsonify({"message": "Train added successfully"}), 201


@app.route('/trains', methods=['GET'])
def get_trains():
    trains = list(db.trains.find())
    trains = [convert_object_id(train) for train in trains]
    return jsonify(trains), 200
    # get_trains_list = []
    # for train in trains:
    #     train['_id'] = str(train['_id'])
    #     get_trains_list.append(train)
    # return jsonify(get_trains_list)


@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.get_json()
    train = db.trains.find_one({'train_id': data['train_id']})

    if train and train['available_seats'] > 0:
        seat_number = train['seats'] - train['available_seats'] + 1
        booking = Booking(
            train_id=data['train_id'],
            passenger_name=data['passenger_name'],
            seat_number=seat_number,
            email=data['email']
        )

        db.bookings.insert_one(booking.to_dict())
        # db.trains.update_one({'_id': ObjectId(train['_id'])}, {'$inc': {'available_seats': -1}})
        db.trains.update_one(
            {'_id': ObjectId(train['_id'])},
            {
                '$inc': {'available_seats': -1},
                '$push': {'bookings': booking.to_dict()}
            }
        )

        departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M:%S')
        delay = calculate_delay(departure_time)
        schedule_email(booking, delay)

        return jsonify({"message": "Ticket booked successfully"}), 201
    else:
        return jsonify({"message": "No available seats"}), 400


