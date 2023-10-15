from flask import Flask, render_template, request
import json
import requests
import subprocess

app = Flask(__name__)
url = "https://2478-2610-148-1f02-3000-9d36-aae4-265d-97d.ngrok-free.app/calls"

# Assuming dct is a global variable
name = ""
location = ""
run_script = True
script_name = "final.py"
dct = {}

# # Function to get user's location
# def get_user_location():
#     g = geocoder.ip('me')
#     return g.latlng

# # Function to set up user's name
# def setup():
#     name = request.form.get("name")
#     dct["name"] = name

# Function to handle emergency calls


def emergency(name, emergencyType, written_location, coordinates):
    global dct
    # user_location = get_user_location()
    dct["coordinates"] = coordinates
    dct["location"] = written_location
    dct["emergencyType"] = emergencyType
    dct["name"] = name
    print(f'Emergency {emergencyType} at {coordinates} has been reported.')
    response = requests.post(url, data=json.dumps(dct), headers={
                             "Content-Type": "application/json"})
    id = response.json()["id"]
    return id


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        global name
        global location
        # print()
        print(request.form)
        loc = [request.form['latitude'], request.form['longitude']]
        name = request.form['Name']
        location = request.form['Location']
        if 'Ambulance' in request.form:
            id = emergency(
                request.form['Name'], "Ambulance", request.form['Location'], loc)
        elif 'Police' in request.form:
            id = emergency(request.form['Name'],
                           "Police", request.form['Location'], loc)
        elif 'Fire' in request.form:
            id = emergency(request.form['Name'],
                           "Fire", request.form['Location'], loc)
        if run_script:
            print(id)
            subprocess.run(['python3', script_name, id])
    return render_template('index.html', name=name, location=location)


if __name__ == '__main__':
    app.run(debug=True, port=5023)
