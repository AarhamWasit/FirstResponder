from flask import Flask, render_template, redirect
from pymongo import MongoClient
import requests
import jsonify


app = Flask(__name__)



@app.route('/')
def index():

        response = requests.get("https://2478-2610-148-1f02-3000-9d36-aae4-265d-97d.ngrok-free.app/calls")
        print(response.text)
        return render_template("index.html", emergency_calls = response.json())
    #return render_template('index.html')


@app.route('/api_endpoint/<id>', methods=['GET'])
def api_endpoint(id):
    response = requests.delete(f"https://2478-2610-148-1f02-3000-9d36-aae4-265d-97d.ngrok-free.app/calls/{id}", )
    # Perform operations or fetch data for the API response
    data = {'message': 'API request successful!'}
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
