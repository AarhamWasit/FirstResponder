from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import pytz

# Get the local time zone
# Replace 'YourTimeZone' with your specific time zone
local_tz = pytz.timezone('America/New_York')


app = Flask(__name__)
app.config['MONGO_URI'] = ""  # add mongo url
mongo = PyMongo(app)


@app.route('/calls', methods=['GET'])
def get_active_data():
    col = mongo.db['callData']

    # Define the filter query
    filter_query = {"status": {"$ne": "handled"}}

    data = col.find(filter_query)
    ret = []
    for d in data:
        temp = {
            'id': str(d['_id']),
            'name': d['name'],
            'location': d.get('location'),
            'cooridnates': d.get('coordinates'),
            'emergencyType': d['emergencyType'],
            'callTime': d['callTime'].strftime('%Y-%m-%d %H:%M:%S')
        }
        ret.append(temp)

    return jsonify(ret)


@app.route('/calls', methods=['POST'])
def add_data():
    print(request.json)
    col = mongo.db['callData']
    name = request.json['name']
    emgtype = request.json['emergencyType']
    if 'callTime' in request.json:
        callTime = datetime.strptime(
            request.json.get('callTime'), '%Y-%m-%d %H:%M:%S')
    else:
        callTime = datetime.now(local_tz)

    data = {
        'name': name,
        'emergencyType': emgtype,
        'callTime': callTime,
        'caseStatus': "In Progress"
    }
    # print(request.json)
    if "location" in request.json:
        # print("here")
        data['location'] = request.json['location']
    if "coordinates" in request.json:
        # print("here")
        data['coordinates'] = {
            "type": "Point",
            "coordinates": request.json['location']
        }
    result = col.insert_one(data)

    ret = {
        'status': "Success",
        "id": str(result.inserted_id)
    }
    return jsonify(ret)


@app.route('/calls/<id>', methods=['PUT'])
def update_data(id):
    col = mongo.db['callData']
    update_fields = {}

    # Extract and update the fields specified in the request
    if 'name' in request.json:
        update_fields['name'] = request.json['name']
    if 'emergencyType' in request.json:
        update_fields['emergencyType'] = request.json['emergencyType']
    if 'callTime' in request.json:
        update_fields['callTime'] = datetime.now().strptime(
            request.json['callTime'], '%Y-%m-%d %H:%M:%S')
    if 'caseStatus' in request.json:
        update_fields['caseStatus'] = "Updated by AI agent"
    if not update_fields:
        return "Error: No fields to update"

    # Update the document with the specified ID
    result = col.update_one(
        {'_id': ObjectId(id)},
        {
            '$set': update_fields
        }
    )

    if result.modified_count > 0:
        return "Success: Data updated"
    else:
        return "Error: No data updated"


@app.route('/calls/<id>', methods=['DELETE'])
def delete_data(id):
    col = mongo.db['callData']
    update_fields = {}
    # Delete the document with the specified ID
    # result = col.delete_one({'_id': ObjectId(id)})
    update_fields['caseStatus'] = "Handled"

    # Update the document with the specified ID
    result = col.update_one(
        {'_id': ObjectId(id)},
        {
            '$set': update_fields
        })

    if result.modified_count > 0:
        return "Success: Case Status Update"
    else:
        return "Case already handled"


@app.route('/calls/all', methods=['GET'])
def get_all_data():
    col = mongo.db['callData']

    data = col.find()
    ret = []
    for d in data:
        temp = {
            'id': str(d['_id']),
            'name': d['name'],
            'location'
            'emergencyType': d['emergencyType'],
            'callTime': d['callTime'].strftime('%Y-%m-%d %H:%M:%S')
        }
        ret.append(temp)

    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)
