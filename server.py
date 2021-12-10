# Importing all need libraries.
from kitchen import Kitchen
import threading
from flask import Flask, request
import time
import json

# Loading the kitchen settings.
kitchen_settings = json.load(open('kitchen_settings.json', 'r'))
menu = json.load(open('menu.json', 'r'))
cooks = json.load(open('cooks.json', 'r'))

kitchen_settings['menu'] = menu
kitchen_settings['cooks'] = cooks

kitchen_obj = None

# Creating the Flask application.
app = Flask(__name__)

@app.route('/order', methods=['POST'])
def receive_order():
    # Getting the order sent to the kitchen.
    order = request.json

    kitchen_obj.receive_order(order)

    return ""

if __name__ == "__main__":
    # Staring the flask app as a thread.
    threading.Thread(target=lambda: {
        app.run(debug=True, use_reloader=False, host="127.0.0.1", port=4000)
    }).start()

    # Creating the Kitchen object and running the main process.
    kitchen_obj = Kitchen(kitchen_settings)
    kitchen_obj.run()