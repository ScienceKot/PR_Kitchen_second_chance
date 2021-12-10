# Importing all needed libraries.
from queue import PriorityQueue
import time
from order import Food, Order
import threading
import requests
from cook import Cook
from cooking_aparatus import CookingAparatus

class Kitchen():
    def __init__(self, kitchen_settings : dict) -> None:
        '''
            The constructor of the Kitchen class.
        :param kitchen_settings: dict
            The dictionary with the settings of the kitchen.
        '''
        self.order_list = PriorityQueue()
        self.menu = kitchen_settings["menu"]

        # Creating the cooks of the kitchen.
        self.cooks = [
            Cook(self, i, kitchen_settings['cooks'][i], self.menu) for i in range(len(kitchen_settings["cooks"]))
        ]

        # Creating the cooking apparatus.
        self.cooking_apparatus = {
            "oven" : [CookingAparatus("oven") for i in range(kitchen_settings["n_ovens"])],
            "stove" : [CookingAparatus("stove") for i in range(kitchen_settings["n_stoves"])]
        }

        # Creating the orders and apparatus mutexes.
        self.order_list_mutex = threading.Lock()
        self.apparatus_mutex = threading.Lock()

    def send_order(self, order) -> None:
        '''
            This functions sends a prepared order to the dinning gall.
        :param order: Order
            The object representing the order.
        '''
        distribution = {
            "order_id" : order.order_id,
            "table_id" : order.table_id,
            "waiter_id" : order.waiter_id,
            "items" : order.items,
            "priority" : order.priority,
            "max_wait" : order.max_wait,
            "pick_up_time" : order.pick_up_time,
            "cooking_time" : order.cooking_time,
            "cooking_details" : [
                {"food_id" : food_item.food_id, "cook_id" : food_item.cook_id}
                for food_item in order.food_items
            ]
        }
        r = requests.post("http://127.0.0.1:3000/distribution", json = distribution)

    def run(self):
        '''
            The main running function of the kitchen.
        '''
        # Starting all cooks form the kitchen.
        for cook in self.cooks:
            threading.Thread(target=cook.working).start()

        # Sending all finished orders.
        while True:
            for _, order in self.order_list.queue:
                if order.is_finished() and not order.is_delivered:
                    order.cooking_time = int(time.time()) - order.received_time
                    order.is_delivered = True
                    self.send_order(order)
                    break

            time.sleep(2)

    def receive_order(self, json_order : dict):
        '''
            This functions adds the received order into a queue of orders.
        :param json_order: dict
            The dictionary with the order information.
        '''
        # Creating an order object from the dictionary with the order information.
        order = Order(json_order, self.menu)

        # Adding the order to the list.
        self.order_list.put((-order.priority, order))